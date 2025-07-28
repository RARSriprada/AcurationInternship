# AI-Powered Data Agent

This repository contains a suite of Python scripts that form a complete AI-powered data agent. The agent is capable of gathering information from multiple sources (local PDFs and websites), summarizing the content, and then providing a conversational interface to query that data using the Google Gemini large language model.

## Features

- **PDF Parsing:** Extracts and cleans text from PDF documents. It uses a robust approach that supports both native text extraction and Optical Character Recognition (OCR) for scanned PDFs.
- **Web Scraping:** Fetches content from a specified URL, extracting and cleaning the main text paragraphs.
- **Structured Output:** Saves all processed data and summaries into a single, organized `combined_output.json` file.
- **Flattening Data:** In order to give the data to the llm,we need to convert the json format to a flattened string format as llm are trained on processing text not Structured Data.
- **AI-Powered Summarization:** Utilizes a pre-trained Hugging Face model (`distilbart-cnn-12-6`) to intelligently condense information from both the PDF and the website.
- **Conversational Querying:** Acts as a bridge between the summarized data and the Google Gemini LLM, allowing users to ask natural language questions about the combined information.


## Project Workflow

The project works in two main stages:

1.  **Data Processing (`WebParser.py`):** This script performs the web scraping, PDF parsing, and summarization. It generates the `combined_output.json` file.
2.  **Querying Agent (`agent_pipeline.py`):** This script reads the `combined_output.json` file and uses the Gemini API to answer user questions based on its content.

## Installation
### Import Statements
In WebParser.py
```
import os
import re
import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import pymupdf as fitz
from transformers import pipeline
```

#### os: For interacting with the operating system (though not heavily used in this version).
#### re: The regular expression module for cleaning text.
#### json: For working with JSON data (saving the final output).
#### requests: For sending HTTP requests to scrape web pages.
#### BeautifulSoup from bs4: For parsing HTML content.
#### Path from pathlib: A modern way to handle file system paths.
#### fitz from pymupdf: The core library for opening and extracting text from PDFs.
#### pipeline from transformers: The key library for loading and using the Hugging Face summarization model. 

In agent_pipeline.py
```
import json
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
```

#### json: For reading the combined_output.json file.
#### os: For interacting with the operating system, particularly to get the API key.
#### load_dotenv from dotenv: To load environment variables (like your API key) from a .env file.
#### ChatGoogleGenerativeAI from langchain_google_genai: The specific LangChain class used to connect to and invoke the Gemini model.
#### HumanMessage from langchain_core.messages: A LangChain class used to format the user's input as a message for the model.

### Input Paths
**File Path Input**
**Web URL Input**
**User Question Input**(In runtime)


### Prerequisites

* Python 3.8 or higher
* A Google Gemini API Key (available from [Google AI Studio](https://aistudio.google.com/))

### Steps

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Set up a virtual environment (recommended):**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install the required libraries:**
    ```sh
    pip install -r requirements.txt
    ```
    _Note: You will need to create a `requirements.txt` file from the imported libraries._

4.  **Configure your API key:**
    Create a `.env` file in the project root and add your Google Gemini API key.
    ```
    GOOGLE_API_KEY="your_gemini_api_key_here"
    ```
    Alternatively, the `query_agent.py` script will prompt you to enter the key if the environment variable is not set.

## Usage

### Step 1: Run the Web_parser.py

First, you need to generate the `combined_output.json` file.

### Step2: Run the agent_pipeline.py

Then give the question i.e.prompt to the model

## Output
Initially  **combined_output.json** is generated after running the web_parser.py
This JSON file is the initial output after running web_parser.py. It serves as the consolidated knowledge base, containing all the extracted and summarized information from both the web scraping and PDF parsing processes.
**Purpose: To store the organized and summarized data in a machine-readable format for subsequent querying by the AI agent.**
Later an Ai generated output for **agent_pipeline.py**
After combined_output.json is generated, agent_pipeline.py uses its content to answer user questions. The "AI-generated output" refers to the natural language response produced by the Large Language Model (Google Gemini) based on its analysis of the data contained within combined_output.json.
**Purpose: To provide direct, conversational answers to user queries, leveraging the summarized information from both web and PDF sources.**


## Sample Input
**web_parser.py:**
->pdf path(Resume File)
->web path(Web Article)
**agent_pipeline.py**
->Can you tell me about the key points mentioned in the web article summary?

## Sample output

#### for web_parser.py
{
  "pdf_data": {
    "title": "Example Resume Title",
    "summary": [
      "Summary paragraph 1 of PDF content...",
      "Summary paragraph 2 of PDF content..."
    ],
    "sections": [
      {"section_title": "Part 1", "summary": "Section 1 summary"},
      {"section_title": "Part 2", "summary": "Section 2 summary"}
    ]
  },
  "web_data": {
    "title": "Example Web Article Title",
    "summary": [
      "Summary paragraph 1 of web content...",
      "Summary paragraph 2 of web content..."
    ],
    "links": [
      "https://www.example.com/article"
    ]
  }
}

#### for agent_pipeline.py

Enter your question based on the combined output: Can you tell me about the key points mentioned in the web article summary?

Gemini Response:
The web article summary discusses [AI-generated response detailing key points from the web summary in combined_output.json]. It particularly highlights [another point] and includes a link to https://www.quora.com/How-do-you-get-the-URL-of-specific-section-on-a-Wikipedia-page.

