from cda import CDA
from wbijam import wbijam
import argparse
import requests
import multiprocessing
from os import system
from sys import platform, stdout


def download(k: int, clink: str, quality: str, path: str, list_only: bool) -> str:  # I/O + returning raw link
    c = CDA(clink)
    raw = c.getRaw(ql=quality)
    filename = f"{k}-{c.playerID}.mp4"

    print(f"\x1b[{str(k + 2)};0H\x1b[2KDownloading:  {clink} -> {path}{filename}", end='')
    stdout.flush()

    if not list_only:
        data = requests.get(raw)
        print(f"\x1b[{str(k+2)};0H\x1b[2KWriting file: {clink} -> {path}{filename}", end='')
        stdout.flush()
        with open(f"{path}/{filename}", "wb") as f:
            f.write(data.content)

    # otherwise only return raw link

    print(f"\x1b[{str(k+2)};0H\x1b[2KCompleted:    {clink} -> {path}{filename}", end='')
    stdout.flush()

    return raw


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="download entire series from wbijam.pl")
    parser.add_argument("-m", type=str, required=True, help="specify the main link, example: https://danmachi.wbijam.pl")
    parser.add_argument("-s", type=str, required=True, help="specify the season, example: pierwsza_seria.html")

    parser.add_argument("-q", required=False, choices=["hd", "sd", "lq", "vl"], help="specify the quality to download [default 'hd']", default="hd")
    parser.add_argument("-o", type=str, required=False, help="specify the path to download to")

    parser.add_argument("-t", type=int, required=False, help="amount of threads to use while downloading [default 1]", default=1)

    parser.add_argument("-l", type=bool, required=False, help="just create list as well as alt-list, dont download", default=False)
    args = parser.parse_args()

    # some checks
    if not requests.get(args.m).ok:
        exit(f"main link is not responding: {args.m}")

    if not requests.get(args.m + '/' + args.s).ok:
        exit(f"season is not responding: {args.m}/{args.s}")

    if not args.o:
        args.o = "./"

    w = wbijam(main_link=args.m, series=args.s)
    clinks = w.get_cLinks()
    # making a list.txt per standard of my storage
    with open(args.o + "/" + "list.txt", "w") as f:
        f.write('\n'.join(clinks))

    with multiprocessing.Pool(args.t) as pool:
        if "win" in platform:
            system("cls")
        else:
            system("clear")

        vals = list(zip(range(len(clinks)), clinks, [args.q] * len(clinks), [args.o] * len(clinks), [args.l] * len(clinks)))
        raw_links = pool.starmap(download, vals)

    # making an alt-list.txt per standard of my storage
    with open(args.o + "/" + "alt-list.txt", "w") as f:
        f.write('\n'.join(raw_links))

    print(f"\x1b[{len(clinks) + 2};0HDone!")
