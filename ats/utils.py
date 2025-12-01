from .base import CV, CourseInfo, ProjectInfo, PublicationInfo, ExperienceInfo, EducationInfo

def print_courses(courses: list[CourseInfo]):
    for course in courses:
        print("-" * 20)
        print(course["Title"])
        print(course["Institution"])

        if course.get("Start", "") and course.get("End", ""):
            print(f"{course["Start"]} - {course["End"]}")
        elif course.get("End", ""):
            print(course["End"])

        print("\n".join(course["Details"]))
        print("-" * 20)

def print_experience(experiences: list[ExperienceInfo]):
    for experience in experiences:
        print("-" * 20)
        print(experience["Title"])
        print(experience["Company"])

        if experience.get("Start", "") and experience.get("End", ""):
            print(f"{experience["Start"]} - {experience["End"]}")
        elif experience.get("End", ""):
            print(experience["End"])

        print("\n".join(experience["Details"]))
        print("-" * 20)

def print_project(projects: list[ProjectInfo]):
    for experience in projects:
        print("-" * 20)
        print(experience["Title"])

        if experience.get("Start", "") and experience.get("End", ""):
            print(f"{experience["Start"]} - {experience["End"]}")
        elif experience.get("End", ""):
            print(experience["End"])

        print("\n".join(experience["Details"]))
        print("-" * 20)

def print_publication(publications: list[PublicationInfo]):
    for publication in publications:
        print("-" * 20)
        print(publication["Title"])

        if publication.get("Date", ""):
            print(publication["Date"])

        print("\n".join(publication["Details"]))
        print("-" * 20)

def print_education(educations: list[EducationInfo]):
    for education in educations:
        print("-" * 20)
        print(education["Title"])
        print(education["Location"])

        if education.get("Start", "") and education.get("End", ""):
            print(f"{education["Start"]} - {education["End"]}")
        elif education.get("End", ""):
            print(education["End"])

        print("-" * 20)

def print_cv(cv: CV):
    print(cv["Name"])
    print(cv["Title"])
    print(f"Email : {cv["Email"]} - Phone : {cv["Phone"]}" + f" - Location : {cv["Location"]}" if cv.get("Location", "") else "")

    if cv["Summary"]:
        print("\n\nSummary\n")
        print("\n".join(cv["Summary"]))

    if cv["Education"]:
        print("\n\nEducation\n")
        print_education(cv["Education"])

    if cv["Skills"]:
        print("\n\nSkills\n")
        print(" - ".join(cv["Skills"]))

    if cv["Languages"]:
        print("\n\nLanguages\n")
        print(" - ".join(cv["Languages"]))

    if cv["Experience"]:
        print("\n\nExperience\n")
        print_experience(cv["Experience"])

    if cv["Projects"]:
        print("\n\nProjects\n")
        print_project(cv["Projects"])

    if cv["Publications"]:
        print("\n\nPublications\n")
        print_publication(cv["Publications"])

    if cv["Courses"]:
        print("\n\nCourses\n")
        print_courses(cv["Courses"])