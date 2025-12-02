from sentence_transformers import SentenceTransformer
from ats.cv.base import CVSection

class SectionInfo(object):

    Sections = {
        CVSection.Summary : [
            "Professional Summary",
            "Career Summary",
            "Executive Summary",
            "Profile",
            "Professional Profile",
            "Career Profile",
            "Summary Statement",
            "Personal Summary",
            "Personal Profile",
            "Overview",
            "Professional Overview",
            "Career Overview",
            "About Me",
            "Highlights",
            "Qualification Summary",
            "Summary of Qualifications",
            "Key Qualifications",
            "Key Strengths",
            "Career Highlights",
            "Professional Highlights"
        ],

        CVSection.Education : [
            "Education",
            "Academic Background",
            "Educational Background",
            "Academic Qualifications",
            "Educational Qualifications",
            "Qualifications",
            "Scholastic Background",
            "Academic History",
            "Education & Training",
            "Training & Education",
            "Professional Education",
            "Formal Education",
            "Academic Profile",
            "Studies",
            "Coursework",
            "Academic Record",
            "Education Summary",
            "Scholarly Credentials",
            "Learning Path",
            "Academic Achievements"
        ],

        CVSection.Experience : [
            "Professional Experience",
            "Work Experience",
            "Employment History",
            "Professional History",
            "Career History",
            "Work History",
            "Experience",
            "Relevant Experience",
            "Industry Experience",
            "Career Experience",
            "Professional Background",
            "Employment Experience",
            "Job History",
            "Work Background",
            "Career Summary",
            "Professional Summary",
            "Career Profile",
            "Professional Record",
            "Occupational History",
            "Work Portfolio"
        ],

        CVSection.Language : [
            "Languages",
            "Language Skills",
            "Linguistic Skills",
            "Language Proficiency",
            "Spoken Languages",
            "Language Competencies",
            "Language Abilities",
            "Language Knowledge",
            "Multilingual Skills",
            "Language Fluency",
            "Communication Languages"
        ],

        CVSection.Skills : [
        "Skills",
        "Key Skills",
        "Core Skills",
        "Technical Skills",
        "Professional Skills",
        "Core Competencies",
        "Competencies",
        "Areas of Expertise",
        "Expertise",
        "Relevant Skills",
        "Skill Set",
        "Technical Competencies",
        "Professional Competencies",
        "Capabilities",
        "Strengths",
        "Professional Strengths",
        "Qualifications & Skills"
        ],

        CVSection.Projects : [
            "Projects",
            "Professional Projects",
            "Academic Projects",
            "Key Projects",
            "Selected Projects",
            "Project Experience",
            "Notable Projects",
            "Project Highlights",
            "Research & Projects",
            "Project Work",
            "Practical Projects",
            "Major Projects",
            "Relevant Projects",
            "Portfolio Projects",
            "Independent Projects"
        ],
        CVSection.Courses : [
            "Courses",
            "Relevant Courses",
            "Coursework",
            "Academic Courses",
            "Professional Courses",
            "Training Courses",
            "Completed Courses",
            "Certifications & Courses",
            "Educational Courses",
            "Specialized Courses",
            "Core Courses",
            "Selected Courses",
            "Continuing Education",
            "Professional Development Courses",
            "Online Courses"
        ],
        CVSection.Publication : [
            "Publications",
            "Research Publications",
            "Academic Publications",
            "Scholarly Publications",
            "Articles",
            "Papers",
            "Research Papers",
            "Peer-Reviewed Publications",
            "Journal Publications",
            "Conference Publications",
            "Published Work",
            "Written Work",
            "Scientific Publications",
            "Books & Publications",
            "Selected Publications"
        ]
    }

    def __init__(self, encoder: str):
        self.model = SentenceTransformer(encoder, trust_remote_code=True)

        self._encodes = {}

        for key in self.Sections:
            self._encodes[key] = self.model.encode(self.Sections[key])

    def find_section(self, title: str, threshold = 0.85) -> CVSection:
        encoded = self.model.encode([title])
        best = (CVSection.UnKnown, 0)
        for key in self._encodes:
            score = self.model.similarity(encoded,self._encodes[key])[0].max().item()

            #print(f"{key} : {score}")

            if score > best[1]:
                best = (key, score)

        if best[1] >= threshold:
            return best[0]

        return CVSection.UnKnown
