import os
import logging
import json
import re
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from openai import OpenAI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import pandas as pd
from datetime import datetime
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('anti_hacker.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="IOD Data protection(restrict Create, update and delete queries on the database)")

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load prompt from file
try:
    with open("prompt.txt", "r", encoding="utf-8") as f:
        PROMPT_TEMPLATE = f.read()
except FileNotFoundError:
    logger.error("prompt.txt not found")
    raise RuntimeError("prompt.txt is required")

# Pydantic model for request body
class UserQuery(BaseModel):
    query: str

# Fallback rule-based filter for CUD keywords
CUD_KEYWORDS = re.compile(
    r'\b(insert|update|delete|drop|create|alter|truncate|replace|merge|add|remove|modify|change|clear|reset|overwrite|bump)\b',
    re.IGNORECASE
)

# Configuration
CONFIG = {
    "confidence_threshold": 0.7,  # Minimum confidence to trust LLM classification
    "max_query_length": 1000,     # Maximum allowed query length
}

# Excel logging setup
EXCEL_FILE = "query_log.xlsx"
EXCEL_LOCK = threading.Lock()

def log_to_excel(query: str, client_ip: str, status_code: int, response: dict):
    """
    Log the query and API response to an Excel file in a thread-safe manner.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        "Timestamp": timestamp,
        "Client_IP": client_ip,
        "Query": query,
        "Status_Code": status_code,
        "Response": json.dumps(response)
    }

    with EXCEL_LOCK:
        try:
            # If the Excel file exists, append to it; otherwise, create a new one
            if os.path.exists(EXCEL_FILE):
                df = pd.read_excel(EXCEL_FILE)
                df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)
            else:
                df = pd.DataFrame([log_entry])
            
            # Write back to Excel
            df.to_excel(EXCEL_FILE, index=False)
            logger.info(f"Logged query to Excel: {query}")
        except Exception as e:
            logger.error(f"Failed to log to Excel: {str(e)}")

def clean_response(text: str) -> str:
    """
    Clean the LLM response by removing markdown code fences and extra whitespace.
    """
    text = re.sub(r'```(?:json)?\s*\n?(.*?)\n?\s*```', r'\1', text, flags=re.DOTALL)
    return text.strip()

def sanitize_input(query: str) -> str:
    """
    Sanitize user input to prevent injection or abuse.
    """
    # Remove control characters and excessive whitespace
    query = re.sub(r'[\x00-\x1F\x7F]', '', query)
    query = re.sub(r'\s+', ' ', query).strip()
    return query

def classify_query(query: str) -> dict:
    """
    Classify a user query using GPT-4o-mini and a fallback rule-based filter.
    Returns a dict with classification and confidence.
    """
    try:
        # Sanitize input
        query = sanitize_input(query)
        if len(query) > CONFIG["max_query_length"]:
            raise ValueError("Query exceeds maximum length")

        # Prepare the prompt
        formatted_prompt = PROMPT_TEMPLATE.format(query=query)

        # Call GPT-4o-mini
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a precise and security-focused assistant."},
                {"role": "user", "content": formatted_prompt}
            ],
            temperature=0.1,
            max_tokens=150
        )

        # Get and clean response
        raw_response = response.choices[0].message.content.strip()
        logger.debug(f"Raw LLM response: {raw_response}")
        cleaned_response = clean_response(raw_response)

        # Parse JSON
        result = json.loads(cleaned_response)
        classification = result.get("classification", "CUD")
        confidence = result.get("confidence", 0.5)

        # Validate response
        if classification not in ["CUD", "non-CUD"]:
            raise ValueError(f"Invalid classification: {classification}")
        if not (0.0 <= confidence <= 1.0):
            raise ValueError(f"Invalid confidence: {confidence}")

        # Apply confidence threshold
        if confidence < CONFIG["confidence_threshold"]:
            logger.warning(f"Low confidence ({confidence}) for query: {query}")
            classification = "CUD" if CUD_KEYWORDS.search(query) else "non-CUD"
            confidence = 0.8

        # Fallback: Override based on CUD keywords
        if CUD_KEYWORDS.search(query):
            classification = "CUD"
            confidence = max(confidence, 0.9)
        elif classification == "CUD" and not CUD_KEYWORDS.search(query):
            classification = "non-CUD"
            confidence = max(confidence, 0.7)

        logger.info(f"Query: {query} | Classification: {classification} | Confidence: {confidence}")
        return {"classification": classification, "confidence": confidence}

    except Exception as e:
        logger.error(f"Error classifying query '{query}': {str(e)} | Raw response: {raw_response if 'raw_response' in locals() else 'N/A'}")
        # Fallback: Use keyword-based classification
        classification = "CUD" if CUD_KEYWORDS.search(query) else "non-CUD"
        confidence = 0.9 if CUD_KEYWORDS.search(query) else 0.7
        logger.info(f"Fallback classification for '{query}': {classification} | Confidence: {confidence}")
        return {"classification": classification, "confidence": confidence}

@app.post("/query")
@limiter.limit("10/minute")
async def process_query(user_query: UserQuery, request: Request):
    """
    API endpoint to process user queries and restrict CUD operations.
    """
    query = user_query.query.strip()
    client_ip = get_remote_address(request)

    # Basic input validation
    if not query:
        response = {"detail": "Query cannot be empty"}
        log_to_excel(query, client_ip, 400, response)
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # Classify the query
    result = classify_query(query)

    if result["classification"] == "CUD":
        logger.warning(f"Blocked CUD query: {query} | Client IP: {client_ip}")
        response = {
            "detail": "That type of request isn't something I can assist with. What else can I help you with today?"
        }
        log_to_excel(query, client_ip, 403, response)
        raise HTTPException(status_code=403, detail=response["detail"])

    # If non-CUD, allow the query
    response = {
        "status": "allowed",
        "query": query,
        "message": "Query is safe and can be processed.",
        "confidence": result["confidence"]
    }
    log_to_excel(query, client_ip, 200, response)
    return response

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "LLM-Based Anti-Hacker System is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)