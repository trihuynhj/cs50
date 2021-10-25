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

        # Process the buy request
        stock = lookup(symbol)
        date = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
        usercash = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        # Abort if user cannot afford the number of shares at current price
        if stock["price"] * numshares > usercash:
            return apology("not enough money to proceed", 400)

        # Register the BUY request in history TABLE (BUY means trade = 0)
        db.execute("INSERT INTO history (user_id, trade, name, symbol, price, shares, time) VALUES (?, 0, ?, ?, ?, ?, ?)",
                   session["user_id"], stock["name"], stock["symbol"], stock["price"], numshares, date)

        # Update the user's cash balance in users TABLE
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", stock["price"] * numshares, session["user_id"])

         # Update the user's portfolio in portfolio TABLE
        # If the symbol already exists in portfolio, update its shares
        if db.execute("SELECT symbol FROM portfolio WHERE user_id = ? AND symbol = ?", session["user_id"], stock["symbol"]):
            db.execute("UPDATE portfolio SET shares = shares + ? WHERE user_id = ? AND symbol = ?",
                       numshares, session["user_id"], stock["symbol"])
        # If the symbol does not exist, insert it into the portfolio
        else:
            db.execute("INSERT INTO portfolio (user_id, name, symbol, shares) VALUES (?, ?, ?, ?)",
                       session["user_id"], stock["name"], stock["symbol"], numshares)

        # Redirect user to the main page
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    history = db.execute("SELECT * FROM history WHERE user_id = ?", session["user_id"])
    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        if not lookup(request.form.get("symbol")):
            return apology("stock not found", 400)

        stock = lookup(request.form.get("symbol"))
        date = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
        return render_template("quoted.html", stock=stock, date=date)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

        # When getting a POST method, check and process the user registration info
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide a username", 400)
        if not request.form.get("password"):
            return apology("must provide a password", 400)
        if not request.form.get("confirmation"):
            return apology("must provide a password confirmation", 400)
        if db.execute("SELECT username FROM users WHERE username = ?", request.form.get("username")):
            return apology("username has already been registered", 400)
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("The passwords do not match", 400)
        
        user_username = request.form.get("username")
        user_hash = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", user_username, user_hash)

        return render_template("login.html")
    
    # Otherwise (received a GET method), render the register page
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":
        # Get the sell request info from user input
        symbol = request.form.get("symbol")
        numshares = request.form.get("shares")
        portfolio = db.execute("SELECT * FROM portfolio WHERE user_id = ?", session["user_id"])

         # Verify the sell request
        if not symbol:
            return apology("must provide a stock's symbol", 400)
        if not numshares:
            return apology("must provide a number of shares", 400)
        if not numshares.isnumeric() or float(numshares) % 1 > 0 or int(numshares) < 0:
            return apology("number of shares must be a positive integer", 400)
        numshares = int(numshares)
        symbol = symbol.upper()

        for stock in portfolio:
            # Check if the sell stock is in portfolio, then process the sell request if found
            if stock["symbol"] == symbol:
                # Apologize if number of shares to sell is larger than actually in portfolio
                if stock["shares"] < numshares:
                    return apology("you don't have that many shares to sell", 400)
                # If there is only 1 share left, delete that row from portfolio
                elif stock["shares"] == 1:
                    db.execute("DELETE FROM portfolio WHERE user_id = ? AND symbol = ?", session["user_id"], stock["symbol"])
                # Otherwise, update the number of shares left in portfolio
                else:
                    db.execute("UPDATE portfolio SET shares = shares - ? WHERE user_id = ? AND symbol = ?",
                               numshares, session["user_id"], stock["symbol"])
                
                # Update the user's cash balance
                sellvalue = lookup(stock["symbol"])["price"]
                db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", sellvalue * numshares, session["user_id"])

                # Update the transaction log (history TABLE) (SELL means trade = 1)
                date = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
                db.execute("INSERT INTO history (user_id, trade, name, symbol, price, shares, time) VALUES (?, 1, ?, ?, ?, ?, ?)",
                           session["user_id"], stock["name"], stock["symbol"], sellvalue, numshares, date)

                # Once done, redirect user to index page
                return redirect("/")

        # If stock not found in portfolio, apologize to user
        return apology("stock not in portfolio", 400)

    # Otherwise (received a GET method), render the sell page for user input
    else:
        # Get the stocks from portfolio to render the select field in sell page
        portfolio = db.execute("SELECT * FROM portfolio WHERE user_id = ?", session["user_id"])
        return render_template("sell.html", portfolio=portfolio)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


