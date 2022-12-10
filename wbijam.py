from requests import get
from cda import CDA
from re import compile, findall
import asyncio
import aiohttp

from typing import List, Dict


async def async_get(url: str):
    async with aiohttp.ClientSession() as session:
        async with await session.get(url) as request:
            data = await request.read()
            en = request.get_encoding()

    return data.decode(en)


class video:
    def __init__(self, link: str, ref: str, name: str):
        self.link = link
        self.ref = ref
        self.name = name
        self.rule1 = compile("<td class=\"center\">cda</td>\n *.*\n *.*rel=\"(.*?)\">")
        self.rule2 = compile("iframe src=\"(.*?)\"")

    def __str__(self):
        return self.name

    async def direct_link(self, quality="hd", retries=1) -> str:
        data = await async_get(self.link + self.ref)
        plink = findall(self.rule1, data)
        if not plink:
            return ""

        plink = plink[0]
        data = await async_get(self.link + "odtwarzacz-" + plink + ".html")
        plink = findall(self.rule2, data)
        if not plink:
            return ""

        plink = plink[0]
        plink = "https://www.cda.pl/video/" + plink.split('/')[-1]

        return CDA(plink).getRaw(quality, retries)


# I know the name is kinda confusing but "season" is also for listing: Movies, Openings, Endings
class season:
    def __init__(self, **kwargs):
        self.link = kwargs['link']
        self.ref  = kwargs['ref']
        self.full = kwargs['full']

        self.rule = compile("<tr class=\"lista_hover\">\n *<td><a href=\"(.*?)\"><.*?>(.*)</a></td>")

    def __str__(self):
        return self.full

    @property
    async def episodes(self) -> List[video]:
        data = await async_get(self.link + self.ref)
        episodes = findall(self.rule, data)
        episodes.reverse()

        res = list()
        for ref, name in episodes:
            kwargs = {"link": self.link, "ref": ref, "name": name}
            vid = video(**kwargs)
            res.append(vid)

        return res


class series:
    def __init__(self, **kwargs):
        self.link = kwargs["link"]
        self.short = kwargs["short"]
        self.full = kwargs["full"]

        self.rule = compile("<a href=\"(.*?)\">(.*?)</a>")

    def __str__(self):
        return self.full

    @property
    async def seasons(self) -> Dict[str, season]:
        data = await async_get(self.link)
        # splitting the regex search into a tighter sector so the rule does not have to be crazy
        sector = data.split("pmenu_naglowek_b", 1)[1].split("pmenu_naglowek_a")[0]

        links = findall(self.rule, sector)
        res = dict()
        for ref, full in links:
            kwargs = {'link': self.link, 'ref': ref, 'full': full}
            s = season(**kwargs)
            res[full.lower().replace(' ', '-')] = s

        return res


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

    async def get_top_series(self) -> Dict[str, series]:
        # splitting the regex search into a tighter sector so the rule does not have to be crazy
        sector = self.top_text.split("Lista anime", 1)[1].split("wsparcie-wsparcie.html", 1)[0]
        links = findall(self.top_rule, sector)  # link, short, full
        links.remove(('https://inne.wbijam.pl/', 'inne', 'Inne i porzucone'))  # getting rid of sub_link

        res = dict()
        for link, short, full in links:
            kwargs = {"link": link, "short": short, "full": full}
            s = series(**kwargs)
            # a bit dirty yes, but now we can link from full and short directly to its series
            res[full] = s
            res[short] = s

        return res

    async def get_sub_series(self) -> List[series]:
        # TODO: get sub series, similar to top_series
        ...


async def wbijam() -> _wbijam:
    wbj = _wbijam()
    await wbj.__async_init__()
    return wbj
