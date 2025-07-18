# AcurationInternship
PDF → Text Converter with OCR Support
What It Does
Reads a PDF file and prints the page count.

Extracts readable text using PyMuPDF.

If a page has no text (like scanned pages), it automatically runs OCR (with Tesseract) to convert images into text.

Why I Made It
Initial problem: Some PDFs had blank pages—text extraction failed.

Solution: I added OCR fallback to ensure every page is processed.

Tesseract issue: It couldn't find its language files because I installed it in C:\Program Files (x86)\tessdata.

Fix: I pointed the script to the correct folder by setting the environment variable before importing PyMuPDF.

 How It Works
Sorts extracted text for proper reading order.

Falls back to OCR only on pages needing it.

Cleans the final output to keep only letters, numbers, spaces, and basic punctuation.

Saves the result as a .txt file matching the PDF name (e.g., resume.pdf → resume.txt).

Skips execution if the input file isn’t a PDF.

To Use It
Install dependencies:

pip install PyMuPDF
Install Tesseract OCR (make sure eng.traineddata is in C:\Program Files (x86)\tessdata).

Edit the PDF_PATH variable in the script.

Run:

python PdfParsing.py
You’ll get console output like:

Page count: 5
✅ Cleaned text saved to: EPAM_JD - Intern+FTE - 2026.txt
