import requests


def computer_milano_scraper(index, model, prices):
    topics = ["", "rtx ", "intel core "]
    # do not modify this
    url_base = "https://computer.milano.it/catalogsearch/result/index/"
    search = topics[index] + model
    payload = {'dir': 'asc', 'limit': '15', 'order': 'price', 'cat': '14', 'q': search}

    # connect to site and get data
    response = requests.get(url=url_base, params=payload)
    # html file in string format
    raw = response.text

    doc = raw.split('<h2 class="product-name"><')
    for elem in doc[1:]:
        title = elem[elem.find('>') + 1:elem.find('<')]

        elem = elem.split('Prezzo ivato')[1]
        i = elem.find("€") + 2
        price = elem[i:i + 7]
        # delete spaces
        price = price.strip()
        price = price.replace(".", "")
        price = price.replace(",", ".")

        prices += [(float(price), title)]

    return prices
