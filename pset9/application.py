import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

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


# Custom filter
app.jinja_env.filters["usd"] = usd


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Get the info from database
    portfolio = db.execute("SELECT * FROM portfolio WHERE user_id = ?", session["user_id"])
    userinfo = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

    # Get the current price of each stock from API and calculate the total value of stocks
    totalval = 0
    for stock in portfolio:
        stock["currentPrice"] = lookup(stock["symbol"])["price"]
        stock["value"] = stock["shares"] * stock["currentPrice"]
        totalval += stock["value"]

    cash = int(userinfo[0]["cash"])
    grandtotal = cash + totalval

    return render_template("index.html", portfolio=portfolio, cash=cash, grandtotal=grandtotal)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        # Get the stock info from the form (user input via POST)
        symbol = request.form.get("symbol")
        numshares = request.form.get("shares")

        # Verify the stock info
        if not symbol:
            return apology("must provide a stock's symbol", 400)
        if not numshares:
            return apology("must provide a number of shares", 400)
        if not lookup(symbol):
            return apology("stock not found", 400)
        if not numshares.isnumeric() or float(numshares) % 1 > 0 or int(numshares) <= 0:
            return apology("number of shares must be a positive integer", 400)

        numshares = int(numshares)