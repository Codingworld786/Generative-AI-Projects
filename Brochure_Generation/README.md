
# Brochure Generation

## 🧠 Business Problem

In today’s digital marketplace, platforms like **Amazon** host thousands of product, brand, and category pages, each filled with dense content, multiple internal links, and user-generated data. Navigating and summarizing this information manually for marketing, competitor analysis, or content repurposing is time-consuming and inefficient.

### 💡 Use Case

Imagine a product researcher or a marketing team at a startup wants to analyze Amazon’s **product pages** or **seller storefronts**. They need:
- A summarized view of what each page contains (without reading everything)
- All the relevant links (product, category, related pages)
- A marketing-friendly **brochure-style** summary to present internally or to clients

This is where the **Brochure Generation Tool** comes in — automating the scraping, summarization, and formatting of page data.

---

## 🚀 Project Overview

This project automates the following tasks:

- Scrapes **website content** and all **hyperlinks** from a given URL
- Cleans and processes the raw HTML content
- Summarizes the content using **OpenAI GPT models**
- Generates a formatted, brochure-style text suitable for:
  - Marketing handouts
  - Competitor research briefs
  - Slide decks
  - Customer-facing documentation

---

## 🧰 Technologies Used

- 🕸️ **Web Scraping**:  
  - `requests` – for fetching web page content  
  - `BeautifulSoup` – for parsing and cleaning HTML, extracting text and links

- 🧠 **Content Summarization**:  
  - `OpenAI GPT (e.g., gpt-3.5-turbo / gpt-4)` – for intelligent summarization and conversion into natural language

- 🖨️ **Brochure Formatting**:  
  - Auto-generated markdown or text output organized like a brochure
  - Easy integration into PDFs or HTML presentations

- 📂 **Python Scripts**:  
  - Modular code for scraping, processing, and summarizing
  - Extensible for batch processing or crawling multiple URLs
 
  - 
Sample input URL: https://www.deeplearning.ai/courses/machine-learning-specialization/
Sample output URL : 
- ![image](https://github.com/user-attachments/assets/709e6bf1-12c2-49d4-91f8-bec901a6f737)


