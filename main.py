from flaskr import create_app, create_database
from flask_session import Session

app = create_app()
create_database()

if __name__ == "__main__":
    app.run(debug=True)
 