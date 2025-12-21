import os

from flask import Flask

from config import Config
from controllers.productController import productBP
from controllers.userController import userBP
from database.database import Database

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
app.config["UPLOAD_FOLDER"] = Config.UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = Config.MAX_CONTENT_LENGTH

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

app.register_blueprint(userBP)
app.register_blueprint(productBP)

if __name__ == "__main__":
    if os.path.exists(app.config["UPLOAD_FOLDER"]):
        for file in os.listdir(app.config["UPLOAD_FOLDER"]):
            os.remove(os.path.join(app.config["UPLOAD_FOLDER"], file))

    db = Database()
    db.initDB()

    app.run(debug=True)
