import sys
import docx
import PyPDF2
import os

def process_docx(path):
    doc = docx.Document(path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def process_pdf(path):
    text = ""
    with open(path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

files = [
    "/home/hermes/projects/seveso/pozadavky/machatova_20260413.pdf",
    "/home/hermes/projects/seveso/pozadavky/machatova.pdf",
    "/home/hermes/projects/seveso/pozadavky/pozadavky 2026.docx",
    "/home/hermes/projects/seveso/dokumentace/zadani_komunikace/SEVESO náměty_revRJ.docx",
    "/home/hermes/projects/seveso/dokumentace/zadani_komunikace/seveso_analyticke_zadani_krasne.docx"
]

for f_path in files:
    if not os.path.exists(f_path):
        print(f"File not found: {f_path}")
        continue
    print(f"--- START OF FILE: {f_path} ---")
    try:
        if f_path.endswith(".pdf"):
            print(process_pdf(f_path))
        else:
            print(process_docx(f_path))
    except Exception as e:
        print(f"Error processing {f_path}: {e}")
    print(f"--- END OF FILE: {f_path} ---")
