import os
import time

from flask import current_app
from werkzeug.utils import secure_filename

from config import Config
from repositories.favoritesRepository import FavoritesRepository
from repositories.productRepository import ProductRepository


class ProductService:
    def __init__(self):
        self.productRepository = ProductRepository()
        self.favoritesRepository = FavoritesRepository()

    def getProducts(self):
        products = self.productRepository.getAll()
        return products

    def getProduct(self, id):
        product = self.productRepository.getById(id)
        return product

    def addProduct(self, title, description, price, userID, imageFile):
        image = None
        if imageFile and imageFile.filename != "":
            image = ProductService.saveFile(imageFile)

        self.productRepository.create(title, description, price, userID, image)

    def updateProduct(self, id, title, description, price, imageFile, oldImage):
        image = oldImage
        if imageFile.filename != "":
            if oldImage:
                oldImagePath = os.path.join(current_app.config['UPLOAD_FOLDER'], oldImage)
                if os.path.exists(oldImagePath):
                    os.remove(oldImagePath)

            image = ProductService.saveFile(imageFile)
        self.productRepository.updateById(id, title, description, price, image)

    def deleteProduct(self, id):
        image = self.productRepository.getProductImage(id)
        if image:
            imagePath = os.path.join(current_app.config["UPLOAD_FOLDER"], image)
            if os.path.exists(imagePath):
                os.remove(imagePath)

        self.productRepository.deleteById(id)

    def getProductOwner(self, id):
        userID = self.productRepository.getProductOwner(id)
        return userID

    def addUserFavorite(self, userID, productID):
        self.favoritesRepository.add(userID, productID)

    def deleteUserFavorite(self, userID, productID):
        self.favoritesRepository.delete(userID, productID)

    def getUserFavorites(self, userID):
        favorites = self.favoritesRepository.getAll(userID)
        return favorites

    def getUserFavoriteProducts(self, userID):
        favorites = self.favoritesRepository.getAll(userID)
        if not favorites:
            return None

        products = []
        for favorite in favorites:
            product = self.productRepository.getById(favorite)
            products.append(product)
        return products

    @staticmethod
    def isFileAllowed(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

    @staticmethod
    def saveFile(file):
        if file and ProductService.isFileAllowed(file.filename):
            filename = secure_filename(file.filename)

            name, extension = os.path.splitext(filename)
            newFilename = f"{name}_{int(time.time())}{extension}"

            uploadFolder = current_app.config['UPLOAD_FOLDER']
            filePath = os.path.join(uploadFolder, newFilename)
            file.save(filePath)
            return newFilename
        return None