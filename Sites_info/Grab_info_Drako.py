import requests


def drako_scraper(index, model, prices):
    topics = ["", "geforce rtx ", "intel core "]
    # do not modify this
    url_base = "https://www.drako.it/drako_catalog/advanced_search_result.php"
    search = topics[index] + model
    payload = {'keywords': search}

    # connect to site and get data
    response = requests.get(url=url_base, params=payload)
    # html file in string format
    raw = response.text

    # strange codec on euro (€) symbol, if you include it in the string the program doesn't recognize it and .split()
    # doesn't work
    doc = raw.split('<div class="product_title"><a title="')
    for elem in doc[1:]:
        if elem.find(">disponibile") != -1:
            title = elem[0:elem.find('"')]

            if elem.find('y"><span>') != -1:
                elem = elem.split('y"><span>')[1]
            else:
                elem = elem.split('w"><span>ora ')[1]

            price = elem[2:elem.find("<")]
            # problem with thousands separator
            price = price.replace(".", "")
            price = price.replace(",", ".")

            # price before title! (to sort by the former)
            prices += [(float(price), title)]

    prices.sort()
    return prices
