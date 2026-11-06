"""
course_system.py
University Course Prerequisite System (menu-driven, command line).

Uses the generic Graph class. An edge  A -> B  means
"A is a prerequisite of B" (completing A unlocks B), therefore:
  * prerequisites of B  = incoming adjacent vertices of B
  * courses unlocked by A = outgoing adjacent vertices of A

Run:  python course_system.py
"""
from course import Course
from graph import Graph


# ---------------------------------------------------------------------- #
# Initial data: 8 course profiles (min 5, max 10 required)
# ---------------------------------------------------------------------- #
def load_courses():
    return [
        Course("CS101", "Introduction to Programming", 4, "core", 1, "Dr. Tan Wei Ming",
               "Basic programming concepts using Python."),
        Course("MA101", "Discrete Mathematics", 3, "core", 1, "Dr. Siti Aminah",
               "Logic, sets, relations, functions and graph basics."),
        Course("CS201", "Data Structures", 4, "core", 2, "Mr. Raj Kumar",
               "Lists, stacks, queues, trees and hash tables."),
        Course("CS202", "Object-Oriented Programming", 4, "core", 2, "Ms. Lee Mei Ling",
               "Classes, inheritance, polymorphism and design."),
        Course("CS301", "Algorithms", 4, "core", 3, "Dr. Wong Kar Fai",
               "Algorithm design, complexity analysis and graphs."),
        Course("CS302", "Database Systems", 3, "core", 3, "Dr. Nurul Huda",
               "Relational model, SQL and normalisation."),
        Course("CS350", "Mobile App Development", 3, "elective", 3, "Mr. Daniel Lim",
               "Building Android applications."),
        Course("CS401", "Software Engineering", 4, "core", 4, "Prof. Ahmad Faizal",
               "Software process, requirements, testing and teamwork."),
    ]


# (prerequisite, course) pairs -> edge prerequisite -> course
PREREQUISITES = [
    ("CS101", "CS201"), ("MA101", "CS201"),
    ("CS101", "CS202"),
    ("CS201", "CS301"), ("MA101", "CS301"),
    ("CS201", "CS302"),
    ("CS202", "CS350"),
    ("CS202", "CS401"), ("CS302", "CS401"),
]

MAX_COURSES = 10


class CourseSystem:
    """Domain layer: connects Course objects to the generic Graph."""

    def __init__(self):
        self.graph = Graph()
        self.catalogue = {}            # course code -> Course (fast lookup)

    def add_course(self, course):
        if course.code in self.catalogue:
            raise ValueError(f"{course.code} already exists")
        if len(self.catalogue) >= MAX_COURSES:
            raise ValueError(f"maximum of {MAX_COURSES} courses reached")
        self.catalogue[course.code] = course
        self.graph.addVertex(course)

    def find(self, code):
        return self.catalogue.get(code.strip().upper())

    def prerequisites_of(self, course):
        return sorted(self.graph.listIncomingAdjacentVertex(course))

    def unlocked_by(self, course):
        return sorted(self.graph.listOutgoingAdjacentVertex(course))

    def add_prerequisite(self, course, prereq):
        """Make `prereq` a prerequisite of `course` (edge prereq -> course)."""
        if course == prereq:
            return "A course cannot be a prerequisite of itself."
        if self.graph.hasEdge(prereq, course):
            return f"{prereq.code} is already a prerequisite of {course.code}."
        # If course already leads to prereq, the new edge would make a cycle
        # (no student could ever register for either course).
        if self.graph.hasPath(course, prereq):
            return (f"Rejected: {course.code} is already required (directly or "
                    f"indirectly) before {prereq.code}; this would create a cycle.")
        self.graph.addEdge(prereq, course)
        return f"{prereq.code} added as a prerequisite of {course.code}."

    def remove_prerequisite(self, course, prereq):
        if self.graph.removeEdge(prereq, course):
            return f"{prereq.code} removed from the prerequisites of {course.code}."
        return f"{prereq.code} is not a prerequisite of {course.code}."


def build_system():
    system = CourseSystem()
    for c in load_courses():
        system.add_course(c)
    for pre, course in PREREQUISITES:
        system.graph.addEdge(system.find(pre), system.find(course))
    return system


# ---------------------------------------------------------------------- #
# User interface helpers
# ---------------------------------------------------------------------- #
def ask_course(system, prompt="Enter Course Code: "):
    code = input(prompt).strip().upper()
    course = system.find(code)
    if course is None:
        print(f"Course '{code}' not found. Use option 1 to see valid codes.")
    return course


def print_course_list(title, courses, empty_msg):
    print(title)
    if not courses:
        print(f"  {empty_msg}")
    for c in courses:
        print(f"  - {c.short()}")


# ---------------------------------------------------------------------- #
# Mandatory features
# ---------------------------------------------------------------------- #
def view_all(system):
    print("\nAvailable Courses:")
    for i, c in enumerate(system.catalogue.values(), 1):
        print(f"{i:>2}. {c.code} - {c.name}")


def view_details(system):
    course = ask_course(system)
    if course:
        print(f"\nFull details of {course.code}:")
        print(course.full_details())


def view_prerequisites(system):
    course = ask_course(system)
    if course:
        print_course_list(f"Prerequisites for {course.code} - {course.name}:",
                          system.prerequisites_of(course),
                          "None (this is an entry-level course).")


def view_unlocked(system):
    course = ask_course(system)
    if course:
        print_course_list(f"Courses unlocked by {course.code} - {course.name}:",
                          system.unlocked_by(course),
                          "None (no course requires it).")


# ---------------------------------------------------------------------- #
# Advanced features
# ---------------------------------------------------------------------- #
def add_course_on_demand(system):
    if len(system.catalogue) >= MAX_COURSES:
        print(f"Cannot add: the system holds a maximum of {MAX_COURSES} courses.")
        return
    code = input("New Course Code: ").strip().upper()
    if not code or system.find(code):
        print("Invalid or duplicate course code.")
        return
    name = input("Course Name: ").strip() or "Untitled"
    try:
        credits = int(input("Credit Hours: "))
        year = int(input("Year Offered (1-4): "))
    except ValueError:
        print("Credit hours and year must be whole numbers.")
        return
    level = input("Level (core/elective): ").strip().lower()
    if level not in Course.LEVELS:
        print("Level must be 'core' or 'elective'.")
        return
    lecturer = input("Lecturer: ").strip() or "TBA"
    desc = input("Description: ").strip()
    system.add_course(Course(code, name, credits, level, year, lecturer, desc))
    print(f"Course {code} added as a new vertex. Total courses: {len(system.catalogue)}")


def view_profile(system):
    course = ask_course(system)
    if course:
        print(f"\nProfile ({course.level}):")
        print(course.profile())


def add_prereq_on_demand(system):
    course = ask_course(system, "Course X (the course that needs a prerequisite): ")
    if not course:
        return
    prereq = ask_course(system, "Course Y (prerequisite to add): ")
    if prereq:
        print(system.add_prerequisite(course, prereq))


def remove_prereq_on_demand(system):
    course = ask_course(system, "Course X: ")
    if not course:
        return
    print_course_list("Current prerequisites:", system.prerequisites_of(course), "None.")
    prereq = ask_course(system, "Course Y (prerequisite to remove): ")
    if prereq:
        print(system.remove_prerequisite(course, prereq))


MENU = [
    ("View All Courses", view_all),
    ("View Course Details", view_details),
    ("View Prerequisites of a Course", view_prerequisites),
    ("View Courses Unlocked by a Course", view_unlocked),
    ("Add a New Course", add_course_on_demand),
    ("View Course Profile (core/elective visibility)", view_profile),
    ("Add a Prerequisite to a Course", add_prereq_on_demand),
    ("Remove a Prerequisite from a Course", remove_prereq_on_demand),
]


def main():
    system = build_system()
    exit_no = len(MENU) + 1
    while True:
        print("\n==== University Course Prerequisite System ====")
        for i, (label, _) in enumerate(MENU, 1):
            print(f"{i}. {label}")
        print(f"{exit_no}. Exit")
        choice = input("Enter choice: ").strip()
        if choice == str(exit_no):
            print("Exiting program. Goodbye!")
            break
        if choice.isdigit() and 1 <= int(choice) <= len(MENU):
            print()
            MENU[int(choice) - 1][1](system)
        else:
            print(f"Invalid choice, please enter 1-{exit_no}.")


if __name__ == "__main__":
    main()
