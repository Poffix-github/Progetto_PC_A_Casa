import requests


def hardware_planet_scraper(index, model, prices):
    topics = ["", "nvidia geforce rtx ", "intel core "]
    # do not modify this
    url_base = "https://www.hardware-planet.it/ricerca"
    search = topics[index] + model
    payload = {'controller': 'search', 'orderby': 'position', 'orderway': 'desc', 'order': 'product.price.asc',
               'search_query': search}

    # connect to site and get data
    response = requests.get(url=url_base, params=payload)
    # html file in string format
    raw = response.text

    doc = raw.split('<div class="item col-xs-6 col-sm-4 col-md-4 col-lg-4">')
    for elem in doc[1:]:
        if elem.find("Esaurito") == -1:
            elem = elem.split('<div class="product_name" itemprop="name">')[1]
            elem = elem.split('.html">')[1]
            title = elem[0:elem.find("<")]

            elem = elem.split('<span itemprop="price" class="price">')[1]
            price = elem[0:elem.find("\xa0")]
            # for float conversion
            price = price.replace(".", "")
            price = price.replace(",", ".")

            prices += [(float(price), title)]
    return prices
