from typing import TypedDict, NotRequired
from enum import Enum


class CVSection(Enum):
    UnKnown = 0
    Education = 1
    Experience = 2
    Courses = 3
    Publication = 4
    Language = 5
    Skills = 6
    Summary = 7
    Projects = 8


class EducationInfo(TypedDict):
    Title: str
    Start: NotRequired[str]
    End: NotRequired[str]
    Location: str

class ExperienceInfo(TypedDict):
    Title: str
    Start: NotRequired[str]
    End: NotRequired[str]
    Company: str
    Details: list[str]

class PublicationInfo(TypedDict):
    Title: str
    Publishers: list[str]
    Date: NotRequired[str]
    Details: list[str]

class CourseInfo(TypedDict):
    Title: str
    Institution: str
    Location: NotRequired[str]
    Start: NotRequired[str]
    End: NotRequired[str]
    Details: list[str]

class ProjectInfo(TypedDict):
    Title: str
    Start: NotRequired[str]
    End: NotRequired[str]
    Details: list[str]

class CV(TypedDict):
    Name: str
    Title: str
    Email: str
    Phone: str
    Location: NotRequired[str]
    Summary: list[str]
    Education: list[EducationInfo]
    Experience: list[ExperienceInfo]
    Languages: list[str]
    Skills: list[str]
    Publications: list[PublicationInfo]
    Courses: list[CourseInfo]
    Projects: list[ProjectInfo]