import requests


def vg_informatica_scraper(index, model, prices):
    topics = ["", "rtx ", "intel core "]
    # do not modify this
    url_base = "https://www.vginformatica.com/search"
    search = topics[index] + model
    payload = {'item': '24', 'q': search}

    # connect to site and get data
    response = requests.get(url=url_base, params=payload)
    # html file in string format
    raw = response.text

    doc = raw.split('<div class="featured-info mb0">')
    for elem in doc[1:]:
        elem = elem.lstrip("\n\t<")
        title = elem[elem.find(">") + 1: elem.find("<")]

        if title.find("PC DA GAMING ASSEMBLATO") == -1:
            if elem.find('pb1">&euro; ') != -1:
                elem = elem.split('pb1">&euro; ')[1]
            else:
                elem = elem.split('price_discount">&euro; ')[1]
            price = elem[0:elem.find('<')]
            price = price.replace(".", "")
            price = price.replace(",", ".")

            prices += [(float(price), title)]
    return prices
