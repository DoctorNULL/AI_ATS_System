from typing import TypedDict
from enum import Enum


class RequirementSection(Enum):
    Unknown = 0
    Summary = 1
    Responsibilities = 2
    Requirements = 3
    Skills = 4
    AboutUs = 5

class JobRequirement(TypedDict):
    ProficiencyYears: int
    Field: str
    Title: str
    Summary: list[str]
    Responsibilities: list[str]
    Requirements: list[str]
    Skills: list[str]
