import pdfplumber
import os

def extract_text_from_pdfs():
    data = {}
    pdf_folder = "kalro_pdfs"

    for pdf_file in os.listdir(pdf_folder):
        pdf_path = os.path.join(pdf_folder, pdf_file)

        with pdfplumber.open(pdf_path) as pdf:
            text = " ".join([page.extract_text() or "" for page in pdf.pages])

        data[pdf_file] = text

    return data

if __name__ == "__main__":
    extracted_data = extract_text_from_pdfs()  # ✅ CALL THE FUNCTION FIRST!

    if not extracted_data:
        print("⚠️ No text extracted. Check if the PDFs exist and contain text.")

    for pdf_file, text in extracted_data.items():
        print(f"\n📄 Extracted from {pdf_file}:\n{text[:500]}...\n")  # Print first 500 characters
