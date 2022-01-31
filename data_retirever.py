import asyncio
from threading import Thread

#import httpx

from Sites_info.Grab_info_Computer_Milano import computer_milano_scraper
from Sites_info.Grab_info_Computer_Valley import computer_valley_scraper
from Sites_info.Grab_info_Drako import drako_scraper
from Sites_info.Grab_info_Hardware_Planet import hardware_planet_scraper
from Sites_info.Grab_info_HWonline import hwonline_scraper
from Sites_info.Grab_info_Nexths import nexths_scraper
from Sites_info.Grab_info_PC_OK import pc_ok_scraper
from Sites_info.Grab_info_VG_Informatica import vg_informatica_scraper
from Sites_info.sites import SiteObjs


async def data_retriever(topic: int, model):
    """Retrieves the information about each site and return a list of tuples. The first element of each tulpe is a string
    with the name of a site, the second element contains a list of products from that site."""
    # OLD
    Computer_Milano = []
    Computer_Valley = []
    Drako = []
    Hardware_Planet = []
    HWonline = []
    Nexths = []
    PC_ok = []
    VG_Informatica = []

    threads = [None] * 8
    threads[0] = Thread(target=computer_milano_scraper, args=(topic, model, Computer_Milano))
    threads[1] = Thread(target=computer_valley_scraper, args=(topic, model, Computer_Valley))
    threads[2] = Thread(target=drako_scraper, args=(topic, model, Drako))
    threads[3] = Thread(target=hardware_planet_scraper, args=(topic, model, Hardware_Planet))
    threads[4] = Thread(target=hwonline_scraper, args=(topic, model, HWonline))
    threads[5] = Thread(target=nexths_scraper, args=(topic, model, Nexths))
    threads[6] = Thread(target=pc_ok_scraper, args=(topic, model, PC_ok))
    threads[7] = Thread(target=vg_informatica_scraper, args=(topic, model, VG_Informatica))

    for foo in threads:
        foo.start()
    for foo in threads:
        foo.join()

    return [("Computer_Milano", Computer_Milano),("Computer_Valley", Computer_Valley), ("Drako", Drako), ("Hardware_Planet", Hardware_Planet),
    ("HWonline", HWonline), ("Nexths", Nexths), ("PC_ok", PC_ok), ("VG_informatica", VG_Informatica)]
    # NEW
    sites = SiteObjs().sites
    all_prices = []

    # set query topic
    for site in sites:
        site.set_url(topic, model)

    # ERROR: does not accept {'':''} as a header
    # get all html files
    async with httpx.AsyncClient() as client:
        tasks = (client.get(url=site.url_base, params=site.payload, headers=site.headers) for site in sites)
        reqs = await asyncio.gather(*tasks)  # TODO: httpx.ReadTimeout

    htmls = [req.text for req in reqs]

    # TODO: parallelize this loop for performance
    # parse all files and get names and prizes of all products
    for html, site, prices in zip(htmls, sites, all_prices):
        site.parser(html, prices)

    return [(name.__class__.__name__, prices) for name, prices in zip(sites, all_prices)]
