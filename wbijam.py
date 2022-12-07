from requests import get
from cda import CDA
from re import compile, findall
import asyncio
import aiohttp

from typing import List

# TODO: async this


async def async_get(url: str):
    async with aiohttp.ClientSession() as session:
        async with await session.get(url) as r:
            data = await r.read()

    return data

class video:
    def __init__(self, link):
        pass


class series:
    def __init__(self, **kwargs):
        self.link = kwargs["link"]
        self.short = kwargs["short"]
        self.full = kwargs["full"]

    @property
    async def movies(self) -> List[video]:
        ...

    @property
    async def episodes(self) -> List[video]:
        ...

    @property
    async def openings(self) -> List[video]:
        ...

    @property
    async def endings(self) -> List[video]:
        ...


class _cl_wbijam:
    def __init__(self):
        self.top_link = "https://wbijam.pl"
        self.sub_link = "https://inne.wbijam.pl"

    async def __async_init__(self):
        if get(self.top_link).ok:
            self.ok = True
            self.top_text = get(self.top_link).text
            self.sub_text = get(self.sub_link).text
        else:
            self.ok = False
            self.top_text = None
            self.sub_text = None

    async def get_top_series(self) -> List[series]:
        sector = self.top_text.split("Lista anime", 1)[1].split("wsparcie-wsparcie.html", 1)[0]
        links = findall("<a href=\"(.*?)\" class=\"sub_link\" rel=\"(.*?)\">(.*?)</a>[^,]", sector)  # link, short, full
        links.remove(('https://inne.wbijam.pl/', 'inne', 'Inne i porzucone'))  # getting rid of sub_link

        res = list()
        for link, short, full in links:
            kwargs = {"link": link, "short": short, "full": full}
            res.append(series(**kwargs))

        return res

    async def get_sub_series(self) -> List[series]:
        ...


async def wbijam() -> _cl_wbijam:
    wbj = _cl_wbijam()
    await wbj.__async_init__()
    return wbj



w = wbijam()
print(await async_get("https://chainsawman.wbijam.pl/"))

