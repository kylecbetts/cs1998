import sqlite3
from datetime import datetime

# From: https://goo.gl/YzypOI
def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance

class DatabaseDriver(object):
    """
    Database driver for the Venmo (Full) app.
    Handles with reading and writing data with the database.
    """

    def __init__(self):
        self.conn = sqlite3.connect("venmo.db", check_same_thread=False)
        self.create_users_table()
        self.create_transactions_table()
        self.create_friends_table()

    
    def create_users_table(self):
        """
        Using SQL, creates a users table
        """
        try:
            self.conn.execute(
                """
                    CREATE TABLE users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        username TEXT NOT NULL,
                        balance INT NOT NULL
                    );
                """
            )
        except Exception as e:
            print(e)


    def create_transactions_table(self):
        """
        Using SQL, creates a transactions table
        """
        try:
            self.conn.execute(
                """
                    CREATE TABLE transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        sender_id INTEGER SECONDARY KEY NOT NULL,
                        receiver_id INTEGER SECONDARY KEY NOT NULL,
                        amount INTEGER NOT NULL,
                        message TEXT NOT NULL,
                        accepted INTEGER
                    );
                """
            )
        except Exception as e:
            print(e)


    def create_friends_table(self):
        """
        Using SQL, creates a friends table
        """
        try:
            self.conn.execute(
                """
                    CREATE TABLE friends (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user1 INTEGER SECONDARY KEY NOT NULL,
                        user2 INTEGER SECONDARY KEY NOT NULL
                    );
                """
            )
        except Exception as e:
            print(e)


    def delete_users_table(self):
        """
        Using SQL, deletes the users table
        """
        self.conn.execute("DROP TABLE IF EXISTS users;")

    
    def delete_transactions_table(self):
        """
        Using SQL, deletes the transactions table
        """
        self.conn.execute("DROP TABLE IF EXISTS transactions;")

    
    def delete_friends_table(self):
        """
        Using SQL, deletes the friends table
        """
        self.conn.execute("DROP TABLE IF EXISTS friends;")


    def get_all_users(self):
        """
        Using SQL, gets all users in the users table
        """
        cursor = self.conn.execute("SELECT id, name, username FROM users;")
        users = []
        for row in cursor:
            users.append({"id": row[0], "name": row[1], "username": row[2]})
        return users


    def insert_users_table(self, name, username, balance):
        """
        Using SQL, adds a new user in the users table
        """
        cursor = self.conn.execute("INSERT INTO users (name, username, balance) VALUES (?, ?, ?);", (name, username, balance))
        self.conn.commit()
        return cursor.lastrowid


    def get_user_by_id(self, id):
        """
        Using SQL, gets a user by its id
        """
        cursor = self.conn.execute("SELECT * FROM users WHERE id=?;", (id,))
        for row in cursor:
            return {"id": row[0], "name": row[1], "username": row[2], "balance": row[3]}
        return None

    
    def delete_user_by_id(self, id):
        """
        Using SQL, deletes a user by id
        """
        self.conn.execute("DELETE FROM users WHERE id=?;", (id,))
        self.conn.commit()


    def update_user_balance_by_id(self, id, balance):
        """
        Using SQL, updates the balance a user by id
        """
        self.conn.execute("UPDATE users SET balance=? WHERE id=?;", (balance, id))
        self.conn.commit()

    
    def insert_transactions_table(self, sender_id, receiver_id, amount, message, accepted=None):
        """
        Use SQLite3 to create new transaction.
        """
        timestamp = datetime.now()
        if accepted == True:
            cursor = self.conn.execute("INSERT INTO transactions (timestamp, sender_id, receiver_id, amount, message, accepted) VALUES (?, ?, ?, ?, ?, ?);", (timestamp, sender_id, receiver_id, amount, message, accepted))
        else:
            cursor = self.conn.execute("INSERT INTO transactions (timestamp, sender_id, receiver_id, amount, message) VALUES (?, ?, ?, ?, ?);", (timestamp, sender_id, receiver_id, amount, message))
        self.conn.commit()
        return cursor.lastrowid

    
    def get_transaction_by_id(self, id):
        """
        Using SQL, gets a transaction by id
        """
        cursor = self.conn.execute("SELECT * FROM transactions WHERE id = ?", (id,))
        for row in cursor:
            if row[6] is None:
                accepted = None
            else:
                accepted = bool(row[6])
            return {
                "id": row[0],
                "timestamp": row[1],
                "sender_id": row[2],
                "receiver_id": row[3],
                "amount": row[4],
                "message": row[5],
                "accepted": accepted
            }
        return None

    
    def get_transactions_by_user(self, user_id):
        """
        Using SQL, get all transactions for a user with id user_id
        """
        cursor = self.conn.execute("SELECT * FROM transactions WHERE sender_id=? OR receiver_id=?;", (user_id, user_id))
        transactions = []
        for row in cursor:
            if row[6] is None:
                accepted = None
            else:
                accepted = bool(row[6])
            transactions.append({
                "id": row[0],
                "timestamp": row[1],
                "sender_id": row[2],
                "receiver_id": row[3],
                "amount": row[4],
                "message": row[5],
                "accepted": accepted
            })
        return transactions


    def get_transactions_by_user_join(self, user_id):
        """
        Using SQL, get all transactions for a user with id user_id
        """
        cursor = self.conn.execute("""
        SELECT u1.name, u2.name, t.timestamp, t.amount, t.message, t.accepted 
        FROM transactions t INNER JOIN users u1 ON t.sender_id=u1.id 
        INNER JOIN users u2 ON t.receiver_id=u2.id
        WHERE t.sender_id=? OR t.receiver_id=?;""", (user_id, user_id))
        transactions = []
        for row in cursor:
            if row[5] is None:
                accepted = None
            else:
                accepted = bool(row[5])
            transactions.append({
                "sender_name": row[0],
                "receiver_name": row[1],
                "timestamp": row[2],
                "amount": row[3],
                "message": row[4],
                "accepted": accepted
            })
        return transactions

    
    def update_transaction_accepted_by_id(self, id, accepted):
        """
        Using SQL, updates the balance a user by id
        """
        self.conn.execute("UPDATE transactions SET accepted=? WHERE id=?;", (accepted, id))
        self.conn.commit()

    
    def insert_friends_table(self, user1, user2):
        """
        Using SQL, adds a new friend pair to the friends table
        """
        cursor = self.conn.execute("INSERT INTO friends (user1, user2) VALUES (?, ?);", (user1, user2))
        self.conn.commit()
        return cursor.lastrowid

    
    def get_friends_by_user(self, user_id):
        """
        Using SQL, get all friends for a user with id user_id
        """
        cursor = self.conn.execute("SELECT * FROM friends WHERE user1=? OR user2=?;", (user_id, user_id))
        friends = []
        for row in cursor:
            friend_id = row[1]
            if friend_id == user_id:
                friend_id = row[2]
            friend = self.get_user_by_id(friend_id)
            del friend["balance"]
            friends.append(friend)
        return friends

    
# Only <=1 instance of the database driver
# exists within the app at all times
DatabaseDriver = singleton(DatabaseDriver)   
