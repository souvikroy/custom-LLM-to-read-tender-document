import sys
import PyPDF2

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_text.py <pdf_path>")
        sys.exit(1)
    pdf_path = sys.argv[1]
    text = extract_text_from_pdf(pdf_path)
    print(text)
