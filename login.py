import re
from flask import Flask, request, redirect, url_for, render_template, flash, session, jsonify, send_from_directory
import sqlite3
from flask import g 
import os
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import random
import smtplib
from email.mime.text import MIMEText
import logging
from logging import FileHandler
from main import app
import time
import logging

DATABASE = "/cloudide/workspace/SoftCare/data.db"

# Set a secret key for session cookies
app.secret_key = "your_very_secret_key"  # Change this to a strong, random key

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

        data = request.json
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
            "SELECT userid, usertype FROM users WHERE username = ? AND password = ?", (username, password)
        ).fetchone()
        conn.close()

        if user:
            user_id = user["userid"]  # Corrected column name
            usertype = user["usertype"]

            print(f"✅ Login successful! UserType: {usertype}, UserID: {user_id}")
             # Update the user's status to "Online"
            cursor.execute("UPDATE users SET status = ? WHERE userid = ?", ("Online", user_id))
            conn.commit()
            conn.close()

            # Store user info in session (cookie storage)
            session["user_id"] = user_id
            session["usertype"] = usertype
            session["username"] = username
            session.permanent = True  # Keep session persistent
            app.permanent_session_lifetime = timedelta(days=7)  # Session expires after 7 days

            return jsonify({"success": True, "message": "Login successful", "user_id": user_id, "usertype": usertype})
        else:
            print("❌ Invalid username or password.")
            return jsonify({"success": False, "message": "Invalid username or password"}), 401

    except sqlite3.Error as sql_error:
        print(f"⚠️ Database error: {sql_error}")
        return jsonify({"success": False, "message": "Database error"}), 500

    except Exception as e:
        print(f"⚠️ Unexpected error in /login: {e}")
        return jsonify({"success": False, "message": "Internal Server Error"}), 500


@app.route("/logout", methods=["POST"])
def logout():
    """Logs the user out by updating status to 'Offline' and clearing the session."""
    try:
        user_id = session.get("user_id")  # Get user_id from session
        
        if user_id:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Update the user's status to "Offline"
            cursor.execute("UPDATE users SET status = ? WHERE userid = ?", ("Offline", user_id))
            conn.commit()
            conn.close()
            
            print(f"🔴 User {user_id} set to Offline.")

        session.clear()  # Remove all stored session data
        print("✅ User logged out successfully.")

        return jsonify({"success": True, "message": "Logout successful"})

    except sqlite3.Error as sql_error:
        print(f"⚠️ Database error: {sql_error}")
        return jsonify({"success": False, "message": "Database error"}), 500

    except Exception as e:
        print(f"⚠️ Unexpected error in /logout: {e}")
        return jsonify({"success": False, "message": "Internal Server Error"}), 500


@app.route("/session-data", methods=["GET"])
def get_session_data():
    """Returns session data for debugging or client-side verification."""
    if "user_id" in session:
        return jsonify({
            "logged_in": True,
            "user_id": session["user_id"],
            "usertype": session["usertype"],
            "username": session["username"],
        })
    else:
        return jsonify({"logged_in": False, "message": "No active session"}), 401
