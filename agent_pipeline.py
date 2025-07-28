import json
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()

# Prompt for Gemini API key if not set
if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = input("Enter your Google Gemini API key: ")

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    google_api_key=os.environ["GOOGLE_API_KEY"]
)

# Load and parse JSON
with open("combined_output.json", "r", encoding="utf-8") as f:
    raw = json.load(f)

# Flatten content properly
def flatten_data(data):
    flattened = ""

    # --- PDF Data ---
    if "pdf_data" in data:
        pdf = data["pdf_data"]
        flattened += f"PDF Title: {pdf.get('title', '')}\n"
        flattened += "PDF Summary:\n" + "\n".join(pdf.get("summary", [])) + "\n"
        for section in pdf.get("sections", []):
            flattened += f"{section.get('section_title', '')}: {section.get('summary', '')}\n"

    # --- Web Data ---
    if "web_data" in data:
        web = data["web_data"]
        flattened += f"\nWeb Title: {web.get('title', '')}\n"
        flattened += "Web Summary:\n" + "\n".join(web.get("summary", [])) + "\n"
        flattened += "Links:\n" + "\n".join(web.get("links", [])) + "\n"

    return flattened

# Get flattened text
combined_text = flatten_data(raw)

# User prompt
user_prompt = input(" Enter your question based on the combined output: ")

# Final prompt
final_input = f"""
You are an intelligent assistant. Based on the following extracted and summarized data:

{combined_text}

Now answer this user question:

{user_prompt}
"""

# Get Gemini response
response = llm.invoke([HumanMessage(content=final_input)])

# Display result
print("\n Gemini Response:")
print(response.content)
