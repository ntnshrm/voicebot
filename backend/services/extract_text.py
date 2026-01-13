from pypdf import PdfReader
import easyocr
from PIL import Image

reader = easyocr.Reader(['en'])

def extract_text(file_path):
    if file_path.lower().endswith(".pdf"):
        pdf = PdfReader(file_path)
        return "\n".join(page.extract_text() or "" for page in pdf.pages)
    else:
        result = reader.readtext(file_path, detail=0)
        return "\n".join(result)
