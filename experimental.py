import asyncio
import aiofiles
import aiohttp

from cda import CDA
from wbijam import wbijam
import argparse
import multiprocessing as mp


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

def parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="download entire series from wbijam.pl")
    # TODO: redo whole argument system, keep in mind the goal of not having to open the browser

    #  // major behaviour changers [MBC]
    # switch to show all available series on wbijam.pl
    parser.add_argument("--list-series", action="store_true", help="list available series on wbijam.pl")
    #  an option for those especially hungry for data
    parser.add_argument("--devour", action="store_true", help="'when i said everything, i meant EVERYTHING' (download every series, every opening, every ending possible)")
    # an option for listing possible episodes of a series
    parser.add_argument("--list-episodes", type=str, required=False, help="list available episodes of a series, syntax [short] or [full_name] (_ for any space)", default="unspecified")

    #  // optional
    # an option for specifying 'episodes'
    parser.add_argument("-e", type=str, required=False, help="specify 'episodes' to download, syntax: '1,2,3,4,10,11,12' or '1-4,10-12' will only download episodes 1, 2, 3, 4, 10, 11 and 12", default="all")
    # an option for specifying quality, 1 of 4 possible
    parser.add_argument("-q", type=str, required=False, help="specify quality, one of four possible: 'vl'(very low), 'lq'(low), 'sd'(standard (720p)), 'hd'(high (1040p)) (not always all are available for an episode)", default="highest")
    # an option to change the save path
    parser.add_argument("-p", type=str, required=False, help="specify output path, default used is current execution path", default="./")
    # an option to create content lists
    parser.add_argument("-c", action="store_true", help="create a content list")
    # an option for specifying the amount of cores to use
    parser.add_argument("-k", type=int, required=False, help="specify amount of cores to use, check: min(n_of_cores, given_number)", default=1)

    #  // required, with the exception when major behaviour changers are used
    parser.add_argument("series", type=str, nargs="?", default="unspecified")
    parser.add_argument("season", type=str, nargs="?", default="unspecified")

    return parser


async def download(url: str, path: str, name: str) -> None:  # IO
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as request:
            data = await request.read()

    async with aiofiles.open(path + '/' + name + '.mp4', 'wb') as file:
        await file.write(data)


async def main() -> None:  # IO
    args = parser().parse_args()
    print(args)  # debug
    wbj = await wbijam()

    #  // additional checks
    if not wbj.ok:
        ...  # todo: exit with error [server]

    if not (args.list_series or args.devour) and (args.series == "unspecified" or args.season):
        ...  # todo: exit with error [arg conflict]

    #  // basic setup
    top_series = await wbj.get_top_series()
    syb_series = await wbj.get_sub_series()

    #  // MBC
    if args.list_series:  # todo: also include sub series
        ...  # todo:  list series, exit

    if args.list_episodes != "unspecified":
        ...  # todo: list episodes of a series, exit

    if args.devour:
        ...  # todo: devour, exit




if __name__ == '__main__':
    asyncio.run(main())
