def checkProducts(inProducts):
  outProducts = []
  for product in inProducts:

    if product.name is not None and (len(product.name) > 6):
      if product.url is not None and product.url != "":
        outProducts.append(product)
        

  return outProducts
        