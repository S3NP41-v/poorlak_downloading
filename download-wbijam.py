from cda import CDA
from wbijam import wbijam
import argparse
import requests
import multiprocessing


def _download(data: tuple) -> None:  # I/O
    clink = data[0]
    k = data[1]

    c = CDA(clink)
    raw_link = c.getRaw(ql=args.q)

    print(f"#{k} downloading data from {clink} [{raw_link}] ...")  # debug
    r = requests.get(raw_link)

    print(f"#{k} creating file: " + args.o + '/' + f"{k}-{c.playerID}.mp4")  # debug
    with open(args.o + '/' + f"{k}-{c.playerID}.mp4", "wb") as f:
        f.write(r.content)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="download entire series from wbijam.pl")
    parser.add_argument("-m", type=str, required=True, help="specify the main link, example: https://danmachi.wbijam.pl")
    parser.add_argument("-s", type=str, required=True, help="specify the season, example: pierwsza_seria.html")

    parser.add_argument("-q", required=False, choices=["hd", "sd", "lq", "vl"], help="specify the quality to download [default 'hd']", default="hd")
    parser.add_argument("-o", type=str, required=False, help="specify the path to download to")

    parser.add_argument("-t", type=int, required=False, help="amount of threads to use while downloading [default 4]", default=4)

    args = parser.parse_args()

    # some checks
    if not requests.get(args.m).ok:
        exit(f"main link is not responding: {args.m}")

    if not requests.get(args.m + '/' + args.s).ok:
        exit(f"season is not responding: {args.m}/{args.s}")

    if not args.o:
        args.o = "./"

    w = wbijam(main_link=args.m, series=args.s)

    with multiprocessing.Pool(args.t) as pool:
        clinks = w.get_cLinks()
        pool.map(_download, zip(clinks, list(range(len(clinks)))), chunksize=1)

