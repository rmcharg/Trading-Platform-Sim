from flask import Flask, flash, redirect, render_template, request
from flask_session import Session

from helpers import login_required

import sqlite3 


app = Flask(__name__)
app.config['SECRET_KEY'] = 'uhfoauwheoachowehico'

# Configure sessions to use filesystem 
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
@login_required
def index():
    return render_template("index.html")



@app.route("/portfolio")
@login_required
def portfolio():
    return render_template("portfolio.html")

@app.route("/transactions")
@login_required
def transactions():
    return render_template("transactions.html")




if __name__ == "__main__":
    app.run(debug=True)