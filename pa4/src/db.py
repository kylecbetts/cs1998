from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

instructors_table = db.Table(
    "instructors",
    db.Column("course_id", db.Integer, db.ForeignKey("courses.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"))
)

students_table = db.Table(
    "students",
    db.Column("course_id", db.Integer, db.ForeignKey("courses.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"))
)

# your classes here
class Course(db.Model):
    """
    Course model for CMS classroom manager.

    Has a one-to-many relationship with the Assignment model.
    Has a many-to-many relationship with the User model.
    """
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    assignments = db.relationship("Assignment", cascade="delete")
    instructors = db.relationship("User", secondary=instructors_table, back_populates="instructor")
    students = db.relationship("User", secondary=students_table, back_populates="student")


    def __init__(self, **kwargs):
        """
        Initializes a Course object.
        """
        self.code = kwargs.get("code", "")
        self.name = kwargs.get("name", "")


    def serialize(self):
        """
        Serializes a Course object.
        """
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "assignments": [a.simple_serialize() for a in self.assignments],
            "instructors": [i.simple_serialize() for i in self.instructors],
            "students": [s.simple_serialize() for s in self.students]
        }

    def simple_serialize(self):
        """
        Serializes a Course object without instructors, students, assignments.
        """
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name
        }


class User(db.Model):
    """
    User model for CMS classroom manager.
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False)
    instructor = db.relationship("Course", secondary=instructors_table, back_populates="instructors")
    student = db.relationship("Course", secondary=students_table, back_populates="students")


    def __init__(self, **kwargs):
        """
        Initializes a User object.
        """
        self.name = kwargs.get("name", "")
        self.netid = kwargs.get("netid", "")


    def get_all_courses(self):
        """
        Returns a list of the users student and instructor courses.
        """
        courses = []
        for i in self.instructor:
            courses.append(i.simple_serialize())
        for s in self.student:
            courses.append(s.simple_serialize())
        return courses

    
    def serialize(self):
        """
        Serializes a User object.
        """
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid,
            "courses": self.get_all_courses()
        }


    def simple_serialize(self):
        """
        Serializes a User object without courses.
        """
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid
        }


class Assignment(db.Model):
    """
    Assignment model for CMS classroom manager.
    """
    __tablename__ = "assignments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    due_date = db.Column(db.Integer, nullable=False)
    course = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)


    def __init__(self, **kwargs):
        """
        Initializes Assignment object.
        """
        self.title = kwargs.get("title", "")
        self.due_date = kwargs.get("due_date")
        self.course = kwargs.get("course")


    def serialize(self):
        """
        Serializes Assignment object.
        """
        return {
            "id": self.id,
            "title": self.title,
            "due_date": self.due_date,
            "course": self.course
        }

    
    def simple_serialize(self):
        """
        Serializes Assignment object without course.
        """
        return {
            "id": self.id,
            "title": self.title,
            "due_date": self.due_date
        }
