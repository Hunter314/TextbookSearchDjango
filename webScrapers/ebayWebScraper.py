from bs4 import BeautifulSoup
import requests
import html5lib
import sys
from .productClass import Product
#methods used for scraper
def priceprocess(string):
    index = -1
    if string == "":
        return 0
    for i in range(0, len(string)-1):
        if string[i] == ' ':
            index = i
    return float(string[index+2:])

def ratingprocess(string):
    index = -1
    if string == "":
        return 0
    for i in range(0, len(string)):
        if string[i] == ' ':
            index = i
            break
    if index == -1:
        return 0
    return float(string[0:index])

SORTING_MODE = 1
#1 - Price + ShippingPrice / 2 - Price / 3 - Rating

class EbayWebScraper:
    searchItem = "test"
    parsedContent = "blank"
    soup = None #BeautifulSoup representation of website
    def __init__(self, searchTerm):
        self.searchItem = searchTerm

        #headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64;     x64; rv:66.0) Gecko/20100101 Firefox/66.0",
                   #"Accept-Encoding": "gzip, deflate",
                   #"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
                   #"Connection": "close", "Upgrade-Insecure-Requests": "1"}

        page = requests.get("https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw="+searchTerm+"&_sacat=0&LH_BIN=1")
        html_file = page.content

        self.soup = BeautifulSoup(html_file, 'html5lib')
        self.parsedContent = html_file


    def getProducts(self):
        listProducts = self.soup.find_all(class_='s-item')
        countGood = 0

        Products = []

        for i in range(0, len(listProducts)):
            bookListing = listProducts[i]
            if not bookListing.find(class_="s-item__title--tagblock"):
                #print("I found a good one!")
                #print(bookListing.prettify())

                bookName = bookListing.find(class_="s-item__title").text

                bookUrl = bookListing.find(class_="s-item__link")["href"]

                bookDistributor = bookListing.find(class_="s-item__subtitle").text

                bookRating = bookListing.find(class_="b-starrating")
                if bookRating and bookRating.find(class_="clipped"):
                    bookRating = ratingprocess(bookRating.find(class_="clipped").text)
                else:
                    bookRating = 0
                
                if bookDistributor[0:2] == "by":
                    bookDistributor = bookDistributor[3:]
                else:
                    bookDistributor = "N/A"
                
                bookPrice = 0
                if bookListing.find(class_="s-item__price").text[-1:] != "g":
                    bookPrice = priceprocess(bookListing.find(class_="s-item__price").text)

                shippingPrice = 0
                if bookListing.find(class_="s-item__shipping s-item__logisticsCost").text[-1:] != "g":
                   shippingPrice = priceprocess(bookListing.find(class_="s-item__shipping s-item__logisticsCost").text)            

                Products.append(Product(bookName, bookPrice, shippingPrice, bookUrl, bookRating, bookDistributor))
                
                countGood += 1
            if countGood == 10:
                break
        return sorted(Products)
    
    def getProductsAndPrint(self):
        Products = self.getProducts()
        for thisProduct in Products:
            print(thisProduct.toString())
        return Products


#name = input("What is the name of your book?")
#testScraper = EbayWebScraper(name)

#testScraper.getProductsAndPrint()




