from .base import CV, CourseInfo, ProjectInfo, PublicationInfo, ExperienceInfo, EducationInfo

def print_courses(courses: list[CourseInfo]):
    for course in courses:
        print("-" * 20)
        print(course["Title"])
        print(course["Institution"])

        if course.get("Location", ""):
            print(course["Location"])

        if course.get("Start", "") and course.get("End", ""):
            print(f"{course["Start"]} - {course["End"]}")
        elif course.get("End", ""):
            print(course["End"])

        print("\n".join(course["Details"]))
        print("-" * 20)

def print_experience(experience: list[ExperienceInfo]):
    for experience in experience:
        print("-" * 20)
        print(experience["Title"])
        print(experience["Company"])

        if experience.get("Start", "") and experience.get("End", ""):
            print(f"{experience["Start"]} - {experience["End"]}")
        elif experience.get("End", ""):
            print(experience["End"])

        print("\n".join(experience["Details"]))
        print("-" * 20)

def print_cv(cv: CV):
    print(cv["Name"])
    print(cv["Title"])
    print(f"Email : {cv["Email"]} - Phone : {cv["Phone"]}" + f" - Location : {cv["Location"]}" if cv.get("Location", "") else "")

    if cv["Summary"]:
        print("\n\nSummary\n")
        print("\n".join(cv["Summary"]))

    if cv["Skills"]:
        print("\n\nSkills\n")
        print(" - ".join(cv["Skills"]))

    if cv["Languages"]:
        print("\n\nLanguages\n")
        print(" - ".join(cv["Languages"]))

    if cv["Experience"]:
        print("\n\nExperience\n")
        print_experience(cv["Experience"])

    if cv["Courses"]:
        print("\n\nCourses\n")
        print_courses(cv["Courses"])