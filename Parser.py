import os
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files (x86)\tessdata"

import re
import pymupdf as fitz
from pathlib import Path
import json
PDF_PATH = Path(r"")
import json
import re

def advanced_json_format(file_path):
    def is_section_header(line):
        # Treat title-case or all-uppercase short lines as section headers
        return (line.istitle() or line.isupper() or len(line.split()) <= 5) and not line.endswith(".")

    def parse_line(line):
        # Try to extract key-value from a line
        if ':' in line:
            parts = line.split(":", 1)
            return {parts[0].strip(): parts[1].strip()}
        elif '-' in line:
            parts = line.split("-", 1)
            return {parts[0].strip(): parts[1].strip()}
        else:
            return line.strip()

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    json_data = {}
    current_section = "General"
    buffer = []

    for line in lines:
        if is_section_header(line):
            # Save previous section
            if buffer:
                structured = []
                for b in buffer:
                    parsed = parse_line(b)
                    structured.append(parsed)
                json_data[current_section] = structured
                buffer = []
            current_section = line
        else:
            buffer.append(line)

    # Save last section
    if buffer:
        structured = []
        for b in buffer:
            parsed = parse_line(b)
            structured.append(parsed)
        json_data[current_section] = structured

    return json.dumps(json_data, indent=2)

def txt_to_json(file_path):
    # Converts a key-value text file to a JSON dictionary.Example line format: Name: Alice

    data = {}

    with open(file_path, 'r') as file:
        for line in file:
            if ':' in line:
                key, value = line.strip().split(":", 1)
                data[key.strip()] = value.strip()

    return json.dumps(data, indent=2)




def extract_text(path: Path) -> str:

    #For each page:Try native extraction with sorted text for correct order. & If empty, run OCR (English) using Tesseract.

    doc = fitz.open(path)
    print("Page count:", doc.page_count)

    output = ""
    for page in doc:
        txt = page.get_text("text", sort=True)
        if not txt.strip():
            tp = page.get_textpage_ocr(language="eng", dpi=300, full=True)
            txt = tp.extractText()
        output += txt + "\n"

    doc.close()
    return output

def clean_text(text: str) -> str:

   #Keep only letters and Punctuations not Special Sysmbols

    pattern = r'[^A-Za-z0-9\s\.,;:!\?\'\"\-\(\)]+'
    return re.sub(pattern, '', text)

def get_output_path(pdf_path: Path) -> Path:
    #Generate a .txt file path with the same base name as the PDF.
    return pdf_path.with_suffix(".txt")

def save_to_txt(text: str, txt_path: Path):
    #Save the cleaned text into a UTF‑8 encoded .txt file.
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

def main():

    pdf = PDF_PATH
    if pdf.suffix.lower() != ".pdf":
        print(f" Skipped: {pdf} is not a PDF file.")
        return
    txt = get_output_path(pdf)
    print("Opening PDF:", pdf)

    raw = extract_text(pdf)
    cleaned = clean_text(raw)
    save_to_txt(cleaned, txt)

    print("Cleaned text saved to:", txt)
    # Call the function and print JSON output
    print("First Version of JSON O/p")
    json_result = txt_to_json(txt)
    print(json_result)
    print("Second Version of JSON O/p using NLP")
    json_output_advanced = advanced_json_format(txt)
    print(json_output_advanced)

if __name__ == "__main__":
    main()
