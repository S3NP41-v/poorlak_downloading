from requests import get

from cda import CDA
from wbijam import wbijam
import argparse



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

    #  // major behaviour changers
    # switch to show all available series on wbijam.pl
    parser.add_argument("--list-series", action="store_true", help="list available series on wbijam.pl")
    #  an option for those especially hungry for data
    parser.add_argument("--devour", action="store_true", help="'when i said everything, i meant EVERYTHING' (download every series, every opening, every ending possible)")

    #  // optional
    # an option for specifying 'episodes'
    parser.add_argument("-e", type=str, required=False, help="specify 'episodes' to download, syntax: '1,2,3,4,10,11,12' or '1-4,10-12' will only download episodes 1, 2, 3, 4, 10, 11 and 12", default="all")
    # an option for specifying quality, 1 of 4 possible
    parser.add_argument("-q", type=str, required=False, help="specify quality, one of four possible: 'vl'(very low), 'lq'(low), 'sd'(standard (720p)), 'hd'(high (1040p)) (not always all are available for an episode)", default="highest")
    # an option for listing possible episodes of a series
    parser.add_argument("-l", action="store_false", required=False, help="list available episodes of a series", default=False)
    # an option to change the save path
    parser.add_argument("-p", type=str, required=False, help="specify output path, default used is current execution path", default="./")
    # an option to create content lists
    parser.add_argument("-c", action="store_true", help="create a content list")
    # an option for specifying the amount of cores to use
    parser.add_argument("-k", type=int, required=False, help="specify amount of cores to use, check: min(n_of_cores, given_number)", default=1)

    #  // required, with the exception when major behaviour changers are used
    parser.add_argument("series", type=str, nargs="?", default="unspecified")

    return parser


def main() -> None:  # IO
    args = parser().parse_args()
    print(args)  # debug
    wbj = wbijam()

    #  // additional checks
    if not wbj.ok:
        ...  # exit with error [server]

    if not (args.list_series or args.devour) and args.series == "unspecified":
        ...  # exit with error [arg conflict]

    #  // MBC
    if args.list_series:
        ...  # list series, exit

    if args.devour:
        ...  # devour, exit


if __name__ == '__main__':
    main()
