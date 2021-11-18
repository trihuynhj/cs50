import os
import re
import requests

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import error, login_required, random_image, send_email

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

# Index page: shows user's info (history, number of searchs left etc.)
@app.route("/")
@login_required
def index():
    """Render user's search history."""

    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0] # Return a dictionary
    responses = db.execute("SELECT * FROM search_history WHERE user_id = ?", session["user_id"]) # Return a list of dictionaries
    return render_template("index.html", user=user, responses=responses)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Check and make sure the password contain at least 1 number and 1 special symbol

    # When getting a POST method, check and process the user registration info
    if request.method == "POST":
        if not request.form.get("username"):
            return error("must provide a username", 400)
        if not request.form.get("password"):
            return error("must provide a password", 400)
        if not request.form.get("confirmation"):
            return error("must provide a password confirmation", 400)
        if db.execute("SELECT username FROM users WHERE username = ?", request.form.get("username")):
            return error("username has already been registered", 400)
        if request.form.get("password") != request.form.get("confirmation"):
            return error("The passwords do not match", 400)
        
        # Check and validate password (more than 10 characters and containing at least 1 number and 1 special character)
        user_password = request.form.get("password")
        if len(user_password) < 16:
            return render_template("register.html", invalid_password=4)
        
        check_number = re.findall("[0-9]", user_password)
        check_symbol = re.findall("[!@#$%^&*()_+]", user_password)
        if not check_number and not check_symbol:
            return render_template("register.html", invalid_password=1)
        