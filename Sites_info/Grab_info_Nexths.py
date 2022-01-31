import requests


def nexths_scraper(index, model, prices):
    topics = ["", "geforce rtx ", "intel core "]
    # do not modify this
    url_base = "https://www.nexths.it/products/getSkuFromLev/rpp/48/page/1/sort/prezzoa/query/"
    search = topics[index] + model
    # site doesn't like connections from non browsers entites
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 '
                      'Safari/537.36'}  # This is chrome

    # connect to site and get data
    response = requests.get(url=url_base + search, headers=headers)
    # html file in string format
    raw = response.text

    # strange codec on euro (€) symbol, if you include it in the string the program doesn't recognize it and .split()
    # doesn't work
    doc = raw.split('<p class="gallery-descrbreve">')
    for elem in doc[1:]:
        if elem.find("DISPONIBILE in pronta consegna") != -1:
            title = elem[0:elem.find(' <')]

            elem = elem.split('oswald">&euro; ')[1]
            price = elem[0:elem.find("<")]
            price = price.replace(".", "")
            price = price.replace(",", ".")

            prices += [(float(price), title)]
    return prices
