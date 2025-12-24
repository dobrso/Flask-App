import os

from flask import current_app

from repositories.favoritesRepository import FavoritesRepository
from repositories.productRepository import ProductRepository
from utilities.fileHandler import FileHandler


class ProductService:
    def __init__(self):
        self.productRepository = ProductRepository()
        self.favoritesRepository = FavoritesRepository()

    def getProducts(self):
        products = self.productRepository.getAll()
        return products

    def getProduct(self, productId):
        product = self.productRepository.get(productId)
        return product

    def addProduct(self, title, description, price, userId, imageFile):
        image = None
        if imageFile and imageFile.filename != "":
            image = FileHandler.saveFile(imageFile)

        self.productRepository.create(title, description, price, userId, image)

    def updateProduct(self, productId, title, description, price, imageFile, oldImage):
        image = oldImage
        if imageFile.filename != "":
            if oldImage:
                oldImagePath = os.path.join(current_app.config['UPLOAD_FOLDER'], oldImage)
                if os.path.exists(oldImagePath):
                    os.remove(oldImagePath)

            image = FileHandler.saveFile(imageFile)
        self.productRepository.update(productId, title, description, price, image)

    def deleteProduct(self, productId):
        image = self.productRepository.getImage(productId)
        if image:
            imagePath = os.path.join(current_app.config["UPLOAD_FOLDER"], image)
            if os.path.exists(imagePath):
                os.remove(imagePath)

        self.productRepository.delete(productId)

    def getProductOwner(self, productId):
        userId = self.productRepository.getOwner(productId)
        return userId

    def addUserFavorite(self, userId, productId):
        self.favoritesRepository.add(userId, productId)

    def deleteUserFavorite(self, userId, productId):
        self.favoritesRepository.delete(userId, productId)

    def getUserFavorites(self, userId):
        favorites = self.favoritesRepository.getAll(userId)
        return favorites

    def getUserFavoriteProducts(self, userId):
        favorites = self.favoritesRepository.getAll(userId)
        if not favorites:
            return None

        products = []
        for favorite in favorites:
            product = self.productRepository.get(favorite)
            products.append(product)
        return products
