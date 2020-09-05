from django.http import HttpResponse
from django.shortcuts import render
#from django.http import Q
from webScrapers.ebayWebScraper import EbayWebScraper
from webScrapers.amazonWebScraper import AmazonWebScraper
from webScrapers.productClass import Product
from webScrapers.productChecker import checkProducts

def home(request):
  #template_name = 'homepage.html'
  #return render(request, 'homepage.html')
  # TEMP:
  searchTerm = None



  products = None
  template_name = 'homepage.html'
  context= {'productList': products, 'searchTerm': searchTerm}
  return render(request, 'homepage.html', context)



def search(request):
  searchTerm = request.GET.get('q')
  products = []
  sources = []
  numResults = {"test":0}

  if(searchTerm is not None):

    scrapers = []
    #scraper = AmazonWebScraper(searchTerm)

    #print('compete!')
    #products = scraper.getProducts()

    scrapers.append(AmazonWebScraper(searchTerm))

    scrapers.append(EbayWebScraper(searchTerm))
    for scraper in scrapers:
      theseProducts = scraper.getProducts()
      scraperName = scraper.getDistributorName()
      sources.append(scraperName)

      numResults[scraperName] = 0 + len(theseProducts)
      for product in theseProducts:
        products.append(product)

    products = checkProducts(products)

  else:
    products = None

  template_name = 'homepage.html'
  context= {'productList': products, 'searchTerm': searchTerm, 'numResults':numResults, 'sources':sources}

  return render(request, 'homepage.html', context)


def search_results(request):
  return HttpResponse('Hello world')


def about(request):
  return render(request, 'aboutus.html')
