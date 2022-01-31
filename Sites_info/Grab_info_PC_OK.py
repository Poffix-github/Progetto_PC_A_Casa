import requests


def pc_ok_scraper(index, model, prices):
    topics = ["", "rtx ", "intel core "]
    # do not modify this
    url_base = "https://www.pcokomegna.it/s"
    search = topics[index] + model
    payload = {'item': '24', 'q': search}

    # connect to site and get data
    response = requests.get(url=url_base, params=payload)
    # html file in string format
    raw = response.text

    doc = raw.split('<h3>')
    for elem in doc[1:]:
        title = elem[0:elem.find(" <")]
        title = title[:50] if len(title) > 50 else title

        if title.find("GAMING PC") == -1 & title.find("GAMING-PC") == -1:
            i = elem.find('d">&euro; ')
            if i == -1:
                i = elem.find(' ">&euro; ')
            i += 10
            price = elem[i:i + elem[i:].find("<")]
            # problem with thousands separator
            price = price.replace(".", "")
            price = price.replace(",", ".")

            prices += [(float(price), title)]
    return prices
