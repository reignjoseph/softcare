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
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ? AND usertype = 'Local'", (username,)).fetchone()
    conn.close()

    if user:
        return render_template('local_user.html', username=username)
    else:
        return "❌ Access Denied: You are not a local user.", 403  # Forbidden access
