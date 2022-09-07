# coding: utf-8

import requests
import re
from json import loads
from time import sleep


class CDA:
    def __init__(self, url: str):
        self.url = url
        _r = requests.get(url)
        rawData = _r.text

        self.qualities: dict = loads(re.search("\"qualities\":(\{.*?\})", rawData).groups()[0])
        self.videoHash = re.search("hash2\":\"([a-z0-9]*)\"", rawData).groups()[0]
        self.videoKey = re.search("setTimeout\(function\(\) \{\n.*\n.*ts:\"(\d*)\"", rawData).groups()[0]
        self.playerID = url.split('/')[-1]

    def getRaw(self, ql: str = "hd"):
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

        res = loads(requests.post(url=self.url, json=js).text)["result"]["resp"]
        if res == "bad key":
            sleep(3)
            return self.getRaw(ql)
        else:
            return res

