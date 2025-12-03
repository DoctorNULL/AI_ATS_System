from sentence_transformers import SentenceTransformer
from .section_info import RequirementInfo
from .base import JobRequirement, RequirementSection
from ..job_title_info import JobTitles
from ..skills_info import SkillsInfo
from ..utils.common import get_line
from ..config import ParserConfig
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter

class RequirementParser(object):
    def __init__(self, encoder: str, config: ParserConfig = None):
        self.model = SentenceTransformer(encoder, trust_remote_code=True)

        self.info = RequirementInfo(self.model)
        self.skills = SkillsInfo()

        if config:
            self.config = config
        else:
            self.config = ParserConfig()

        self.spliter = RecursiveCharacterTextSplitter(chunk_size= self.config.text_spliter_chunk_size,
                                                      chunk_overlap= self.config.text_spliter_chunk_overlap)

    def _find_section(self, data: list[str]) -> list[str]:
        line = get_line(data)
        res = []
        while self.info.find_section(line, self.config.title_similarity_threshold) == RequirementSection.Unknown and data:

            if line:
                res.append(line)

            line = get_line(data)

        data.insert(0, line)
        return res

    def _parse_section(self, data: list[str]) -> list[str]:
        section = self._find_section(data)

        res = []

        for text in section:
            res += self.spliter.split_text(text)

        return res

    def parse_requirement(self, text: list[str]) -> JobRequirement:

        line = get_line(text)

        if "title:" not in line.lower().replace(" ", ""):
            raise Exception("Title : <Jop Title Required> should be the first line")

        titles = JobTitles(self.model)
        title = line.split(":")[1]
        title = titles.find_title(title, self.config.title_similarity_threshold)
        field = titles.job_filed(title)
        years = 0

        years_regex = r"\d\+? (year)(s)?"
        matches = re.search(years_regex, " ".join(text))

        if matches:
            years = int(matches.group().split()[0].replace("+", ""))

        line = get_line(text)

        summary = []
        skills = self.skills.find_in_text(text)
        requirements = []
        responsibilities = []

        while text:
            section = self.info.find_section(line, self.config.title_similarity_threshold)

            match section:
                case RequirementSection.Summary:
                    summary = self._parse_section(text)

                case RequirementSection.Requirements:
                    requirements = self._find_section(text)

                case RequirementSection.Responsibilities:
                    responsibilities = self._parse_section(text)

            line = get_line(text)


        return {
            "Title": title,
            "Summary": summary,
            "ProficiencyYears": years,
            "Skills": skills,
            "Requirements": requirements,
            "Responsibilities": responsibilities,
            "Field": field
        }