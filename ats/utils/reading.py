import pickle

from ..requriement.parser import RequirementParser
from ..requriement.base import JobRequirement
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


def read_text_file(file: str) -> list[str]:
    text = [""]

    try:
        with open(file, "r") as content:
            text = content.readlines()
    except:
        pass

    return [x.replace("\n", "") for x in text]


def read_requirements_from_text(file: str, encoder: str, config: ParserConfig = None) -> JobRequirement:
    parser = RequirementParser(encoder, config)

    return parser.parse_requirement(read_text_file(file))


def save_data(path: str, data: object):
    with open(path + ".ats", 'wb') as file:
        pickle.dump(data, file)


def load_saved_data(file_name: str) -> object:
    with open(file_name, 'rb') as file:
        return  pickle.load(file)