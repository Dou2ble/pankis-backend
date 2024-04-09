from fastapi import FastAPI
from profanity import has_profanity
import sqlite3
import bcrypt
import re
from dotenv import load_dotenv
import jwt
import os

def is_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

load_dotenv()
secret = os.getenv('SECRET')
if secret is None:
    raise Exception('SECRET not found in .env file')

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

def create_tables():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users
            (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, email TEXT, password TEXT)
        ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats
            (user_id INTEGER PRIMARY KEY, pancakes INTEGER, total_pancakes INTEGER)
    ''')
    
    conn.commit()

create_tables()

app = FastAPI()

@app.get("/")
def read_root():
    return {"success": True, "message": "Hello World"}

@app.get("/account/create")
def create_account(username: str, email: str, password: str):
    if has_profanity(username):
        return {"success": False, "message": "Username contains profanity"}
    if not is_email(email):
        return {"success": False, "message": "Invalid email address"}
    if len(password) < 8:
        return {"success": False, "message": "Password must be at least 8 characters long"}

    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cursor.execute('''
        INSERT INTO users (username, email, password)
        VALUES (?, ?, ?)
        ''', (username, email, hashed_password))
    
    conn.commit()

    return {"success": True, "message": "Account created"}

@app.get("/account/login")
def login_account(email: str, password: str):
    if not is_email(email):
        return {"success": False, "message": "Invalid email address"}

    cursor.execute('''
        SELECT * FROM users WHERE email = ?
        ''', (email,))
    
    user = cursor.fetchone()

    if user is None:
        return {"success": False, "message": "User not found"}
    
    if not bcrypt.checkpw(password.encode('utf-8'), user[3]):
        return {"success": False, "message": "Invalid password"}
    
    # generate a access token for the user
    token = jwt.encode({'id': user[0]}, secret, algorithm='HS256')

    return {"success": True, "message": "Logged in", "token": token}

@app.get("/account/update-stats")
def update_stats_account(token: str, pancakes: int, total_pancakes: int):
    if pancakes < 0:
        return {"success": False, "message": "Invalid pancakes value"}
    if total_pancakes < 0:
        return {"success": False, "message": "Invalid total_pancakes value"}

    try:
        user = jwt.decode(token, secret, algorithms=['HS256'])
    except:
        return {"success": False, "message": "Invalid token"}
    
    cursor.execute('''
        INSERT INTO stats (user_id, pancakes, total_pancakes)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET pancakes = ?, total_pancakes = ?
        ''', (user['id'], pancakes, total_pancakes, pancakes, total_pancakes))
    
    conn.commit()

@app.get("/leaderboard")
def leaderboard():
    cursor.execute('''
        SELECT username, pancakes, total_pancakes FROM stats
        JOIN users ON stats.user_id = users.id
        ORDER BY total_pancakes DESC
        ''')
    
    data = cursor.fetchall()

    return {"success": True, "data": data}


# run using:
# uvicorn main:app --reload