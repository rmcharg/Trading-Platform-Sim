from flask import Flask, flash, redirect, render_template, request, session


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login ():
    return render_template("login.html")

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

@app.route("/transactions")
def transactions():
    return render_template("transactions.html")




if __name__ == "__main__":
    app.run(debug=True)