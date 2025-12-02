from sentence_transformers import SentenceTransformer

from .base import RequirementSection


class RequirementInfo:
    Sections = {
        RequirementSection.Summary : [
            "Job Summary",
            "Role Summary",
            "Position Summary",
            "Overview",
            "Job Overview",
            "Position Overview",
            "Role Overview",
            "Summary of the Role",
            "Summary of the Position",
            "About the Role",
            "About the Position",
            "Role Description",
            "Position Description",
            "Job Description Summary",
            "Job Brief",
            "Role Brief",
            "Position Brief",
            "Brief Summary",
            "Summary",
            "Introduction",
            "Job Introduction",
            "Role Introduction",
            "Position Introduction",
            "Purpose of the Role",
            "Role Purpose",
            "Position Purpose",
            "Mission of the Role",
            "Key Role Summary",
            "Key Position Summary",
            "Career Summary",
            "Job Snapshot",
            "Position Snapshot",
            "Role Snapshot",
            "At-a-Glance",
            "Executive Summary",
            "Overview of Responsibilities",
            "Role Highlights",
            "Position Highlights",
            "Job Highlights",
            "Summary Statement",
            "Job Profile",
            "Position Profile",
            "Role Profile",
            "Profile Summary",
            "General Summary",
            "Essential Summary"
        ],
        RequirementSection.Responsibilities : [
            "Key Responsibilities",
            "Responsibilities",
            "Role Responsibilities",
            "Job Responsibilities",
            "Primary Responsibilities",
            "Main Responsibilities",
            "Core Responsibilities",
            "Duties and Responsibilities",
            "Position Responsibilities",
            "Accountabilities",
            "Role Accountabilities",
            "Key Accountabilities",
            "Core Duties",
            "Main Duties",
            "Job Duties",
            "Position Duties",
            "Responsibilities Overview",
            "What You’ll Do",
            "What You Will Do",
            "Tasks and Responsibilities",
            "Essential Duties",
            "Core Functions",
            "Primary Duties",
            "Areas of Responsibility",
            "Scope of Role",
            "Role Scope",
            "Responsibilities Summary",
            "Key Tasks",
            "Principal Responsibilities",
            "Responsibilities and Duties",
            "Major Responsibilities",
            "Responsibilities and Accountabilities",
            "Core Tasks",
            "Task Overview",
            "Job Functions",
            "Operational Responsibilities",
            "Functional Responsibilities",
            "Role Objectives",
            "Your Responsibilities",
            "Key Deliverables",
            "Main Tasks",
            "Daily Responsibilities",
            "Typical Duties",
            "Accountability Areas",
            "Role Duties",
            "Work Responsibilities"
        ],

        RequirementSection.Requirements: [
            "Qualifications",
            "Job Requirements",
            "Requirements",
            "Role Requirements",
            "Position Requirements",
            "Candidate Requirements",
            "Must-Have Skills",
            "Essential Qualifications",
            "Minimum Qualifications",
            "Minimum Requirements",
            "Eligibility Criteria",
            "Required Skills",
            "Required Experience",
            "Prerequisites",
            "Education and Experience",
            "Professional Requirements",
            "Role Qualifications",
            "Position Qualifications",
            "Knowledge, Skills, and Abilities",
            "KSA (Knowledge, Skills, Abilities)",
            "Experience Requirements",
            "Job Criteria",
            "Skill Requirements",
            "Mandatory Skills",
            "Credentials",
            "Core Competencies",
            "Eligibility Requirements"
        ],

        RequirementSection.Skills : [
            "Preferred Qualifications",
            "Preferred Skills",
            "Nice-to-Have Skills",
            "Desirable Skills",
            "Optional Skills",
            "Additional Qualifications",
            "Bonus Skills",
            "Extra Skills",
            "Advantageous Skills",
            "Helpful Skills",
            "Preferred Experience",
            "Desirable Experience",
            "Preferred Attributes",
            "Nice-to-Have Qualifications",
            "Extra Qualifications",
            "Additional Skills",
            "Complementary Skills",
            "Preferred Competencies",
            "Preferred Knowledge",
            "Desirable Competencies"
        ],

        RequirementSection.AboutUs : [
            "Preferred Qualifications",
            "Preferred Skills",
            "Nice-to-Have Skills",
            "Desirable Skills",
            "Optional Skills",
            "Additional Qualifications",
            "Bonus Skills",
            "Extra Skills",
            "Advantageous Skills",
            "Helpful Skills",
            "Preferred Experience",
            "Desirable Experience",
            "Preferred Attributes",
            "Nice-to-Have Qualifications",
            "Extra Qualifications",
            "Additional Skills",
            "Complementary Skills",
            "Preferred Competencies",
            "Preferred Knowledge",
            "Desirable Competencies"
        ]

    }

    def __init__(self, encoder: str):
        self.model = SentenceTransformer(encoder, trust_remote_code=True)

        self._encodes = {}

        for key in self.Sections:
            self._encodes[key] = self.model.encode(self.Sections[key])

    def find_section(self, title: str, threshold = 0.85) -> RequirementSection:
        encoded = self.model.encode([title])
        best = (RequirementSection.Unknown, 0)
        for key in self._encodes:
            score = self.model.similarity(encoded,self._encodes[key])[0].max().item()

            #print(f"{key} : {score}")

            if score > best[1]:
                best = (key, score)

        if best[1] >= threshold:
            return best[0]

        return RequirementSection.Unknown
