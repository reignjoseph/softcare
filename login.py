import re
from flask import Flask, request, redirect, url_for, render_template, flash, session, jsonify,send_from_directory
import sqlite3
from flask import g 
import os
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import random
import smtplib
from email.mime.text import MIMEText
#___________________________________
import logging
from logging import FileHandler
from main import app
import time
import logging

DATABASE = "/cloudide/workspace/SoftCare/data.db"

def get_db_connection():
    """Establishes and reuses a database connection per request."""
    print("🔹 Attempting to connect to database...")
    if "db" not in g:
        if not os.path.exists(DATABASE):
            print(f"⚠️ Database not found at {DATABASE}")
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # Allows accessing columns by name
        print("✅ Database connection established.")
    return g.db

@app.teardown_appcontext
def close_db_connection(exception):
    """Closes the database connection after request execution."""
    db = g.pop("db", None)
    if db is not None:
        print("🔸 Closing database connection.")
        db.close()

@app.route("/login", methods=["POST"])
def login():
    try:
        print("\n🔹 Received login request.")

        print("Request headers:", request.headers)  # Print request headers
        print("Raw request data:", request.data)  # Print raw request data

        data = request.json
        print("Parsed JSON data:", data)  # Print parsed JSON

        if not data:
            return jsonify({"success": False, "message": "Invalid JSON data"}), 400
        
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            print("❌ Missing username or password.")
            return jsonify({"success": False, "message": "Username and password required"}), 400

        print(f"🔍 Checking database for user: {username}")

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?", (username, password)
        ).fetchone()

        if user:
            usertype = user["usertype"]
            print(f"✅ Login successful! UserType: {usertype}")
            return jsonify({"success": True, "usertype": usertype})
        else:
            print("❌ Invalid username or password.")
            return jsonify({"success": False, "message": "Invalid username or password"}), 401

    except sqlite3.Error as sql_error:
        print(f"⚠️ Database error: {sql_error}")
        return jsonify({"success": False, "message": "Database error"}), 500

    except Exception as e:
        print(f"⚠️ Unexpected error in /login: {e}")
        return jsonify({"success": False, "message": "Internal Server Error"}), 500