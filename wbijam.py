from requests import get
from cda import CDA
from re import compile, findall
import asyncio
import aiohttp

from typing import List

# TODO: async this


async def async_get(url: str):
    async with aiohttp.ClientSession() as session:
        async with await session.get(url) as request:
            data = await request.read()

    return str(data)


class video:
    def __init__(self, link):
        pass


class season:
    def __init__(self):
        pass

    def __str__(self):
        return  # name

    @property
    async def episodes(self) -> List[video]:
        ...

    @property
    async def openings(self) -> List[video]:
        ...

    @property
    async def endings(self) -> List[video]:
        ...


class series:
    def __init__(self, **kwargs):
        self.link = kwargs["link"]
        self.short = kwargs["short"]
        self.full = kwargs["full"]

    #  todo: think of the appropriate place for movies, be wary of arg layout in experimental.py
    @property
    async def movies(self) -> List[video]:
        ...

    def __str__(self):
        return self.full

    async def seasons(self) -> List[season]:



        ...


class _wbijam:
    def __init__(self):
        self.top_link = "https://wbijam.pl"
        self.sub_link = "https://inne.wbijam.pl"

        # regex rules for finding links
        self.top_rule = compile("<a href=\"(.*?)\" class=\"sub_link\" rel=\"(.*?)\">(.*?)</a>[^,]")
        self.sub_rule = compile("")

    async def __async_init__(self):
        if get(self.top_link).ok:
            self.ok = True
            self.top_text, self.sub_text = await asyncio.gather(
                async_get(self.top_link),
                async_get(self.sub_link))
        else:
            self.ok = False
            self.top_text = None
            self.sub_text = None

    async def get_top_series(self) -> List[series]:
        # splitting the regex search into a tighter sector so the rule does not have to be crazy
        sector = self.top_text.split("Lista anime", 1)[1].split("wsparcie-wsparcie.html", 1)[0]
        links = findall(self.top_rule, sector)  # link, short, full
        links.remove(('https://inne.wbijam.pl/', 'inne', 'Inne i porzucone'))  # getting rid of sub_link

        res = list()
        for link, short, full in links:
            kwargs = {"link": link, "short": short, "full": full}
            res.append(series(**kwargs))

        return res

    async def get_sub_series(self) -> List[series]:
        ...


async def wbijam() -> _wbijam:
    wbj = _wbijam()
    await wbj.__async_init__()
    return wbj


async def main():
    w = await wbijam()
    series = await w.get_top_series()
    for s in series:
        print(s.full)


if __name__ == '__main__':
    asyncio.run(main())
