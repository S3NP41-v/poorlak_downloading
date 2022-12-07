from requests import get
from cda import CDA
from re import compile, findall

# TODO: async this


class video:
    def __init__(self, link):
        pass


class series:
    def __init__(self, short: str, name=None):
        pass

    @property
    def movies(self) -> [video]:
        ...

    @property
    def episodes(self) -> [video]:
        ...

    @property
    def openings(self) -> [video]:
        ...

    @property
    def endings(self) -> [video]:
        ...


class wbijam:
    def __init__(self):
        self.top_link = "https://wbijam.pl"
        self.sub_link = "https://inne.wbijam.pl"
        if get(self.top_link).ok:
            self.ok = True
            self.top_text = get(self.top_link).text
            self.sub_text = get(self.sub_link).text
        else:
            self.ok = False
            self.top_text = None
            self.sub_text = None

    def get_top_series(self) -> [series]:
        sector = self.top_text.split("Lista anime", 1)[1].split("wsparcie-wsparcie.html", 1)[0]
        links = findall("<a href=\"(.*?)\" class=\"sub_link\" rel=\"(.*?)\">(.*?)</a>[^,]", sector)  # link, short, full
        links.remove(('https://inne.wbijam.pl/', 'inne', 'Inne i porzucone'))  # getting rid of sub_link recursion


    def get_sub_series(self) -> [series]:
        ...




w = wbijam()

