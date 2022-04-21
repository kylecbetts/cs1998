import json
import os

from db import db
from db import Course
from db import User
from db import Assignment

from flask import Flask
from flask import request

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

def success_response(data, code=200):
    return json.dumps(data), code

def failure_response(message, code=404):
    return json.dumps({"error": message}), code


@app.route("/")
def welcome():
    """
    Endpoint for sending welcome message.
    """
    return str(os.environ.get("NETID")) + " was here!"


# your routes here
@app.route("/api/courses/")
def get_courses():
    """
    Endpoint for getting all courses.
    """
    return success_response({"courses": [c.serialize() for c in Course.query.all()]})


@app.route("/api/courses/", methods=["POST"])
def create_course():
    """
    Endpoint for creating a new course.
    """
    body = json.loads(request.data)
    code = body.get("code")
    if code is None:
        return failure_response({"error": "No code provided."}, 400)
    name = body.get("name")
    if name is None:
        return failure_response({"error": "No name provided."}, 400)
    
    new_course = Course(code=code, name=name)
    db.session.add(new_course)
    db.session.commit()
    return success_response(new_course.serialize(), 201)


@app.route("/api/courses/<int:course_id>/")
def get_course(course_id):
    """
    Endpoint for getting a course by id.
    """
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Course not found.")
    return success_response(course.serialize())


@app.route("/api/courses/<int:course_id>/", methods=["DELETE"])
def delete_course(course_id):
    """
    Endpoint for deleting a course by id.
    """
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Course not found.")
    db.session.delete(course)
    db.session.commit()
    return success_response(course.serialize())


@app.route("/api/users/", methods=["POST"])
def create_user():
    """
    Endpoint for creating a new user.
    """
    body = json.loads(request.data)
    name = body.get("name")
    if name is None:
        return failure_response({"error": "No name provided."}, 400)
    netid = body.get("netid")
    if netid is None:
        return failure_response({"error": "No netid provided."}, 400)
    new_user = User(name=name, netid=netid)
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)


@app.route("/api/users/<int:user_id>/")
def get_user(user_id):
    """
    Endpoint for getting a user by id.
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found.")
    return success_response(user.serialize())


@app.route("/api/courses/<int:course_id>/add/", methods=["POST"])
def add_user_to_course(course_id):
    """
    Endpoint for adding a user to a course.
    """
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Course not found.")
    
    body = json.loads(request.data)
    user_id = body.get("user_id")
    if user_id is None:
        return failure_response({"error": "No user_id provided."}, 404)
    type = body.get("type")
    if type is None:
        return failure_response({"error": "No type provided."}, 404)

    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found.")

    if type == "student":
        course.students.append(user)
    elif type == "instructor":
        course.instructors.append(user)
    db.session.commit()
    return success_response(course.serialize())


@app.route("/api/courses/<int:course_id>/assignment/", methods=["POST"])
def create_assignment(course_id):
    """
    Endpoint for creating a new assignment.
    """
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Course not found.")

    body = json.loads(request.data)
    title = body.get("title")
    if title is None:
        return failure_response({"error": "No title provided."}, 400)
    due_date = body.get("due_date")
    if due_date is None:
        return failure_response({"error": "No due_date provided."}, 400)

    assignment = Assignment(
        title=title,
        due_date=due_date,
        course=course_id
    )
    db.session.add(assignment)
    db.session.commit()
    assignment = assignment.serialize()
    assignment["course"] = course.simple_serialize()
    return success_response(assignment, 201)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
