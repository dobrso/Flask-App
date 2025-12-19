from flask import Blueprint, request, render_template, session, url_for, flash
from werkzeug.utils import redirect

from services.userService import UserService

userBP = Blueprint("user", __name__)

userService = UserService()

@userBP.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirmPassword = request.form["confirmPassword"]

        if password != confirmPassword:
            flash("Пароли не совпадают", "danger")
            return render_template("registration.html")

        status, message, userID = userService.register(username, password)
        if status:
            session["user_id"] = userID
            flash(message, "success")
            return redirect(url_for("home"))

        flash(message, "danger")
        return render_template("registration.html")


    return render_template("registration.html")

@userBP.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        status, message, userID = userService.login(username, password)
        if status:
            session["user_id"] = userID
            flash(message, "success")
            return redirect(url_for("home"))

        flash(message, "danger")
        return render_template("login.html")

    return render_template("login.html")

@userBP.route("/logout")
def logout():
    if "user_id" in session:
        session.pop("user_id")

    return redirect(url_for("home"))
