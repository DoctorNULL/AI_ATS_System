class ParserConfig:
    def __init__(self,
                 text_spliter_chunk_size = 150,
                 text_spliter_chunk_overlap = 50,
                 text_similarity_threshold = 0.9,
                 title_similarity_threshold = 0.85
                 ):

        self.text_spliter_chunk_size = text_spliter_chunk_size
        self.text_spliter_chunk_overlap = text_spliter_chunk_overlap
        self.text_similarity_threshold = text_similarity_threshold
        self.title_similarity_threshold = title_similarity_threshold

'''
ATS Configration contains a list of parameters for the evaluations of ATS Scoring System

:param
title_weight: Evaluation of jop title score
summary_weight: Evaluation of summary section score
proficiency_weight: Evaluation of proficiency years
responsibilities_weight: Evaluation of responsibility score
requirements_weight: Evaluation of requirements score
skills_weight: Evaluation of skills score

jop_relevancy_score: Score that controls how work experience is relevant to job title
'''
class ATSConfig:
    def __init__(self,
                 title_weight = 0.025,
                 proficiency_weight = 0.05,
                 summary_weight = 0.1,
                 responsibilities_weight = 0.175,
                 requirements_weight = 0.35,
                 skills_weight = 0.3,

                 jop_relevancy_score = 1
                 ):

        assert sum([title_weight, summary_weight, proficiency_weight,
                    responsibilities_weight, requirements_weight, skills_weight]) == 1, "All weights must sum to 1"

        self.title_weight = title_weight
        self.summary_weight = summary_weight
        self.proficiency_weight = proficiency_weight
        self.responsibilities_weight = responsibilities_weight
        self.requirements_weight = requirements_weight
        self.skills_weight = skills_weight

        self.jop_relevancy_Score = jop_relevancy_score

    def __str__(self):
        return (f"Title {self.title_weight}, Proficiency {self.proficiency_weight}"
                f", Summary {self.summary_weight}, Responsibilities {self.responsibilities_weight}"
                f", Requirement {self.requirements_weight}, Skills {self.skills_weight}")

