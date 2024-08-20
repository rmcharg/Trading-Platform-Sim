from flask import Blueprint, render_template, request, session
from flaskr.helpers import login_required

views = Blueprint('views', __name__)

@views.route("/")
@login_required
def index():
    return render_template("index.html")

@views.route("/portfolio")
@login_required
def portfolio():
    return render_template("portfolio.html")

@views.route("/transactions")
@login_required
def transactions():
    return render_template("transactions.html")


@views.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response