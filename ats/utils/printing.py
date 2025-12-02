from ats.cv.base import CV, CourseInfo, ProjectInfo, PublicationInfo, ExperienceInfo, EducationInfo

def print_courses(courses: list[CourseInfo]):
    for course in courses:
        print(course["Title"])
        print(course["Institution"])

        if course.get("Start", "") and course.get("End", ""):
            print(f"{course["Start"]} - {course["End"]}")
        elif course.get("End", ""):
            print(course["End"])

        print("\n".join(course["Details"]))
        print("\n" * 2)

def print_experience(experiences: list[ExperienceInfo]):
    for experience in experiences:
        print(experience["Title"])
        print(experience["Company"])

        if experience.get("Start", "") and experience.get("End", ""):
            print(f"{experience["Start"]} - {experience["End"]}")
        elif experience.get("End", ""):
            print(experience["End"])

        print("\n".join(experience["Details"]))
        print("\n" * 2)

def print_project(projects: list[ProjectInfo]):
    for experience in projects:
        print(experience["Title"])

        if experience.get("Start", "") and experience.get("End", ""):
            print(f"{experience["Start"]} - {experience["End"]}")
        elif experience.get("End", ""):
            print(experience["End"])

        print("\n".join(experience["Details"]))
        print("\n" * 2)

def print_publication(publications: list[PublicationInfo]):
    for publication in publications:
        print(publication["Title"])

        if publication.get("Date", ""):
            print(publication["Date"])

        print("\n".join(publication["Details"]))
        print("\n" * 2)

def print_education(educations: list[EducationInfo]):
    for education in educations:
        print(education["Title"])
        print(education["Location"])

        if education.get("Start", "") and education.get("End", ""):
            print(f"{education["Start"]} - {education["End"]}")
        elif education.get("End", ""):
            print(education["End"])

        print("\n" * 2)

def print_cv(cv: CV):
    print(cv["Name"])
    print(cv["Title"])
    print(f"Email : {cv["Email"]} - Phone : {cv["Phone"]}" + f" - Location : {cv["Location"]}" if cv.get("Location", "") else "")

    if cv["Summary"]:
        print("Summary")
        print("-" * 50)
        print("\n".join(cv["Summary"]))

    if cv["Education"]:
        print("Education")
        print("-" * 50)
        print_education(cv["Education"])

    if cv["Skills"]:
        print("Skills")
        print("-" * 50)
        print(" - ".join(cv["Skills"]))

    if cv["Languages"]:
        print("Languages")
        print("-" * 50)
        print(" - ".join(cv["Languages"]))

    if cv["Experience"]:
        print("Experience")
        print("-" * 50)
        print_experience(cv["Experience"])

    if cv["Projects"]:
        print("Projects")
        print("-" * 50)
        print_project(cv["Projects"])

    if cv["Publications"]:
        print("Publications")
        print("-" * 50)
        print_publication(cv["Publications"])

    if cv["Courses"]:
        print("Courses")
        print("-" * 50)
        print_courses(cv["Courses"])