import os
import re
import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import pymupdf as fitz
from transformers import pipeline


PDF_PATH = Path(r"C:/Users/venka/Downloads/2200031639_Resume.pdf")
WEB_URL = "https://www.britannica.com/technology/artificial-intelligence/Is-artificial-general-intelligence-AGI-possible"
WIKI_TXT_PATH = Path("wiki_raw.txt")
OUTPUT_JSON_PATH = Path("combined_output.json")
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files (x86)\tessdata"


summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")


def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)   # collapse multiple spaces/newlines
    return re.sub(r'[^\w\s\.,;:!?\'\"()-]', '', text)  # remove special characters


def extract_text_from_pdf(path: Path) -> str:
    print("[PDF] Extracting text...")
    doc = fitz.open(path)
    full_text = ""
    for page in doc:
        text = page.get_text("text", sort=True)
        if not text.strip():
            ocr_text = page.get_textpage_ocr(language="eng", dpi=300, full=True)
            text = ocr_text.extractText()
        full_text += text + "\n"
    doc.close()
    return clean_text(full_text)


def scrape_web_text(url: str, save_path: Path) -> str:
    print("[Web] Scraping text...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.content, "html.parser")
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
    full_text = "\n".join(p for p in paragraphs if p)
    save_path.write_text(full_text, encoding='utf-8')
    return clean_text(full_text)


def summarize_text(text: str) -> list:
    print("[Summarizer] Summarizing content...")
    max_chunk = 700  # smaller chunk for speed
    chunks = [text[i:i+max_chunk] for i in range(0, len(text), max_chunk)]
    summaries = []
    for chunk in chunks[:4]:  # limit chunks for speed
        result = summarizer(chunk, max_length=90, min_length=25, do_sample=False)
        summaries.append(result[0]["summary_text"])
    return summaries


def save_to_json(pdf_summary: list, web_summary: list, out_path: Path):
    print("[Output] Saving JSON file...")
    data = {
        "PDF_Summary": pdf_summary,
        "Web_Summary": web_summary
    }
    out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"[Done] Output saved at: {out_path.resolve()}")


def main():
    pdf_text = extract_text_from_pdf(PDF_PATH)
    pdf_summary = summarize_text(pdf_text)

    web_text = scrape_web_text(WEB_URL, WIKI_TXT_PATH)
    web_summary = summarize_text(web_text)

    save_to_json(pdf_summary, web_summary, OUTPUT_JSON_PATH)

if __name__ == "__main__":
    main()
