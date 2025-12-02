from ..config import ParserConfig
from ..cv.parser import CVParser
import pdfplumber

def read_cv_from_pdf(file: str, encoder: str, config: ParserConfig = None):
    text = ""

    with pdfplumber.open(file) as file:
        for page in file.pages:
            text += page.extract_text() + "\n\n"

    parser = CVParser(encoder, config)

    return parser.parse_cv(text)


def read_text_file(file: str):
    text = [""]

    try:
        with open(file, "r") as content:
            text = content.readlines()
    except:
        pass

    return [x.replace("\n", "") for x in text]