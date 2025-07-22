# Acuration Internship

## Day 3 — PDF → Text Converter with OCR Support

###  What It Does
- Reads a PDF file and prints the page count.
- Extracts readable text using **PyMuPDF**.
- If a page has no text (e.g., scanned pages), it automatically uses **Tesseract OCR** to extract text from images.

###  Why I Made It
- **Problem**: Some PDFs had blank pages because text extraction failed.
- **Solution**: Added an OCR fallback using Tesseract to ensure every page is processed.
- **Tesseract Issue**: Couldn’t find language files due to installation path.
- **Fix**: Set the `TESSDATA_PREFIX` environment variable to:
  ```
  C:\Program Files (x86)\tessdata
  ```

###  How It Works
- Sorts extracted text for proper reading order.
- Falls back to OCR only on pages that need it.
- Cleans output to keep only letters, numbers, spaces, and basic punctuation.
- Saves result as `.txt` file (e.g., `resume.pdf → resume.txt`).
- Skips execution if the file isn’t a PDF.

### How to Use
1. **Install dependencies:**
   ```bash
   pip install PyMuPDF
   ```
2. **Install Tesseract OCR** (ensure `eng.traineddata` exists at the path above).
3. **Edit** the `PDF_PATH` variable in `PdfParsing.py`.
4. **Run:**
   ```bash
   python PdfParsing.py
   ```

**Expected Output:**
```
Page count: 5
Cleaned text saved to: EPAM_JD - Intern+FTE - 2026.txt
```

---

## Day 4 — Text Parser with JSON Conversion

###  Script: `Parser.py`
Adds two key functions on top of `PdfParsing.py`:

- `txt_to_json`: Converts plain text into a basic key-value JSON format.
- `advanced_json_format`: Generates structured, section-wise JSON from the text.

### How to Use
1. Set your PDF path in the `PDF_PATH` variable.
2. Run:
   ```bash
   python Parser.py
   ```

### 📤 Output
- A cleaned `.txt` file.
- Two JSON outputs printed to console:
  - Basic key-value format
  - Advanced structured format
