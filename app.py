from flask import Flask, render_template

from config import Config
from controllers.userController import userBP
from database.database import Database

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

app.register_blueprint(userBP)


@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    db = Database()
    db.initDB()

    app.run(debug=True)
