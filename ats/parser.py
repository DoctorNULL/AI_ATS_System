from .base import ProjectInfo, PublicationInfo, ExperienceInfo, EducationInfo, CourseInfo, CV, CVSection
from .section_info import SectionInfo
from .config import ATSConfig
from .job_title_info import JobTitles
import validators
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re

def get_line(data: list[str]) -> str:
    if not data:
        return ""

    val = data[0]
    data.pop(0)

    return val


class CVParser(object):
    def __init__(self, encoder: str, config: ATSConfig = None):
        self.sections = SectionInfo(encoder)
        self.job_titles = JobTitles(encoder)

        if not config:
            self.config = ATSConfig()
        else:
            self.config = config

        self.special_words_pattern = r"\w*[\\\./@!$#+%&]+\w*"
        self.date_pattern = r"((0[1-9]|[12]\d|3[01])/(0[1-9]|1[0-2])/(19|20)\d{2}|(0[1-9]|1[0-2])/(19|20)\d{2}|(19|20)\d{2})"
        self.present_keywords = [
            "present",
            "current",
            "ongoing",
            "to date",
            "until now",
            "still employed",
            "continuing",
            "in progress",
            "now",
            "today",
            "present day",
            "active",
            "active role",
            "current role",
            "current position",
            "current employment",
            "through present",
            "through current date",
            "up to current",
            "up to the present",
            "up to this date"
        ]

    def _get_section(self, data:list[str], section_seperator = " <line> ") -> str:
        section = ""
        line = get_line(data)

        while self.sections.find_section(line) == CVSection.UnKnown and line:
            section += line + section_seperator
            line = get_line(data)

        data.insert(0, line)

        return section

    def _parse_base_info(self, data: list[str]) -> dict[str, str]:

        result = {
            "Name": get_line(data),
            "Title": get_line(data),
            "Email": "",
            "Phone": ""
        }
        line = get_line(data)

        section = self.sections.find_section(line)

        if section != CVSection.UnKnown:
            data.insert(0, line)
        else:
            vals = line.split()

            for val in vals:
                if validators.email(val):
                    result["Email"] = val
                elif val.isnumeric() or val.startswith("+"):
                    result["Phone"] = val
                elif val.isalpha() and not "Location" in result.keys():
                    result["Location"] = val

        return result

    def _parse_summary(self, data: list[str]) -> list[str]:

        result = []

        section = self._get_section(data)

        spliter = RecursiveCharacterTextSplitter(
            chunk_size= self.config.text_spliter_chunk_size,
            chunk_overlap= self.config.text_spliter_chunk_overlap
        )

        result += spliter.split_text(section)

        return result

    def _parse_education(self, data: list[str]) -> list[EducationInfo]:
        result : list[EducationInfo] = []

        education_title_keywords = [
            "bachelor", "bachelors", "bachelor's", "degree", "ba.", "b.a", "bsc", "b.sc",
            "bs.", "b.s", "beng", "b.eng", "btech", "b.tech", "bba", "b.com", "bcom.",
            "master", "masters", "master's", "ma.", "m.a", "msc.", "m.sc",
            "ms.", "m.s", "meng.", "m.eng", "mba.", "mphil.",
            "phd.", "ph.d", "dphil.", "doctorate", "doctoral",
            "diploma", "advanced", "graduate",
            "postgraduate", "certification", "certificate", "certified",
            "course", "completion",
        ]

        institution_keywords = [
            "university", "college", "institute", "school", "academy",
            "polytechnic", "high", "secondary", "senior", "secondary",
        ]

        section = self._get_section(data)

        section = section.split()

        section = [x.strip() for x in section]

        line = ""
        isText = True

        section_lines = []

        for i, word in enumerate(section):
            if word == "<line>" and line:
                section_lines.append(line.strip())
                line = ""
                isText = True
            else:
                try:
                    maybe_present3 = " ".join(section[i:i+3])
                except:
                    maybe_present3 = word
                try:
                    maybe_present2 = " ".join(section[i:i+3])
                except:
                    maybe_present2 = word

                if (word.isnumeric() or word.lower() in self.present_keywords
                        or maybe_present2.lower() in self.present_keywords or maybe_present3.lower() in self.present_keywords or
                        (not word.isalnum() and len(word.strip()) == 1)):
                    if line and isText:
                        section_lines.append(line.strip())
                        line = ""

                    isText = False
                else:
                    if not isText and line:
                        section_lines.append(line.strip())
                        line = ""

                    isText = True

                line += word + " "

        current_title = ""
        current_start = ""
        current_location = ""
        current_end = ""

        for line in section_lines:
            if any([x in line.lower() for x in education_title_keywords]):
                if current_title and current_location:
                    x : EducationInfo = {
                        "Title": current_title,
                        "Location": current_location
                    }

                    if current_start:
                        x["Start"] = current_start

                    if current_end:
                        x["End"] = current_end

                    result.append(x)
                    current_start = ""
                    current_location = ""
                    current_end = ""

                current_title = line

            elif any([x in line.lower() for x in institution_keywords]):
                    current_location = line
            elif line.isnumeric():
                current_end = line
            elif len(line.split()) == 3:
                x = line.split()
                current_start = x[0]
                current_end = x[2]
            elif line.lower() in self.present_keywords:
                current_end = line

        if current_title and current_location:
            x : EducationInfo = {
                "Title": current_title,
                "Location": current_location
            }

            if current_start:
                x["Start"] = current_start

            if current_end:
                x["End"] = current_end

            result.append(x)

        return result

    def _parse_experience(self, data:list[str]) -> list[ExperienceInfo]:
        result : list[ExperienceInfo] = []

        section = self._get_section(data)

        section = section.split()

        section = [x.strip() for x in section]

        line = ""
        lines = []
        for word in section:
            if word.isalpha():
                line += word + " "
            elif word[:-1].isalpha():
                line += word[:-1] + " " + word[-1]
            else:
                if line:
                    lines.append(line.strip())
                    line = ""

                lines.append(word)
        if line:
            lines.append(line)

        spliter = RecursiveCharacterTextSplitter(
            chunk_size= self.config.text_spliter_chunk_size,
            chunk_overlap= self.config.text_spliter_chunk_overlap
        )

        current_title = ""
        current_start = ""
        current_end = ""
        current_detail = ""
        current_company = ""

        skip_counter = 0
        for i, line in enumerate(lines):

            if skip_counter:
                skip_counter -= 1
                continue

            title = self.job_titles.find_title(line, self.config.title_similarity_threshold)

            if title:

                if current_title and current_company:
                    x : ExperienceInfo = {
                        "Title": current_title,
                        "Company": current_company,
                        "Details": spliter.split_text(current_detail)
                    }

                    if current_end:
                        x["End"] = current_end

                    if current_start:
                        x["Start"] = current_start

                    result.append(x)
                    current_start = ""
                    current_end = ""
                    current_company = ""
                    current_detail = ""

                current_title = title
            elif line == "<line>":
                continue
            else:
                if current_title:
                    if line in self.present_keywords:
                        current_end = line
                    elif (not current_company and (line.replace(",", "").replace(".", "").replace(" ", "").isalpha()
                                                  or re.fullmatch(self.special_words_pattern, line))
                          and not re.fullmatch(self.date_pattern, line) and not line in self.present_keywords):
                        current_company = line
                    elif (line.replace("\"", "").replace("'", "").replace(" ", "").isalpha()
                          or line[:-1].replace("\"", "").replace("'", "").replace(" ", "").isalpha()):
                        current_detail += line + " "
                    elif re.fullmatch(self.date_pattern, line):
                        try:
                            if re.fullmatch(self.date_pattern, lines[i + 2]) or lines[i + 2] in self.present_keywords:
                                current_start = line
                                current_end = lines[i + 2]
                                skip_counter = 2
                        except:
                            pass

        if current_title and current_company:
            x : ExperienceInfo = {
                "Title": current_title,
                "Company": current_company,
                "Details": spliter.split_text(current_detail)
            }

            if current_end:
                x["End"] = current_end

            if current_start:
                x["Start"] = current_start

            result.append(x)

        return result

    def _parse_project(self, data:list[str]) -> list[ProjectInfo]:
        result : list[ProjectInfo] = []

        section = self._get_section(data)

        section = section.split()

        section = [x.strip() for x in section]

        line = ""
        lines = []
        for word in section:
            if word.isalpha():
                line += word + " "
            elif word[:-1].isalpha():
                line += word[:-1] + " " + word[-1]
            elif re.fullmatch(self.special_words_pattern, word):
                line += word + " "
            else:
                if line:
                    lines.append(line.strip())
                    line = ""

                lines.append(word)
        if line:
            lines.append(line)

        spliter = RecursiveCharacterTextSplitter(
            chunk_size= self.config.text_spliter_chunk_size,
            chunk_overlap= self.config.text_spliter_chunk_overlap
        )

        current_title = ""
        current_start = ""
        current_end = ""
        current_detail = ""

        skip_counter = 0
        for i, line in enumerate(lines):

            if skip_counter:
                skip_counter -= 1
                continue

            if (line.istitle()
                    or all([word.isupper() or word[0].isupper() for word in line.split()])):

                if current_title:
                    x : ProjectInfo = {
                        "Title": current_title,
                        "Details": spliter.split_text(current_detail)
                    }

                    if current_end:
                        x["End"] = current_end

                    if current_start:
                        x["Start"] = current_start

                    result.append(x)
                    current_start = ""
                    current_end = ""
                    current_detail = ""

                current_title = line
            elif line == "<line>":
                continue
            else:
                if current_title:
                    if line in self.present_keywords:
                        current_end = line
                    elif re.fullmatch(self.date_pattern, line):
                        try:
                            if re.fullmatch(self.date_pattern, lines[i + 2]) or lines[i + 2] in self.present_keywords:
                                current_start = line
                                current_end = lines[i + 2]
                                skip_counter = 2
                        except:
                            pass
                    else:
                        current_detail += line + " "

        if current_title:
            x : ProjectInfo = {
                "Title": current_title,
                "Details": spliter.split_text(current_detail)
            }

            if current_end:
                x["End"] = current_end

            if current_start:
                x["Start"] = current_start

            result.append(x)

        return result

    def _parse_publications(self, data:list[str]) -> list[PublicationInfo]:
        result : list[PublicationInfo] = []

        section = self._get_section(data)

        section = section.split()

        section = [x.strip() for x in section]

        line = ""
        lines = []
        for word in section:
            if word.isalpha():
                line += word + " "
            elif word[:-1].isalpha():
                line += word[:-1] + " " + word[-1]
            elif re.fullmatch(self.special_words_pattern, word):
                line += word + " "
            else:
                if line:
                    lines.append(line.strip())
                    line = ""

                lines.append(word)
        if line:
            lines.append(line)

        spliter = RecursiveCharacterTextSplitter(
            chunk_size= self.config.text_spliter_chunk_size,
            chunk_overlap= self.config.text_spliter_chunk_overlap
        )

        current_title = ""
        current_date = ""
        publishers = ""
        current_detail = ""

        skip_counter = 0
        for i, line in enumerate(lines):

            if skip_counter:
                skip_counter -= 1
                continue

            if (line.istitle()
                    or all([word.isupper() or word[0].isupper() for word in line.split()])):

                if current_title:
                    x : PublicationInfo = {
                        "Title": current_title,
                        "Publishers": publishers,
                        "Details": spliter.split_text(current_detail)
                    }

                    if current_date:
                        x["Date"] = current_date

                    result.append(x)
                    publishers = ""
                    current_date = ""
                    current_detail = ""

                current_title = line
            elif line == "<line>":
                continue
            else:
                if current_title:
                    if line in self.present_keywords:
                        current_date = line
                    elif re.fullmatch(self.date_pattern, line):
                        current_date = line
                    elif not publishers and all([word.isupper() or word.istitle for word in line.split(",")]):
                        publishers = line
                    else:
                        current_detail += line + " "

        if current_title:
            x : PublicationInfo = {
                "Title": current_title,
                "Publishers": publishers,
                "Details": spliter.split_text(current_detail)
            }

            if current_date:
                x["Date"] = current_date

            result.append(x)

        return result

    def _parse_courses(self, data:list[str]) -> list[CourseInfo]:
        result : list[CourseInfo] = []

        section = self._get_section(data)

        section = section.split()

        section = [x.strip() for x in section]

        line = ""
        lines = []
        for word in section:
            if word.isalpha():
                line += word + " "
            elif word[:-1].isalpha():
                line += word[:-1] + " " + word[-1]
            elif re.fullmatch(self.special_words_pattern, word):
                line += word + " "
            else:
                if line:
                    lines.append(line.strip())
                    line = ""

                lines.append(word)
        if line:
            lines.append(line)

        spliter = RecursiveCharacterTextSplitter(
            chunk_size= self.config.text_spliter_chunk_size,
            chunk_overlap= self.config.text_spliter_chunk_overlap
        )

        current_title = ""
        current_start = ""
        current_end = ""
        institution = ""
        current_detail = ""

        skip_counter = 0
        for i, line in enumerate(lines):

            if skip_counter:
                skip_counter -= 1
                continue

            if (line.istitle()
                    or all([word.isupper() or word[0].isupper() for word in line.split()])):

                if current_title and institution:
                    x : CourseInfo = {
                        "Title": current_title,
                        "Institution": institution,
                        "Details": spliter.split_text(current_detail)
                    }

                    if current_start:
                        x["Start"] = current_start

                    if current_end:
                        x["End"] = current_end

                    result.append(x)
                    institution = ""
                    current_start = ""
                    current_end = ""
                    current_detail = ""

                current_title = line
            elif line == "<line>":
                continue
            else:
                if current_title:
                    if line in self.present_keywords:
                        current_end = line
                    elif re.fullmatch(self.date_pattern, line):
                        try:
                            if re.fullmatch(self.date_pattern, lines[i + 2]) or lines[i + 2] in self.present_keywords:
                                current_start = line
                                current_end = lines[i + 2]
                                skip_counter = 2
                        except:
                            pass
                    elif not institution:
                        institution = line
                    else:
                        current_detail += line + " "

        if current_title and institution:
            x : CourseInfo = {
                "Title": current_title,
                "Institution": institution,
                "Details": spliter.split_text(current_detail)
            }

            if current_start:
                x["Start"] = current_start

            if current_end:
                x["End"] = current_end

            result.append(x)

        return result

    def _parse_list(self, data: list[str]) -> list[str]:
        result = []

        section = self._get_section(data, " ")

        result += section.split()

        return result

    def parse_cv(self, data: str) -> CV:
        current_data = data.splitlines()
        base_info = self._parse_base_info(current_data)

        summary : list[str] = []
        education : list[EducationInfo] = []
        skills : list[str] = []
        langs : list[str] = []
        experience : list[ExperienceInfo] = []
        projects : list[ProjectInfo] = []
        publications : list[PublicationInfo] = []
        courses : list[CourseInfo] = []

        line = get_line(current_data)

        while current_data:
            section = self.sections.find_section(line)
            match section:

                case CVSection.Summary:
                    summary = self._parse_summary(current_data)

                case CVSection.Education:
                    education = self._parse_education(current_data)

                case CVSection.Skills:
                    skills = self._parse_list(current_data)

                case CVSection.Language:
                    langs = self._parse_list(current_data)

                case CVSection.Experience:
                    experience = self._parse_experience(current_data)

                case CVSection.Projects:
                    projects = self._parse_project(current_data)

                case CVSection.Publication:
                    publications = self._parse_publications(current_data)

                case CVSection.Courses:
                    courses = self._parse_courses(current_data)


            line = get_line(current_data)

        result : CV = {
            "Name": base_info["Name"],
            "Title": base_info["Title"],
            "Email": base_info["Email"],
            "Phone": base_info["Phone"],
            "Summary": summary,
            "Courses": courses,
            "Education": education,
            "Experience": experience,
            "Languages": langs,
            "Projects": projects,
            "Publications": publications,
            "Skills": skills
        }

        if "Location" in base_info.keys():
            result["Location"] = base_info["Location"]

        return result