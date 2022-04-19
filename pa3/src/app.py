from datetime import datetime
import json

import db
from flask import Flask
from flask import request
from flask import Response

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
    user_transactions = DB.get_transactions_by_user(user_id)
    if user_transactions is None:
        return json.jumps({"error": "Something went wrong while creating user"}), 404
    user["transactions"] = user_transactions
    return json.dumps(user), 201


@app.route("/api/users/<int:user_id>/")
def get_user(user_id):
    """
    Endpoint for getting the user with user_id.

    Throws a 404 error if no user with user_id exists.
    """
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "User not found"}), 404
    user_transactions = DB.get_transactions_by_user(user_id)
    if user_transactions is None:
        return json.jumps({"error": "Something went wrong while getting a user"}), 404
    user["transactions"] = user_transactions
    return json.dumps(user), 200


@app.route("/api/users/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    """
    Endpoint for deleting a user with user_id.

    Throws a 404 error if no user with user_id exists.
    """
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "User not found"}), 404
    user_transactions = DB.get_transactions_by_user(user_id)
    if user_transactions is None:
        return json.jumps({"error": "Something went wrong deleting the user"}), 404
    user["transactions"] = user_transactions
    DB.delete_user_by_id(user_id)
    return json.dumps(user), 200


@app.route("/api/transactions/", methods=["POST"])
def create_transaction():
    """
    Endpoint for sending money from one user to another.

    Throws a 400 error if there is no request body, or the request body does 
    not contain a sender_id, receiver_id, amount, or message. accepted field 
    is optional, and should be set to true if provided. Throws a 403 error 
    if there are insufficient funds.
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
    message = body.get("message")
    if message is None:
        return json.dumps({"error": "No message provided."}), 400
    accepted = body.get("accepted")

    sender = DB.get_user_by_id(sender_id)
    if sender is None:
        return json.dumps({"error": "Sender not found"}), 404
    receiver = DB.get_user_by_id(receiver_id)
    if receiver is None:
        return json.dumps({"error": "Receiver not found"}), 404

    if accepted == True:
        if amount > sender.get("balance"):
            return json.dumps({"error": "Insufficient funds"}), 403
        DB.update_user_balance_by_id(sender_id, sender.get("balance") - amount)
        DB.update_user_balance_by_id(receiver_id, receiver.get("balance") + amount)
        tx_id = DB.insert_transactions_table(sender_id, receiver_id, amount, message, True)
    else:
        tx_id = DB.insert_transactions_table(sender_id, receiver_id, amount, message)

    tx = DB.get_transaction_by_id(tx_id)
    return json.dumps(tx), 201


@app.route("/api/transactions/<int:tx_id>/", methods=["POST"])
def update_transaction(tx_id):
    """
    Endpoint for updating the accepted status of a transaction.

    Throws a 400 error if there is no request body, or the request body does 
    not contain an accepted field. Throws a 403 error if there are insufficient 
    funds or the transaction accepted status is already true / false.
    """
    if not request.data :
        return json.dumps({"error": "No body provided."}), 400
    body = json.loads(request.data)

    accepted = body.get("accepted")
    if accepted is None:
        return json.dumps({"error": "No accepted provided."}), 400

    tx = DB.get_transaction_by_id(tx_id)
    current_status = tx.get("accepted")
    if current_status is not None:
        return json.dumps({"error": "Transaction already final."}), 403

    DB.update_transaction_accepted_by_id(tx_id, accepted)

    if accepted == True:
        sender_id = tx.get("sender_id")
        receiver_id = tx.get("receiver_id")
        amount = tx.get("amount")

        sender = DB.get_user_by_id(sender_id)
        if sender is None:
            return json.dumps({"error": "Sender not found"}), 404
        receiver = DB.get_user_by_id(receiver_id)
        if receiver is None:
            return json.dumps({"error": "Receiver not found"}), 404

        if amount > sender.get("balance"):
            return json.dumps({"error": "Insufficient funds"}), 403
        DB.update_user_balance_by_id(sender_id, sender.get("balance") - amount)
        DB.update_user_balance_by_id(receiver_id, receiver.get("balance") + amount)

    tx = DB.get_transaction_by_id(tx_id)
    return json.dumps(tx), 200


@app.route("/api/extra/users/<int:user_id>/friends/")
def get_user_friends(user_id):
    """
    Endpoint for getting the user's friends.

    Throws a 404 error if no user with user_id exists.
    """
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "User not found"}), 404
    return json.dumps({"friends": DB.get_friends_by_user(user_id)}), 200


@app.route("/api/extra/users/<int:user1>/friends/<int:user2>/", methods=["POST"])
def create_friendship(user1, user2):
    """
    Endpoint for creating a friendship between user1 and user2.
    """
    id = DB.insert_friends_table(user1, user2)
    return Response(status=201)


@app.route("/api/extra/users/<int:user_id>/join/")
def get_user_transactions(user_id):
    """
    Endpoint for getting the user's transactions.
    """
    return json.dumps({"transactions": DB.get_transactions_by_user_join(user_id)}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
