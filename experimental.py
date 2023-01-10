import asyncio
import os

import aiofiles
import aiohttp

from os import path, access
from cda import CDA
from wbijam import wbijam
import argparse


# contact the developer on discord: S3NP41#8357
# or via an email at: s3np41v@gmail.com
# ===========================================================================================================
# = all the code I share is completely free to use, include, change and share further without my permission =
# = long live the open source!                                                                              =
# ===========================================================================================================
#
# i make no promises, this code may break at any moment, use at your own risk, it relays a lot on the internal workings
# of cda.pl and wbijam.pl to not change, in the case you are very free to ask me to fix it
#
# have fun! And if you ever decide using my code for a project, do show me what you created, better yet, make it open source!


def parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="download entire series from wbijam.pl, current version is in active beta, bugs are to be expected")

    #  // major behaviour changers [MBC]
    # an option to show all available series on wbijam.pl
    parser.add_argument("--list-series", action="store_true", help="list available series on wbijam.pl")
    # an option for listing seasons of a series
    parser.add_argument("--list-seasons", type=str, required=False,
                        help="list available seasons of a series, syntax [short] or [full-name] (- for any space)",
                        default="unspecified")
    # an option for listing possible episodes of a season
    parser.add_argument("--list-episodes", type=str, required=False,
                        help="list available episodes of a season, syntax 'series/season' (both short and long versions are valid, '-' for any space)",
                        default="unspecified")
    #  an option for those especially hungry for data
    parser.add_argument("--devour", action="store_true",
                        help="'when i said everything, i meant EVERYTHING' (download every series, every opening, every ending possible)")

    #  // optional
    parser.add_argument("-v", action="store_true", help="verbose mode")
    # an option for specifying 'episodes'
    parser.add_argument("-e", type=str, required=False,
                        help="specify 'episodes' to download, syntax: '1,2,3,4,10,11,12' or '1-4,10-12' will only download episodes 1, 2, 3, 4, 10, 11 and 12",
                        default="all")
    # an option for specifying quality, 1 of 4 possible
    parser.add_argument("-q", type=str, required=False,
                        help="specify quality, one of four possible: 'vl'(very low), 'lq'(low), 'sd'(standard (720p)), 'hd'(high (1040p)) (not always all are available for an episode)",
                        default="highest")
    # an option to force download
    parser.add_argument("-f", action="store_true",
                        help="force download, do not skip downloading already existing files")
    # an option to change the save path
    parser.add_argument("-p", type=str, required=False,
                        help="specify output path, default used is current execution path", default="./")
    # an option to create content lists
    parser.add_argument("-c", action="store_true", help="create a content list")
    # an option for specifying the amount of cores to use
    parser.add_argument("-k", type=int, required=False,
                        help="specify amount of threads to use for downloading (warning, using more than the default value may lead to an IP ban)",
                        default=1)

    #  // required, with the exception when major behaviour changers are used
    parser.add_argument("series", type=str, nargs="?", default="unspecified")
    parser.add_argument("season", type=str, nargs="?", default="unspecified")

    return parser


class errors:
    def __init__(self):
        pass

    @staticmethod
    def network():
        print("[error][network] there seems to be no internet connection, or server is not responding")
        exit()

    @staticmethod
    def arg_conflict(*args):
        print(f"[error][arg-conflict] argument conflict with arguments: {args}")
        exit()

    @staticmethod
    def series_doesnt_exist(series):
        print(f"[error][series-doesnt-exist] provided series: '{series}' does not exist or cannot be found")
        exit()

    @staticmethod
    def season_doesnt_exist(season):
        print(f"[error][season-doesnt-exist] provided season: '{season}' does not exist or cannot be found")
        exit()

    @staticmethod
    def arg_syntax(argument):
        print(f"[error][arg-syntax] incorrect syntax for argument: {argument}")
        exit()

    @staticmethod
    def write_permission(path):
        print(f"[error][write-permission] insufficient permission to write to path: '{path}'")
        exit()

    @staticmethod
    def path_doesnt_exist(path):
        print(f"[error][path-doesnt-exist] provided path: '{path}' does not exist or cannot be found")
        exit()


# TODO: current idea for the download is to make it a class with asynchronous methods to download and
#     / report their speeds, current file etc. to the main method, then have another one for display.
#     / CHANGE THIS:
async def download(url: str, path: str, name: str) -> None:  # IO
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as request:
            data = await request.read()

    async with aiofiles.open(path + '/' + name + '.mp4', 'wb') as file:
        await file.write(data)


def debug(message: str, debug_on: bool) -> None:
    if debug_on:
        print(message)


async def main() -> None:  # IO
    args = parser().parse_args()
    debug_on = args.v
    exit_on_error = errors()
    debug(str(args), debug_on)
    wbj = await wbijam()

    #  // additional checks
    debug("checking server", debug_on)
    if not wbj.ok:
        exit_on_error.network()

    debug("checking arg conflict", debug_on)
    if (args.series == "unspecified" or args.season == "unspecified") and not (args.list_episodes != "unspecified" or args.list_seasons != "unspecified" or args.devour or args.list_series):
        exit_on_error.arg_conflict("list-series", "series", "season")

    #  // basic setup
    top_series = await wbj.get_top_series()
    sub_series = await wbj.get_sub_series()

    all_full = top_series["full"] | sub_series["full"]
    all_short = top_series["short"] | sub_series["short"]
    all_series = all_short | all_full
    debug(f"got all series, number: {len(top_series['full']) + len(sub_series['full'])}", debug_on)

    #  // MBC
    if args.list_series:  # list series, exit
        # todo: print only a screenfull of information at a time
        l = len(max(top_series["short"], key=lambda x: len(x)))
        print("[short]" + (' ' * (l - 7 + 1)) + "[full]")
        for short, full in zip(top_series["short"], top_series["full"]):
            print(short + (' ' * (l - len(short) + 1)) + full)

        exit()

    if args.list_seasons != "unspecified":  # list seasons of a series, exit
        sr = args.list_seasons
        sr = all_series.get(sr, None)
        if not sr:
            exit_on_error.series_doesnt_exist(args.list_seasons)

        seasons = await sr.seasons
        for season in seasons:
            print(season)

    if args.list_episodes != "unspecified":  # list episodes of a season, exit
        if args.list_episodes.count('/') != 1:
            exit_on_error.arg_syntax("list-episodes")

        _series, _season = args.list_episodes.split('/')
        _series = all_series.get(_series, None)
        if not _series:
            exit_on_error.series_doesnt_exist(args.list_seasons)

        _seasons = await _series.seasons
        _season = _seasons.get(_season, None)
        if not _season:
            exit_on_error.season_doesnt_exist(args.list_episodes.split('/')[1])

        episodes = await _season.episodes
        print(args.list_episodes)
        for k, ep in enumerate(episodes):
            if ep.ready:
                print(f"{k + 1}{' ' * ((len(str(len(episodes))) + 1) - (len(str(k + 1))))}{ep}")

        exit()

    if args.devour:
        ...  # todo: devour, exit
        exit()

    #  // Normal Behaviour

    # getting series, season and episodes
    _series = all_series.get(args.series, None)
    if not _series:
        exit_on_error.series_doesnt_exist(args.series)

    _seasons = await _series.seasons
    _season = _seasons.get(args.season, None)
    if not _season:
        exit_on_error.season_doesnt_exist(args.season)

    debug("getting episodes", debug_on)
    _episodes = await _season.episodes

    # getting episode range
    if args.e != "all":
        ep_range = list()
        for i in args.e.split(','):
            i: str
            if i.isdigit():  # ex: 1
                ep_range.append(int(i))
            elif i[0].isdigit() and i[1] == '-' and i[2].isdigit():  # ex: 1-2
                ep_range += range(*map(int, i.split('-')))
            else:
                exit_on_error.arg_syntax("-e")
    else:
        ep_range = range(1, len(_episodes) + 1)

    # checking if path exists
    if not path.exists(args.p):
        exit_on_error.path_doesnt_exist(args.p)

    # validating path for write access
    if not access(args.p, 2):
        exit_on_error.write_permission(args.p)

    # TODO: download

if __name__ == '__main__':
    asyncio.run(main())
