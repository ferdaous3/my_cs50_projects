import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Disable caching in debug mode
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter for USD
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect to database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    stocks = db.execute("SELECT symbol, SUM(shares) AS total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0", user_id)
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    total = cash
    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["price"] = quote["price"]
        stock["name"] = quote["name"]
        stock["total"] = stock["price"] * stock["total_shares"]
        total += stock["total"]

    return render_template("index.html", stocks=stocks, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol")
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("invalid number of shares")

        quote = lookup(symbol)
        if quote is None:
            return apology("invalid symbol")

        shares = int(shares)
        price = quote["price"]
        total_cost = shares * price
        user_id = session["user_id"]
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        if cash < total_cost:
            return apology("not enough cash")

        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, user_id)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, type, time) VALUES (?, ?, ?, ?, 'buy', ?)",
                   user_id, quote["symbol"], shares, price, datetime.datetime.now())

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    user_id = session["user_id"]
    transactions = db.execute("SELECT symbol, shares, price, type, time FROM transactions WHERE user_id = ? ORDER BY time DESC", user_id)
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol")
        quote = lookup(symbol)
        if quote is None:
            return apology("invalid symbol")
        return render_template("quoted.html", quote=quote)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username")

        if not password or not confirmation:
            return apology("must provide password and confirmation")

        if password != confirmation:
            return apology("passwords must match")

        hash_pw = generate_password_hash(password)

        try:
            user_id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_pw)
        except:
            return apology("username already exists")

        session["user_id"] = user_id
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    user_id = session["user_id"]
    symbols = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", user_id)

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must select a stock")
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("invalid number of shares")

        shares = int(shares)
        owned = db.execute("SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol", user_id, symbol)[0]["total_shares"]

        if shares > owned:
            return apology("too many shares")

        quote = lookup(symbol)
        price = quote["price"]
        total_value = shares * price

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_value, user_id)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, type, time) VALUES (?, ?, ?, ?, 'sell', ?)",
                   user_id, symbol, -shares, price, datetime.datetime.now())

        return redirect("/")
    else:
        return render_template("sell.html", symbols=[row["symbol"] for row in symbols])
