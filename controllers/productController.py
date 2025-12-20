from flask import Blueprint, render_template, request, session, url_for
from werkzeug.utils import redirect

from services.productService import ProductService

productBP = Blueprint("productBP", __name__)

productService = ProductService()

@productBP.route("/")
def products():
    userID = session.get("user_id")
    products = productService.getProducts()
    return render_template("product/products.html", products=products, userID=userID)

@productBP.route("/product/add", methods=["GET", "POST"])
def addProduct():
    if "user_id" not in session:
        return redirect(url_for("productBP.products"))

    if request.method == "POST":
        title = request.form["title"].strip()
        description = request.form["description"].strip()
        price = request.form["price"]
        userID = session["user_id"]

        productService.addProduct(title, description, price, userID)
        return redirect(url_for("productBP.products"))

    return render_template("product/add_product.html")

@productBP.route("/product/<int:id>")
def detailProduct(id):
    product = productService.getProductById(id)
    return render_template("product/detail_product.html", product=product)

@productBP.route("/product/edit/<int:id>", methods=["GET", "POST"])
def editProduct(id):
    product = productService.getProductById(id)

    if request.method == "POST":
        title = request.form["title"].strip()
        description = request.form["description"].strip()
        price = request.form["price"]

        productService.updateProduct(product.id, title, description, price)

        return redirect(url_for("productBP.products"))

    return render_template("product/edit_product.html", product=product)

@productBP.route("/product/delete/<int:id>")
def deleteProduct(id):
    productService.deleteProduct(id)

    return redirect(url_for("productBP.products"))
