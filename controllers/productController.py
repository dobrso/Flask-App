from flask import Blueprint, render_template, request, session, url_for
from werkzeug.utils import redirect

from services.productService import ProductService
from services.userService import UserService

productBP = Blueprint("product", __name__)

productService = ProductService()
userService = UserService()

@productBP.route("/")
def products():
    userID = session.get("user_id")
    profileID = userService.getProfileID(userID)
    products = productService.getProducts()
    return render_template("product/products.html", products=products, profileID=profileID)

@productBP.route("/product/add", methods=["GET", "POST"])
def addProduct():
    if "user_id" not in session:
        return redirect(url_for("productBP.products"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        price = request.form.get("price")
        userID = session.get("user_id")

        imageFile = None
        if "image" in request.files:
            imageFile = request.files.get("image")

        productService.addProduct(title, description, price, userID, imageFile)
        return redirect(url_for("product.products"))

    return render_template("product/add_product.html")

@productBP.route("/product/<int:id>")
def detailProduct(id):
    product = productService.getProduct(id)
    return render_template("product/detail_product.html", product=product)

@productBP.route("/product/edit/<int:id>", methods=["GET", "POST"])
def editProduct(id):
    if "user_id" not in session:
        return redirect(url_for("product.products"))

    product = productService.getProduct(id)

    if session.get("user_id") != product.user_id:
        return redirect(url_for("product.products"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        price = request.form.get("price")

        imageFile = None
        if "image" in request.files:
            imageFile = request.files.get("image")

        productService.updateProduct(product.id, title, description, price, imageFile, product.image)
        return redirect(url_for("product.products"))

    return render_template("product/edit_product.html", product=product)

@productBP.route("/product/delete/<int:id>")
def deleteProduct(id):
    if "user_id" not in session:
        return redirect(url_for("product.products"))

    userID = productService.getProductOwner(id)

    if session.get("user_id") != userID:
        return redirect(url_for("product.products"))

    productService.deleteProduct(id)

    return redirect(url_for("product.products"))
