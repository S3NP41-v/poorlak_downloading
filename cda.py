# coding: utf-8

import requests
import re
from json import loads
from time import sleep
from os import popen

# contact the developer on discord: S3NP41#8357
#
# ===========================================================================================================
# = all the code I share is completely free to use, include, change and share further without my permission =
# = long live the open source!                                                                              =
# ===========================================================================================================
#
# i make no promises of it being fail proof as it relays a lot on the internal workings
# of cda.pl and wbijam.pl to not change, in the case you are very free to ask me to fix it
#
# have fun! And if you ever decide using my code, please do share what you created

class CDA:
    def __init__(self, url: str):
        # making sure to request via https
        self.url = url.replace('http:', 'https:')
        _r = requests.get(url)
        rawData = _r.text

        self.cookies = _r.cookies

        self.qualities: dict = loads(re.search("\"qualities\":(\{.*?\})", rawData).groups()[0])
        self.videoHash = re.search("hash2\":\"([a-z0-9]*)\"", rawData).groups()[0]
        self.videoKey = re.search("setTimeout\(function\(\) \{\n.*\n.*ts:\"(\d*)\"", rawData).groups()[0]
        self.playerID = url.split('/')[-1]

        _pairs = list()
        for k, v in self.cookies.get_dict().items():
            _pairs.append(f"{k}={v};")
        _ck = ' '.join(_pairs)


        self.headers = {'authority': 'www.cda.pl',
                        'accept': 'application/json, text/javascript, */*; q=0.01',
                        'accept-language': 'en,pl-PL;q=0.9,pl;q=0.8,en-US;q=0.7',
                        'content-type': 'application/json',
                        'dnt': '1',
                        'origin': 'https://www.cda.pl',
                        'referer': self.url,
                        'cookies': _ck,
                        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        'sec-fetch-dest': 'empty',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'same-origin',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/105.0.0.0 Safari/537.36',
                        'x-requested-with': 'XMLHttpRequest'}

    def getRaw(self, ql: str = "hd", retries=1):
        sortKey = lambda x: {"hd": 0, "sd": 1, "lq": 2, "vl": 3}[x]
        if ql not in self.qualities:
            ql = sorted(list(self.qualities.values()), key=sortKey)[0]

        js = {"jsonrpc": "2.0", "method": "videoGetLink",
              "params": [
                  f"{self.playerID}",
                  f"{ql}",
                  int(self.videoKey),
                  f"{self.videoHash}",
                  {}],
              "id": 3}


        res = requests.post(url=self.url, json=js, cookies=self.cookies.get_dict()).text
        res = loads(res)
        res = res["result"]["resp"]

        if res == "bad key":
            sleep(3 * min(retries, 20))
            return self.getRaw(ql, retries=retries + 1)
        else:
            return res
