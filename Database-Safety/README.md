
# LLM-Based Anti-Hacker System

This system protects databases by classifying and blocking potentially dangerous `Create`, `Update`, and `Delete` (CUD) queries using FastAPI and OpenAI's GPT-4o. It also logs interactions for auditing and applies rate-limiting to prevent abuse.

## Features
- **CUD Query Detection**: Blocks harmful database operations.
- **Rate Limiting**: Limits requests to prevent abuse.
- **Query Logging**: Logs queries to an Excel file for auditing.
- **OpenAI Integration**: Uses GPT-4o for query classification.

## Endpoints

### `POST /query`
Receives and classifies user queries as CUD or non-CUD.
- **Request Body**: `{ "query": "user query" }`
- **Response**:
  - **CUD** queries: Blocked with status `403`.
  - **Non-CUD** queries: Processed with status `200`.

### `GET /`
Health check endpoint: `"LLM-Based Anti-Hacker System is running"`

## Setup

### Requirements
- Python 3.8+
- FastAPI
- OpenAI
- Pandas
- Uvicorn

### Installation
```bash
pip install -r requirements.txt


# Run the app
uvicorn main:app --reload

# Example Request
# POST /query (CUD Example)
{
  "query": "DELETE FROM users WHERE id=1"
}
# Response
{
  "detail": "That type of request isn't something I can assist with."
}

# POST /query (Non-CUD Example)

{
  "query": "Show the products details."
}
# Response

{
  "status": "allowed",
  "query": "Show the products details.",
  "message": "Query is safe.",
  "confidence": 0.85
}
