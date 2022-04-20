import json
from flask import Flask, request
import db
import os
import hashlib

DB = db.DatabaseDriver()

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello world!"


# your routes here
@app.route("/api/users/")
def get_users():
    """
    Endpoint for getting all users.
    """
    return json.dumps({"users": DB.get_all_users()}), 200


@app.route("/api/users/", methods=["POST"])
def create_user():
    """
    Endpoint for creating a new user.

    Throws a 400 error if there is no request body, or the request body does 
    not contain a name or username. balance field is optional and is set to 
    0 if none is provided.
    """
    if not request.data :
        return json.dumps({"error": "No body provided."}), 400
    body = json.loads(request.data)

    name = body.get("name")
    if not name:
        return json.dumps({"error": "No name provided."}), 400
    username = body.get("username")
    if not username:
        return json.dumps({"error": "No username provided."}), 400
    balance = body.get("balance", 0)

    user_id = DB.insert_users_table(name, username, balance)
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "Something went wrong while creating user"}), 404
    return json.dumps(user), 201


@app.route("/api/extra/users/", methods=["POST"])
def create_user_extra():
    """
    Endpoint for creating a new user with a password.

    Throws a 400 error if there is no request body, or the request body does 
    not contain a name, username, or password. balance field is optional and is 
    set to 0 if none is provided.
    """
    if not request.data :
        return json.dumps({"error": "No body provided."}), 400
    body = json.loads(request.data)

    name = body.get("name")
    if not name:
        return json.dumps({"error": "No name provided."}), 400
    username = body.get("username")
    if not username:
        return json.dumps({"error": "No username provided."}), 400
    password = body.get("password")
    if not password:
        return json.dumps({"error": "No password provided."}), 400
    balance = body.get("balance", 0)

    hashed_password = hash_password(password)
    user_id = DB.insert_users_table(name, username, balance, hashed_password)
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "Something went wrong while creating user"}), 404
    user["password"] = password
    return json.dumps(user), 201


@app.route("/api/user/<int:user_id>/")
def get_user(user_id):
    """
    Endpoint for getting the user with user_id.

    Throws a 404 error if no user with user_id exists.
    """
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "User not found"}), 404
    return json.dumps(user), 200


@app.route("/api/extra/user/<int:user_id>/", methods=["POST"])
def get_user_extra(user_id):
    """
    Endpoint for getting the user with user_id.

    Throws a 404 error if no user with user_id exists. Throws a 400 error if 
    there is no request body, or the request body does not contain a password. 
    Throws a 401 error if the password does not belong to the user.
    """
    if not request.data :
        return json.dumps({"error": "No body provided."}), 400
    body = json.loads(request.data)

    password = body.get("password")
    if not password:
        return json.dumps({"error": "No password provided."}), 400

    correct_hash = DB.get_user_password_by_id(user_id)
    if correct_hash is None:
        return json.dumps({"error": "User not found"}), 404

    hash = hash_password(password)
    if hash != correct_hash:
        return json.dumps({"error": "Incorrect password."}), 401

    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "User not found"}), 404
    user["password"] = password
    return json.dumps(user), 200


@app.route("/api/user/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    """
    Endpoint for deleting a user with user_id.

    Throws a 404 error if no user with user_id exists.
    """
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "User not found"}), 404
    DB.delete_user_by_id(user_id)
    return json.dumps(user), 200


@app.route("/api/send/", methods=["POST"])
def send_money():
    """
    Endpoint for sending money from one user to another.

    Throws a 400 error if there is no request body, or the request body does 
    not contain a sender_id, receiver_id or amount.
    """
    if not request.data :
        return json.dumps({"error": "No body provided."}), 400
    body = json.loads(request.data)

    sender_id = body.get("sender_id")
    if sender_id is None:
        return json.dumps({"error": "No sender_id provided."}), 400
    receiver_id = body.get("receiver_id")
    if receiver_id is None:
        return json.dumps({"error": "No receiver_id provided."}), 400
    amount = body.get("amount")
    if amount is None:
        return json.dumps({"error": "No amount provided."}), 400

    sender = DB.get_user_by_id(sender_id)
    if sender is None:
        return json.dumps({"error": "Sender not found"}), 404
    receiver = DB.get_user_by_id(receiver_id)
    if receiver is None:
        return json.dumps({"error": "Receiver not found"}), 404

    if amount > sender.get("balance"):
        return json.dumps({"error": "Insufficient funds"}), 400
    DB.update_user_balance_by_id(sender_id, sender.get("balance") - amount)
    DB.update_user_balance_by_id(receiver_id, receiver.get("balance") + amount)

    return json.dumps(body), 200


@app.route("/api/extra/send/", methods=["POST"])
def send_money_extra():
    """
    Endpoint for sending money from one user to another.

    Throws a 400 error if there is no request body, or the request body does 
    not contain a sender_id, receiver_id, amount, or password. Throws a 401 
    error if the password does not belong to the user.
    """
    if not request.data :
        return json.dumps({"error": "No body provided."}), 400
    body = json.loads(request.data)

    sender_id = body.get("sender_id")
    if sender_id is None:
        return json.dumps({"error": "No sender_id provided."}), 400
    receiver_id = body.get("receiver_id")
    if receiver_id is None:
        return json.dumps({"error": "No receiver_id provided."}), 400
    amount = body.get("amount")
    if amount is None:
        return json.dumps({"error": "No amount provided."}), 400
    password = body.pop("password", None)
    if password is None:
        return json.dumps({"error": "No password provided."}), 400

    correct_hash = DB.get_user_password_by_id(sender_id)
    if correct_hash is None:
        return json.dumps({"error": "Sender not found"}), 404

    hash = hash_password(password)
    if hash != correct_hash:
        return json.dumps({"error": "Incorrect password."}), 401

    sender = DB.get_user_by_id(sender_id)
    if sender is None:
        return json.dumps({"error": "Sender not found"}), 404
    receiver = DB.get_user_by_id(receiver_id)
    if receiver is None:
        return json.dumps({"error": "Receiver not found"}), 404

    if amount > sender.get("balance"):
        return json.dumps({"error": "Insufficient funds"}), 400
    DB.update_user_balance_by_id(sender_id, sender.get("balance") - amount)
    DB.update_user_balance_by_id(receiver_id, receiver.get("balance") + amount)

    return json.dumps(body), 200


def hash_password(password):
    """
    Takes password, adds salt to the start of it and hashes it numerous times.
    """
    password = os.environ['PASSWORD_SALT'] + password
    password = password.encode('ascii')
    for i in range(int(os.environ['NUMBER_OF_ITERATIONS'])):
        m = hashlib.sha256()
        m.update(password)
        password = m.digest()
    hash = m.hexdigest()
    return hash


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
