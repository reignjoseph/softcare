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



@app.route('/local/<username>')
def local(username):
    """Fetches all user details for the given username if they are a local user."""
    conn = get_db_connection()
    
    # Fetch full user data from the database
    user = conn.execute(
        "SELECT * FROM users WHERE username = ? AND usertype = 'Local'", 
        (username,)
    ).fetchone()
    
    conn.close()

    if user:
        return render_template('local_user.html', data=dict(user))  # Convert Row object to dictionary
    else:
        return "❌ Access Denied: You are not a local user.", 403  # Forbidden access




@app.route("/local_user_data")
def get_local_user_data():
    """Fetch the logged-in user's data from the database."""
    if "user_id" not in session:
        return redirect(url_for("login"))  # Redirect to login if not logged in

    user_id = session["user_id"]  # Get the user ID from the session
    conn = get_db_connection()
    
    # Fetch user details from the database
    user = conn.execute("SELECT username FROM users WHERE userid = ?", (user_id,)).fetchone()
    conn.close()

    if user:
        return render_template("local_user.html", data={"username": user["username"]})
    else:
        return redirect(url_for("login"))  # Redirect if user not found

@app.route("/records")
def records():
    """Fetches all patient records and returns them as JSON."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Retrieve all patient records
    cursor.execute("SELECT * FROM patient_records")
    records = cursor.fetchall()
    
    conn.close()

    # Debugging: Print records to check if data is retrieved
    print("📌 Retrieved Records:", records)

    if not records:
        print("⚠️ No records found in the database.")

    # Convert records to a list of dictionaries
    patients = [
        {
            "id": row["patientid"],
            "firstname": row["patientfirstname"],
            "lastname": row["patientlastname"],
            "age": row["patientage"],
            "sex": row["patientsex"],
            "room": row["room"],
            "admission": row["dateaddmision"],
            "discharge": row["datedischarge"],
            "assist": row["assist"]
        }
        for row in records
    ]

    # Debugging: Print the formatted patient data
    print("✅ Processed Patient Data:", patients)

    return jsonify(patients)
