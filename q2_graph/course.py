"""
course.py
Domain/entity class representing a single university course.
"""


class Course:
    LEVELS = ("core", "elective")

    def __init__(self, code: str, name: str, credit_hours: int,
                 level: str, year: int, lecturer: str, description: str = ""):
        if level not in self.LEVELS:
            raise ValueError("level must be 'core' or 'elective'")
        self.code = code.upper()          # unique id, e.g. "CS201"
        self.name = name
        self.credit_hours = int(credit_hours)
        self.level = level                # core / elective
        self.year = int(year)             # year of study it is offered
        self.lecturer = lecturer
        self.description = description

    # Courses are identified by their code, so two Course objects with the
    # same code are treated as the same vertex in the graph.
    def __eq__(self, other):
        return isinstance(other, Course) and self.code == other.code

    def __hash__(self):
        return hash(self.code)

    def __lt__(self, other):            # allows sorted() on Course lists
        return self.code < other.code

    def __repr__(self):
        return f"Course({self.code})"

    def short(self):
        return f"{self.code} ({self.name})"

    def full_details(self):
        return (f"  Course Code  : {self.code}\n"
                f"  Course Name  : {self.name}\n"
                f"  Credit Hours : {self.credit_hours}\n"
                f"  Level        : {self.level.capitalize()}\n"
                f"  Year Offered : {self.year}\n"
                f"  Lecturer     : {self.lecturer}\n"
                f"  Description  : {self.description}")

    def profile(self):
        """Visibility-aware profile: electives only reveal their name."""
        if self.level == "elective":
            return (f"  Course Name  : {self.name}\n"
                    f"  (Elective course - other details are hidden)")
        return self.full_details()
