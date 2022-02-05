import asyncio
import httpx
from Sites_info.sites import SiteObjs


async def data_retriever(topic: int, model):
    """Retrieves the information about each site and return a list of tuples. The first element of each tulpe is a
    string with the name of a site, the second element contains a list of products from that site. """
    # NEW
    sites = SiteObjs().sites
    all_prices = []

    # set query topic
    for site in sites:
        site.set_url(topic, model)

    # get all html files
    async with httpx.AsyncClient(timeout=15.0) as client:
        tasks = (client.get(url=site.url_base, params=site.payload, headers=site.headers) for site in sites)
        reqs = await asyncio.gather(*tasks)

    htmls = [req.text for req in reqs]

    # parse all files and get names and prizes of all products
    for html, site in zip(htmls, sites):
        all_prices += [(site.__class__.__name__, site.parser(html))]

    return all_prices
