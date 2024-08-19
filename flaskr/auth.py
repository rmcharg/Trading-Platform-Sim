from flask import render_template, session, Blueprint

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=["GET", "POST"])
def login ():
    """Log user in"""

    # forget user_id from previous log in
    return render_template("login.html")

@auth.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")