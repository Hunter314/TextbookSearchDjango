SORTING_MODE = 1
class Product:
    price = ""
    rating = 0
    name = ""
    shipPrice = 0
    url = ""
    rating = 0
    distributor = ""
    def __init__(self, name, price, shipPrice, url, rating, distributor = "N/A"):
        self.name = name
        self.price = price
        self.rating = rating
        self.shipPrice = shipPrice
        self.distributor = distributor
        self.url = url
    def __lt__(self, other):
        if SORTING_MODE == 1:
            if(self.shipPrice is not None and other.shipPrice is not None):
                return self.price + self.shipPrice < other.price + other.shipPrice
            else:
                return self.price < other.price
        if SORTING_MODE == 2:
            return self.price < other.price
        if SORTING_MODE == 3:
            return self.rating > other.rating
        return False
    def getPrice(self):
        return self.price
    def getName(self):
        return self.name
    def getRating(self):
        return self.rating
    def getShipPrice(self):
        return self.shipPrice
    def getTotalPrice(self):
        return self.price + self.shipPrice
    def toString(self):
        return "Name: " + self.name + "\nPrice: " + str(self.price) + "\nRating: " + str(self.rating) + "\nShipping Price: " + str(self.shipPrice) + "\nDistributor: " + str(self.distributor)

