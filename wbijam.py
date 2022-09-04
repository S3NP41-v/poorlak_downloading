from cda import CDA
import requests
import multiprocessing.dummy
import re


class wbijam:
    def __init__(self, main_link: str, series: str):
        """
        :param main_link: example: 'https://danmachi.wbijam.pl'
        :param series:    example: 'pierwsza_seria.html'
        """

        self.main_link = main_link
        self.series = series

        self.web_text = requests.get(main_link + '/' + series).text

    def get_vLinks(self) -> list:  # no request
        links = re.findall("<td><a href=\"([a-z_0-9.-]*)\">", self.web_text)
        return list(map(lambda x: self.main_link + '/' + x, links))[::-1]


    def _get_cLink(self, vlink) -> str:  # request
        r = requests.get(vlink).text
        half_clink = self.main_link + '/odtwarzacz-' + re.search("cda.*\n.*\n.*?rel=\"([a-zA-Z0-9_]*)\">oglądaj", r).groups()[0] + '.html'

        r = requests.get(half_clink).text
        return re.search("<iframe src=\"(https://[a-z./0-9]*)\"", r).groups()[0]

    def get_cLinks(self) -> list:
        vlinks = self.get_vLinks()
        with multiprocessing.dummy.Pool(len(vlinks)) as pool:
            half_clink = pool.map(self._get_cLink, vlinks)

        return list(map(lambda x: f"https://www.cda.pl/video/{x.split('/')[-1]}", half_clink))
