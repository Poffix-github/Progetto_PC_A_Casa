import requests


def computer_valley_scraper(index, model, prices):
    topics = ["", "geforce rtx ", "intel core "]
    # do not modify this
    url_base = "https://www.computervalley.it/advanced_search_result.php"
    search = topics[index] + model
    payload = {'search_in_description': '0', 'keywords': search}

    # connect to site and get data
    response = requests.get(url=url_base, params=payload)
    # html file in string format
    raw = response.text

    doc = raw.split('data-price="')
    for elem in doc[1:]:
        if elem.find("Non disponibile") == -1:
            price = elem[0:elem.find('"')]

            elem = elem.split('<meta itemprop="description" content="')[1]
            title = elem[0:elem.find('"')]

            prices += [(float(price), title)]
    return prices
