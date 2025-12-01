import pdfplumber

from ats import CVParser, print_cv

path = r"C:\Users\dell\Desktop\Mohamed-Mostafa-Mohamed.pdf"

text = ""

with pdfplumber.open(path) as file:
    for page in file.pages:
        text += page.extract_text() + "\n\n"

parser = CVParser(r"D:\Pretrained Models\nomic-embed-text-v1")

print_cv(parser.parse_cv(text))