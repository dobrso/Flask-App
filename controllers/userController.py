from flask import Blueprint, request, render_template, session, url_for, flash
from werkzeug.utils import redirect

from services.userService import UserService

userRoute = Blueprint("user", __name__)

userService = UserService()

@userRoute.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        name = request.form.get("name").strip()
        password = request.form.get("password").strip()
        confirmPassword = request.form.get("confirmPassword").strip()

        if password != confirmPassword:
            flash("Пароли не совпадают", "danger")
            return render_template("user/registration.html")

        status, message, userId = userService.register(name, password)
        if status:
            session["user_id"] = userId
            return redirect(url_for("product.products"))

        flash(message, "danger")
        return render_template("user/registration.html")

    return render_template("user/registration.html")

@userRoute.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name").strip()
        password = request.form.get("password").strip()

        status, message, userId = userService.login(name, password)
        if status:
            session["user_id"] = userId
            return redirect(url_for("product.products"))

        flash(message, "danger")
        return render_template("user/login.html")

    return render_template("user/login.html")

@userRoute.route("/logout")
def logout():
    if "user_id" in session:
        session.pop("user_id")

    return redirect(url_for("product.products"))

@userRoute.route("/profile/<int:id>", methods=["GET", "POST"])
def profile(id):
    userId = session.get("user_id")
    profile = userService.getProfile(id)
    user = userService.getUser(id)

    if request.method == "POST":
        bio = request.form.get("bio").strip()
        phoneNumber = request.form.get("phoneNumber").strip()

        imageFile = None
        if "image" in request.files:
            imageFile = request.files.get("image")

        userService.updateProfile(user.id, bio, phoneNumber, imageFile, profile.image)
        profile = userService.getProfile(id)
        return render_template("user/profile.html", profile=profile, user=user, userId=userId)

    return render_template("user/profile.html", profile=profile, user=user, userId=userId)
