from cda import CDA
from wbijam import wbijam
import argparse
import requests
import multiprocessing
from os import system
from sys import platform, stdout
from time import time, sleep


def dummy_download(k: int, clink: str, quality: str, path: str, list_only: bool) -> str:  # I/O + returning raw link
    c = CDA(clink)
    raw = c.getRaw(quality)
    filename = f"{k}-{c.playerID}.mp4"

    start = time()
    filesize = 10 ** 5
    _filesize = round(filesize / 10 ** 6, 2)
    done = 0

    for chunk in range(filesize):
        done = chunk  # += len(chunk)
        ctime = time() - start

        _done = round(done / 10 ** 6, 1)
        speed = round(_done / max(ctime, 1), 2)
        print(f"\x1b[{str(k + 2)};0H\x1b[2K[Dummy] Downloading: [...]{clink.split('/')[-1]} -> {path}{filename} {' ' * (len(str(_filesize)) - len(str(_done)))} {_done}MB/{_filesize}MB ~{speed}MB/s", end='')
        stdout.flush()

    total = round((time() - start) / 60, 2)
    print(f"\x1b[{str(k + 2)};0H\x1b[2K[Dummy] Completed: {clink} -> {path}{filename} Total Time: {total}m {' ' * (len(str(total)) - len(str(speed)))} Speed: {speed}MB/s", end='')
    stdout.flush()

    return raw


def download(k: int, clink: str, quality: str, path: str, list_only: bool) -> str:  # I/O + returning raw link
    c = CDA(clink)
    raw = c.getRaw(ql=quality)
    filename = f"{k}-{c.playerID}.mp4"

    if not list_only:
        raw_data = requests.get(raw, stream=True)

        filesize = int(raw_data.headers.get("content-length"))
        _filesize = round(filesize / 10**6, 2)
        done = 0
        with open(f"{path}/{filename}", "wb") as file:
            start = time()
            for chunk in raw_data.iter_content(chunk_size=4096):
                done += len(chunk)
                ctime = time() - start

                _done = round(done / 10**6, 1)
                speed = round(_done / max(ctime, 1), 2)

                print(f"\x1b[{str(k + 2)};0H\x1b[2KDownloading: [...]{clink.split('/')[-1]} -> {path}{filename} {' ' * ((len(str(_filesize))+1) - len(str(_done)))} {_done}MB/{_filesize}MB ~{speed}MB/s", end='')
                stdout.flush()

                file.write(chunk)
    # else: return only raw link

    print(f"\x1b[{str(k+2)};0H\x1b[2KCompleted: {clink} -> {path}{filename} total time: {round((time() - start) / 60, 2)}m", end='')
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
    parser.add_argument("-b", type=bool, required=False, help="test downloading", default=False)
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

        if not args.b:
            raw_links = pool.starmap(download, vals)
        else:
            raw_links = pool.starmap(dummy_download, vals)

    # making an alt-list.txt per standard of my storage
    with open(args.o + "/" + "alt-list.txt", "w") as f:
        f.write('\n'.join(raw_links))

    print(f"\x1b[{len(clinks) + 2};0HDone!")
