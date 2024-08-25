from flaskr import create_app, create_database
from flask_session import Session
from flask import session


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
    # Initialise a session variable called data this will store stock data for us so
    # we do not need to query again when we change web page
    session['data'] = None
 