import os
from pdf2image import convert_from_path
import pytesseract
from PyPDF2 import PdfReader

# Folder containing PDFs
input_folder = "data"
output_file = "datatxt/content.txt"

def extract_text_from_pdf(pdf_path):
    text_content = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_content += text
        if not text_content.strip():
            print(f"[OCR] No text found in {pdf_path}. Running OCR...")
            images = convert_from_path(pdf_path)
            for img in images:
                text_content += pytesseract.image_to_string(img)
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
    return text_content

def process_folder(folder_path, output_path):
    with open(output_path, 'w', encoding='utf-8') as out_file:
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(".pdf"):
                full_path = os.path.join(folder_path, filename)
                print(f"Processing: {full_path}")
                text = extract_text_from_pdf(full_path)
                out_file.write(f"\n----- Start of {filename} -----\n")
                out_file.write(text)
                out_file.write(f"\n----- End of {filename} -----\n\n")
    print(f"\n✅ All content saved to {output_path}")

# Run the script
process_folder(input_folder, output_file)
