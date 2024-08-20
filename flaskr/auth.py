from flask import render_template, Blueprint, request, flash, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from os import path
from flask_session import Session
from flaskr.helpers import login_required


auth = Blueprint('auth', __name__)

@auth.route("/login", methods=["GET", "POST"])
def login ():
    """Log user in"""

    # make sure no user id stored in session cookie
    session.clear()
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        # check if username or password is empty
        if username is None:
            flash("Must provide username")
            return redirect("/login")
        elif password is None:
            flash("Must provide password")
            return redirect("/login")
        
        # connect to database and set row format so we can use column name
        # to access elements
        conn = sqlite3.connect("flaskr/trade.db")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # Query database and fetchall results giving us a list of rows
        rows = cur.execute('SELECT id, username, hash FROM users WHERE username = ?',(username,)).fetchall()

        if len(rows) !=1 or not check_password_hash(rows[0]['hash'], password):
            print('Login Failed !')
            flash('Invalid username or password')
            return redirect("/login")
        
        print('Login Success')
        flash('Signed In')
        session['user_id'] = rows[0]['id']                        
        return redirect("/")

        


@auth.route("/register", methods=["GET", "POST"])
def register():
    """Register user account"""

    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # check all fields are filled and password matches confirmation
        if username is None or password is None or confirmation is None:
            flash("None of the fields can be empty")
            return redirect("/register")

        if password != confirmation:
            flash("Password and confirmation must match!")
            return redirect("/register")

        # Create new user
        conn  = sqlite3.connect('flaskr/trade.db')
        cur = conn.cursor()

        try:
            cur.execute('INSERT INTO users (username, hash) VALUES (?, ?)', (username, generate_password_hash(password)))
            conn.commit()
            cur.close()
            flash("Account Created!")
            return redirect("/login")
        except:
            flash("Username already exists")
            cur.close()
            return redirect("/register")


@auth.route("/logout")
@login_required
def logout():
    """Log user out """
    session.clear()
    return redirect("/")

