from repositories.productRepository import ProductRepository


class ProductService:
    def __init__(self):
        self.productRepository = ProductRepository()

    def getProducts(self):
        products = self.productRepository.getAll()
        return products

    def getProductById(self, id):
        product = self.productRepository.getById(id)
        return product

    def addProduct(self, title, description, price, userID, image=None):
        self.productRepository.create(title, description, price, userID, image)

    def updateProduct(self, id, title, description, price, image=None):
        self.productRepository.updateById(id, title, description, price, image)

    def deleteProduct(self, id):
        self.productRepository.deleteById(id)

    def getProductOwner(self, id):
        userID = self.productRepository.getProductOwner(id)
        return userID