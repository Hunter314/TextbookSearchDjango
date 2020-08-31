import requests
from bs4 import BeautifulSoup
import html5lib
from .productClass import Product

SORTING_MODE = 1
#1 - Price + ShippingPrice / 2 - Price / 3 - Rating

class AmazonWebScraper:
    searchItem = "test"
    parsedContent = "blank"
    def __init__(self, searchTerm):
        self.searchItem = searchTerm

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64;     x64; rv:66.0) Gecko/20100101 Firefox/66.0",
                   "Accept-Encoding": "gzip, deflate",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
                   "Connection": "close", "Upgrade-Insecure-Requests": "1"}

        page = requests.get("https://www.amazon.com/s?k=" + self.searchItem, headers=headers)
        # test if response is good. 200 is all ok
        print(page)

        self.parsedContent = BeautifulSoup(page.content, 'html5lib')

        # For debugging:
        #print(parsedContent.prettify())

        # searchPrices = parsedContent.find_all('span')
        # searchPriceElements = parsedContent.findAll('span', attrs={'class':'a-price'})
    def safeFloat(self, stringInput):
        try:
            return float(stringInput)
        except ValueError:
            return None

    def parsePrice(self, priceString):
        numString = priceString.replace('$', '')
        return AmazonWebScraper.safeFloat(self, numString)

    def parseRating(self, ratingString):
        # Parses a ratingstring into a float.

        # The first case:
        if(' out of 5 stars' in ratingString):
            numString = ratingString.replace(' out of 5 stars', '')
        else:
            # I don't know, it should be.
            return 0.0
        return AmazonWebScraper.safeFloat(self, numString)

    def parseShipPrice(self, shipPriceString, itemPrice):
        #Note: itemPrice must be a float

        notFree = False
        if('orders over $25' in shipPriceString):
            # check if qualifies for Amazon $25 free shipping
            if(itemPrice is not None and itemPrice > 25):
                return 0.0
            else:
                notFree = True

        elif(('free' in shipPriceString) and not notFree):
            return 0.0
        elif(' shipping' in shipPriceString):
            numString = shipPriceString.replace(' shipping', '')
            return AmazonWebScraper.safeFloat(self, numString)
        else:
            return None
        a = 0


    def getProducts(self):
        #for divTag in self.parsedContent.find_all('div', attrs={'class':'sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item s-asin sg-col-4-of-28 sg-col-4-of-16 AdHolder sg-col sg-col-4-of-20 sg-col-4-of-32'}, recursive = True):
        #    print('Found one.')
        Products = []


        for divTag in self.parsedContent.find_all('div', class_ = 'sg-col-inner', recursive=True):
            # print('Found one.')
            thisName = ''
            # boolean isValid tells if item has enough information to be added to the list
            isValid = True
            thisLinkPart = divTag.find('a', class_ = 'a-link-normal')
            if thisLinkPart is not None:
                thisNameParent = thisLinkPart.find('img')
                if thisNameParent is not None:
                    thisName = thisNameParent.attrs['alt']


            #print("Name: " + thisName)
            thisPriceParent = divTag.find('span', class_ = 'a-price')
            thisPriceString = ''
            if thisPriceParent is not None:
                thisPriceString = thisPriceParent.find('span', class_="a-offscreen").get_text()
            #print("Price: " + thisPriceString)

            thisUrlTag = divTag.find('a', class_="a-link-normal a-text-normal")
            thisUrl = ''
            if thisUrlTag is not None:

                thisUrl = thisUrlTag['href']

            # Rating and ship price have identical parent divs.

            ratingAndShipPrice = []
            ratingAndShipPrice = divTag.findAll('div', class_="a-section a-spacing-none a-spacing-top-micro")
            thisShipPriceString = ''
            thisRatingString = ''

            if(len(ratingAndShipPrice) > 1):

                thisPriceShipParentParent = ratingAndShipPrice[1]
                if thisPriceShipParentParent is not None:
                    #Parent of ship price is: <div class="a-row">
                    thisPriceShipParent = thisPriceShipParentParent.find('div', class_='a-row')

                    possiblePriceShipTags = thisPriceShipParent.findAll('span')
                    for thisPriceShipTag in possiblePriceShipTags:

                        if ('aria-label' in thisPriceShipTag.attrs):
                            thisShipPriceString = thisPriceShipTag['aria-label']
                else:
                    #probably not a real listing
                    isValid = False

                thisRatingParentParent = ratingAndShipPrice[0]
                if thisRatingParentParent is not None:
                    thisRatingParent = thisRatingParentParent.find('div', class_='a-row a-size-small')
                    possibleRatingTags = thisRatingParent.findAll('span', class_='a-icon-alt')

                    for thisRatingTag in possibleRatingTags:

                        thisRatingString = thisRatingTag.get_text()
                    else:
                        #print("could not find the span")
                        # do nothing
                        a = 0

                # else:
                #         print("could not find immediate div parent")

            thisUrl = 'https://amazon.com' + thisUrl

            # print("Url: " + thisUrl)

            thisPrice = AmazonWebScraper.parsePrice(self, thisPriceString)
            thisShipPrice = AmazonWebScraper.parseShipPrice(self, thisShipPriceString, thisPrice)
            thisRating = AmazonWebScraper.parseRating(self, thisRatingString)
            Products.append(Product(thisName, thisPrice, thisShipPrice, thisUrl, thisRating, "Amazon"))
        return Products
    def getProductsAndPrint(self):

        for thisProduct in self.getProducts():
            print(thisProduct.toString())


    def printContents(self):
        print(self.parsedContent.prettify())


    # The following are all temporary functions for testing.
    def getLinksTest(self):
        newList = []
        print(newList)
        for link in self.parsedContent.find_all('a'):
            print(link.get('href'))
    def getSpansTest(self):
        for spanTag in self.parsedContent.find_all('span', recursive=True):
            print(spanTag)
    def getDivsTest(self):
        #for divTag in self.parsedContent.find_all('div', attrs={'class':'sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item s-asin sg-col-4-of-28 sg-col-4-of-16 AdHolder sg-col sg-col-4-of-20 sg-col-4-of-32'}, recursive = True):
        #    print('Found one.')


        for divTag in self.parsedContent.find_all('div', class_ = 'sg-col-inner', recursive=True):
            print('Found one.')
    def tempTest(self):
        for header in self.parsedContent.find_all('h1'):
            print("Headline 1: ")
            print(header)

        for divTag in self.parsedContent.find_all('div', attrs={'class': "s-desktop-width-max s-desktop-content sg-row"}, recursive=True):
            print('Found one.')
    def getVisibleDivs(self):
        print("got here.")
        for divTag in self.parsedContent.find_all('div',recursive=True):

            print("found a div")
            print(divTag.attrs)
    def allTags(self):
        for tag in self.parsedContent.find_all(True):
            print(tag.name)


