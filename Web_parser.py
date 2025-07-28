import os
import re
import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import pymupdf as fitz
from transformers import pipeline

# Configuration
PDF_PATH = Path("C:/Users/venka/Downloads/2200031639_Resume.pdf")  # <-- Replace with your actual file path
WEB_URL = "https://www.britannica.com/technology/artificial-intelligence/Is-artificial-general-intelligence-AGI-possible"
WIKI_TXT_PATH = Path("wiki_raw.txt")
OUTPUT_JSON_PATH = Path("combined_output.json")

# Load Hugging Face summarizer
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def clean_text(text: str) -> str:
    return re.sub(r'[^\w\s\.,;:!?\'\"()-]', '', re.sub(r'\s+', ' ', text))

def extract_text_from_pdf(path: Path) -> tuple:
    doc = fitz.open(path)
    full_text = "".join(page.get_text("text", sort=True) + "\n" for page in doc)
    title = path.stem.replace('_', ' ').title()
    doc.close()
    return title, clean_text(full_text)

def scrape_web_text(url: str, save_path: Path) -> tuple:
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.content, "html.parser")
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
    full_text = "\n".join(paragraphs)
    save_path.write_text(full_text, encoding='utf-8')
    title = soup.title.text.strip() if soup.title else "Web Content"
    return title, clean_text(full_text)

def summarize_text(text: str, max_chunk: int = 700) -> list:
    chunks = [text[i:i+max_chunk] for i in range(0, len(text), max_chunk)]
    return [summarizer(chunk, max_length=90, min_length=25, do_sample=False)[0]["summary_text"] for chunk in chunks[:4]]

def save_to_json(pdf_title, pdf_summary, web_title, web_summary, web_url, out_path: Path):
    data = {
        "pdf_data": {
            "title": pdf_title,
            "summary": pdf_summary,
            "sections": [{"section_title": f"Part {i+1}", "summary": s} for i, s in enumerate(pdf_summary)]
        },
        "web_data": {
            "title": web_title,
            "summary": web_summary,
            "links": [web_url]
        }
    }
    out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"[Done] Output saved at: {out_path.resolve()}")

def main():
    pdf_title, pdf_text = extract_text_from_pdf(PDF_PATH)
    pdf_summary = summarize_text(pdf_text)

    web_title, web_text = scrape_web_text(WEB_URL, WIKI_TXT_PATH)
    web_summary = summarize_text(web_text)

    save_to_json(pdf_title, pdf_summary, web_title, web_summary, WEB_URL, OUTPUT_JSON_PATH)

if __name__ == "__main__":
    main()
