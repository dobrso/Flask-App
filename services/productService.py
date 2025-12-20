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

    def addProduct(self, title, description, price, userID):
        self.productRepository.create(title, description, price, userID)

    def updateProduct(self, id, title, description, price):
        self.productRepository.updateById(id, title, description, price)

    def deleteProduct(self, id):
        self.productRepository.deleteById(id)
