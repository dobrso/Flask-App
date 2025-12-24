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

    def getProduct(self, id):
        product = self.productRepository.getById(id)
        return product

    def addProduct(self, title, description, price, userID, imageFile):
        image = None
        if imageFile and imageFile.filename != "":
            image = FileHandler.saveFile(imageFile)

        self.productRepository.create(title, description, price, userID, image)

    def updateProduct(self, id, title, description, price, imageFile, oldImage):
        image = oldImage
        if imageFile.filename != "":
            if oldImage:
                oldImagePath = os.path.join(current_app.config['UPLOAD_FOLDER'], oldImage)
                if os.path.exists(oldImagePath):
                    os.remove(oldImagePath)

            image = FileHandler.saveFile(imageFile)
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
