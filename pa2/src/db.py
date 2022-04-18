import os
import sqlite3

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
    Database driver for the venmo app.
    Handles with reading and writing data with the database.
    """
    def __init__(self):
        self.conn = sqlite3.connect("venmo.db", check_same_thread=False)
        self.create_users_table()


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
                        balance INT NOT NULL,
                        password TEXT
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

    
    def get_all_users(self):
        """
        Using SQL, gets all users in the users table
        """
        cursor = self.conn.execute("SELECT id, name, username FROM users;")
        users = []
        for row in cursor:
            users.append({"id": row[0], "name": row[1], "username": row[2]})
        return users

    
    def insert_users_table(self, name, username, balance, password=None):
        """
        Using SQL, adds a new user in the users table
        """
        if password is not None:
            cursor = self.conn.execute("INSERT INTO users (name, username, balance, password) VALUES (?, ?, ?, ?);", (name, username, balance, password))
        else:
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

    
    def get_user_password_by_id(self, id):
        cursor = self.conn.execute("SELECT * FROM users WHERE id=?;", (id,))
        for row in cursor:
            return row[4]
        return None
