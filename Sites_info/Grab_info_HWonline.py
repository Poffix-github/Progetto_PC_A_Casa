# TODO: aggiungi filtro per disponibilità (un pallino rosso, verde o arancione minuscolo, arancione significa "ultimi
#  pezzi")
# BUG: se non trova nessun prodotto da IndexOutOfBound

import requests


def hwonline_scraper(index, model, prices):
    topics = ["", "nvidia geforce rtx ", "intel core "]
    # do not modify this
    url_base = "https://www.hwonline.it/ricerca"
    search = topics[index] + model
    payload = {'controller': 'search', 'order': 'product.price.asc', 's': search}

    # connect to site and get data
    response = requests.get(url=url_base, params=payload)
    # html file in string format
    raw = response.text

    doc = raw.split('<div class="product-list">')[-1]
    doc = doc.split('title     = "')
    for elem in doc[1:]:
        title = elem[0:elem.find(' (')]

        if title.find("Computer portatile") == -1:
            elem = elem.split('ce" content="')[1]
            price = elem[0:elem.find('"')]

            prices += [(float(price), title)]
    return prices
