import os
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files (x86)\tessdata"

import re
import pymupdf as fitz
from pathlib import Path

#Replace with ur file name
PDF_PATH = Path(r"")

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
    #Save the cleaned text into a UTF‑8 encoded .txt file ,this can save ur txt file with same name as pdf name.
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

if __name__ == "__main__":
    main()
