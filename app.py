import os

from flask import Flask

from config import Config
from controllers.productController import productRoute
from controllers.userController import userRoute
from database.database import Database

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
app.config["UPLOAD_FOLDER"] = Config.UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = Config.MAX_CONTENT_LENGTH

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

app.register_blueprint(userRoute)
app.register_blueprint(productRoute)

if __name__ == "__main__":
    database = Database()
    database.initDB()

    app.run(debug=True)
