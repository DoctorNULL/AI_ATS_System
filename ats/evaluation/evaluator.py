from sentence_transformers import SentenceTransformer
from ..config import ATSConfig
from ..cv.base import CV
from ..requriement.base import JobRequirement
from ..job_title_info import JobTitles

class ATSEvaluator(object):
    def __init__(self, encoder: str, config: ATSConfig = None):
        self.model = SentenceTransformer(encoder, trust_remote_code=True)
        self.jobs = JobTitles(self.model)

        if config:
            self.config = config
        else:
            self.config = ATSConfig()

    def _score_text(self, text1: str, text2: str) -> float:
        embedding1 = self.model.encode([text1])
        embedding2 = self.model.encode([text2])

        return self.model.similarity(embedding1, embedding2)[0].item()

    def _score_text_list(self, base: list[str], candidates: list[str]) -> float:
        embedding1 = self.model.encode(base)
        embedding2 = self.model.encode(candidates)

        return self.model.similarity(embedding1, embedding2).topk(1, -1).values.mean().item()

    def _max_score_text_list(self, base: list[str], candidates: list[str]) -> float:
        embedding1 = self.model.encode(base)
        embedding2 = self.model.encode(candidates)

        return self.model.similarity(embedding1, embedding2).max().item()

    def _score_skills(self, required: list[str], cv: CV) -> float:
        plain_text = []

        for skill in required:
            plain_text += skill.split()

        score = sum([x in cv["Skills"] for x in plain_text]) / len(plain_text)

        sum_score = sum([x in cv["Summary"] for x in required]) / len(required)

        exp_score = 0

        for exp in cv["Experience"]:
            for detail in exp["Details"]:
                exp_score += sum([x in detail for x in required]) / (len(cv["Experience"]) + len(required))


        pro_score = 0

        for exp in cv["Projects"]:
            for detail in exp["Details"]:
                pro_score += sum([x in detail for x in required]) / (len(cv["Projects"]) + len(required))

        exp_score = min([1, exp_score])
        pro_score = min([1, pro_score])
        score = min([1, score + sum_score])

        return score * 0.25 + exp_score * 0.4 + pro_score * 0.35



    def _score_requirements(self, requirements: list[str], cv: CV) -> float:
        candidates = []
        c = 3

        for exp in cv["Experience"]:
            candidates += exp["Details"]

        score = self._score_text_list(requirements, candidates)

        candidates = []

        for exp in cv["Projects"]:
            candidates += exp["Details"]

        pro_sem = self._score_text_list(requirements, candidates)

        if round(pro_sem, 2) > 0.5:
            score += pro_sem
            c += 1

        candidates = []

        for exp in cv["Publications"]:
            candidates += exp["Details"]

        if candidates:
            pub_sem = self._max_score_text_list(requirements, candidates)

            if round(pub_sem, 2) > 0.5:
                score += pub_sem * 2
                c += 1

        score += self._max_score_text_list(requirements, [x["Title"] for x in cv["Education"]])

        score += self._max_score_text_list(requirements, cv["Summary"])

        return min([1, score / c])

    def evaluate(self, cv: CV, requirements: JobRequirement) -> tuple[float, dict[str, float]]:
        title_score = self._score_text(cv["Title"], requirements["Title"])
        field_score = self._score_text(self.jobs.job_filed(cv["Title"]), requirements["Field"])

        work_exp_score = 0
        years = 0
        for experience in cv["Experience"]:
            if experience["Title"] == requirements["Title"]:
                work_exp_score += self.config.jop_relevancy_Score
                years += ((0.5 if experience["End"] == experience["Start"] else 0) +
                          (1 if experience["End"] == "present" else 0) + int(experience.get("End", "0")[-1:-4]) - int(experience.get("Start", "0")[-1:-4]))

        work_exp_score /= len(cv["Experience"])
        if years >= requirements["ProficiencyYears"]:
            years = years - requirements["ProficiencyYears"] + 1 / 5
        else:
            years = 0

        summary_score = self._score_text_list(requirements["Summary"], cv["Summary"])

        candidates = []

        for detail in cv["Experience"]:
            candidates += detail["Details"]

        responsibilities_score = self._score_text_list(requirements["Responsibilities"], candidates)

        requirements_score = self._score_requirements(requirements["Requirements"], cv)

        skills_score = self._score_skills(requirements["Skills"], cv)

        return round(((title_score * 0.1 + field_score * 0.3 + work_exp_score * 0.6) * self.config.title_weight +
                responsibilities_score * self.config.responsibilities_weight
                + years * self.config.proficiency_weight + summary_score * self.config.summary_weight +
                requirements_score * self.config.requirements_weight + skills_score * self.config.skills_weight),2) * 100, {
            "Title": round(title_score * 0.1 + field_score * 0.3 + work_exp_score * 0.6, 2) * 100,
            "Summary": round(summary_score, 2) * 100,
            "Requirements": round(requirements_score, 2) * 100,
            "Responsibilities": round(responsibilities_score, 2) * 100,
            "Years": years * 100,
            "Skills": round(skills_score, 2) * 100
        }