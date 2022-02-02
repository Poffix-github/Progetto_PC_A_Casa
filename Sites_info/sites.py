class Site:

    def __init__(self, url, topics, query='', payload=None, headers=None):
        self.url_base: str = url
        self.payload: dict[str, str] = payload
        self.headers: dict[str, str] = headers
        self.topics: list[str] = topics
        self.__key = query

    def set_url(self, index, model):
        self.payload[self.__key] = self.topics[index] + model

    def parser(self, html):
        pass


class ComputerMilano(Site):

    def parser(self, html):
        prices = []
        doc = html.split('<h2 class="product-name"><')
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


class ComputerValley(Site):

    def parser(self, html):
        prices = []
        doc = html.split('data-price="')
        for elem in doc[1:]:
            if elem.find("Non disponibile") == -1:
                price = elem[0:elem.find('"')]

                elem = elem.split('<meta itemprop="description" content="')[1]
                title = elem[0:elem.find('"')]

                prices += [(float(price), title)]
        return prices


class Drako(Site):

    def parser(self, html):
        # strange codec on euro (€) symbol, if you include it in the string the program doesn't recognize it and
        # .split() doesn't work
        prices = []
        doc = html.split('<div class="product_title"><a title="')
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


class HardwarePlanet(Site):

    def parser(self, html):
        prices = []
        doc = html.split('<div class="item col-xs-6 col-sm-4 col-md-4 col-lg-4">')
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


class HWOnline(Site):

    def parser(self, html):
        prices = []
        doc = html.split('<div class="product-list">')[-1]
        doc = doc.split('title     = "')
        for elem in doc[1:]:
            if elem.find('class="availability-dot availability-dot-unavailable"') == -1:
                title = elem[0:elem.find(' (')]

                if title.find("Computer portatile") == -1:
                    elem = elem.split('ce" content="')[1]
                    price = elem[0:elem.find('"')]

                    prices += [(float(price), title)]
        return prices


class Nexths(Site):

    def parser(self, html):
        prices = []
        # strange codec on euro (€) symbol, if you include it in the string the program doesn't recognize it and
        # .split() doesn't work
        doc = html.split('<p class="gallery-descrbreve">')
        for elem in doc[1:]:
            if elem.find("DISPONIBILE in pronta consegna") != -1:
                title = elem[0:elem.find(' <')]

                elem = elem.split('oswald">&euro; ')[1]
                price = elem[0:elem.find("<")]
                price = price.replace(".", "")
                price = price.replace(",", ".")

                prices += [(float(price), title)]
        return prices

    # this site is fucked up
    def set_url(self, index, model):
        self.url_base += self.topics[index] + model


class PcOk(Site):

    def parser(self, html):
        prices = []
        doc = html.split('<h3>')
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


class VgInformatica(Site):

    def parser(self, html):
        prices = []
        doc = html.split('<div class="featured-info mb0">')
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


class SiteObjs:
    """contains one object for each site"""

    computer_milano = ComputerMilano(
                        url="https://computer.milano.it/catalogsearch/result/index/",
                        topics=["", "rtx ", "intel core "],
                        query='q',
                        payload={'dir': 'asc', 'limit': '15', 'order': 'price', 'cat': '14'})

    computer_valley = ComputerValley(
                        url="https://www.computervalley.it/advanced_search_result.php",
                        topics=["", "geforce rtx ", "intel core "],
                        query='keywords',
                        payload={'search_in_description': '0'})

    drako = Drako(
                        url="https://www.drako.it/drako_catalog/advanced_search_result.php",
                        topics=["", "geforce rtx ", "intel core "],
                        query='keywords',
                        payload={})

    hardware_planet = HardwarePlanet(
                        url="https://www.hardware-planet.it/ricerca",
                        topics=["", "nvidia geforce rtx ", "intel core "],
                        query='search_query',
                        payload={'controller': 'search', 'orderby': 'position', 'orderway': 'desc',
                                 'order': 'product.price.asc'})

    hwonline = HWOnline(
                        url='https://www.hwonline.it/ricerca',
                        topics=["", "nvidia geforce rtx ", "intel core "],
                        query='s',
                        payload={'controller': 'search', 'order': 'product.price.asc'})

    nexths = Nexths(
                        url="https://www.nexths.it/products/getSkuFromLev/rpp/48/page/1/sort/prezzoa/l1/",
                        topics=["", "Schede%20Video/query/geforce rtx ", "Cpu/query/intel core "],
                        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, ''like '
                                               'Gecko) Chrome/56.0.2924.76 ''Safari/537.36'})
    # https://www.nexths.it/products/getSkuFromLev/query/geforce%20rtx%203070/l1/Schede%20Video/page/1/rpp/48/sort
    # /prezzoa

    pc_ok = PcOk(
                        url="https://www.pcokomegna.it/s",
                        topics=["", "rtx ", "intel core "],
                        query='q',
                        payload={'item': '24'})

    vg_informatica = VgInformatica(
                        url="https://www.vginformatica.com/search",
                        topics=["", "rtx ", "intel core "],
                        query='q',
                        payload={'item': '24'})

    sites = [computer_milano, computer_valley, drako, hardware_planet, hwonline, nexths, pc_ok, vg_informatica]
