from cda import CDA
from wbijam import wbijam
import argparse
import requests
import re
import multiprocessing
from os import system
from sys import platform
from time import time, sleep


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


class errors(Exception):
    ...


class incorrectLink(errors):
    def __init__(self, link: str):
        self.link = link
        super().__init__(f"link '{link}' is incorrect")

    def __str__(self):
        return f"'{self.link}' -/-> 'https://[a-z0-9]*\.wbijam\.pl'"


class serverNotOk(errors):
    def __init__(self, response: int):
        self.response = response
        super().__init__(f"server returned {response}")

    def __str__(self):
        return f"unexpected server response [{self.response}]"


def main():
    parser = argparse.ArgumentParser(description="download entire series from wbijam.pl")
    # TODO: redo whole argument system, keep in mind the goal of not having to open the browser

    #  // major behaviour changers
    # switch to show all available series on wbijam.pl
    parser.add_argument("--list-series", action="store_false", type=bool, required=False, help="list available series on wbijam.pl", default=False)
    #  an option for those especially hungry for data
    parser.add_argument("--devour", action="store_false", type=bool, required=False, help="'when i said everything, i meant EVERYTHING' (download every series, every opening, every ending possible)", default=False)

    #  // optional
    # an option for specifying 'episodes'
    parser.add_argument("-e", type=str, required=False, help="specify 'episodes' to download, syntax: '1,2,3,4,10,11,12' or '1-4,10-12' will only download episodes 1, 2, 3, 4, 10, 11 and 12", default="all")
    # an option for specifying quality, 1 of 4 possible
    parser.add_argument("-q", type=str, required=False, help="specify quality, one of four possible: 'vl'(very low), 'lq'(low), 'sd'(standard (720p)), 'hd'(high (1040p)) (not always all are available for an episode)", default="highest")
    # an option for listing possible episodes of a series
    parser.add_argument("-l", action="store_false", type=bool, required=False, help="list available episodes of a series", default=False)
    # an option to change the save path
    parser.add_argument("-p", type=str, required=False, help="specify output path, default used is current execution path", default="./")
    # an option to create content lists
    parser.add_argument("-c", action="store_false", type=bool, required=False, help="create a content list", default=False)
    # an option for specifying the amount of cores to use
    parser.add_argument("-k", type=int, required=False, help="specify amount of cores to use, check: min(n_of_cores, given_number)", default=1)

    #  // required, with the exception when major behaviour changers are used
    # Series, either a name, or an ID, throws an error if is MBC is not used and series unspecified
    parser.add_argument("series", type=str, nargs="?", default="unspecified")

    args = parser.parse_args()

    #  // additional checks
    if ~(args.list_series | args.devour) & args.series == "unspecified":
        raise Exception("...")  # TODO




if __name__ == '__main__':
    main()
