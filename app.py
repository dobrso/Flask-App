from flask import Flask

from config import Config
from controllers.productController import productBP
from controllers.userController import userBP
from database.database import Database

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

app.register_blueprint(userBP)
app.register_blueprint(productBP)

if __name__ == "__main__":
    db = Database()
    db.initDB()

    app.run(debug=True)
