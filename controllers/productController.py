import os
import time

from flask import Blueprint, render_template, request, session, url_for, current_app
from werkzeug.utils import redirect, secure_filename

from config import Config
from services.productService import ProductService

productBP = Blueprint("productBP", __name__)

productService = ProductService()

def isFileAllowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def saveFile(file):
    if file and isFileAllowed(file.filename):
        filename = secure_filename(file.filename)

        name, extension = os.path.splitext(filename)
        newFilename = f"{name}_{int(time.time())}{extension}"

        uploadFolder = current_app.config['UPLOAD_FOLDER']
        file_path = os.path.join(uploadFolder, newFilename)
        file.save(file_path)
        return newFilename
    return None

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
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        price = request.form.get("price")
        userID = session.get("user_id")

        image = None
        if "image" in request.files:
            file = request.files.get("image")
            if file.filename != "":
                image = saveFile(file)

        productService.addProduct(title, description, price, userID, image)
        return redirect(url_for("productBP.products"))

    return render_template("product/add_product.html")

@productBP.route("/product/<int:id>")
def detailProduct(id):
    if "user_id" not in session:
        return redirect(url_for("productBP.products"))

    product = productService.getProductById(id)
    return render_template("product/detail_product.html", product=product)

@productBP.route("/product/edit/<int:id>", methods=["GET", "POST"])
def editProduct(id):
    if "user_id" not in session:
        return redirect(url_for("productBP.products"))

    product = productService.getProductById(id)

    if session.get("user_id") != product.user_id:
        return redirect(url_for("productBP.products"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        price = request.form.get("price")

        image = product.image
        if "image" in request.files:
            file = request.files.get("image")
            if file.filename != "":
                if product.image:
                    oldImage = os.path.join(current_app.config['UPLOAD_FOLDER'], product.image)
                    if os.path.exists(oldImage):
                        os.remove(oldImage)

                image = saveFile(file)

        productService.updateProduct(product.id, title, description, price, image)

        return redirect(url_for("productBP.products"))

    return render_template("product/edit_product.html", product=product)

@productBP.route("/product/delete/<int:id>")
def deleteProduct(id):
    if "user_id" not in session:
        return redirect(url_for("productBP.products"))

    userID = productService.getProductOwner(id)

    if session.get("user_id") != userID:
        return redirect(url_for("productBP.products"))

    productService.deleteProduct(id)

    return redirect(url_for("productBP.products"))
