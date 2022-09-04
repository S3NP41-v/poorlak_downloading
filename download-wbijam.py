from cda import CDA
from wbijam import wbijam
import argparse
import requests
# import multiprocessing.dummy


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="download entire series from wbijam.pl")
    parser.add_argument("-m", type=str, required=True, help="specify the main link, example: https://danmachi.wbijam.pl")
    parser.add_argument("-s", type=str, required=True, help="specify the season, example: pierwsza_seria.html")

    parser.add_argument("-q", required=False, choices=["hd", "sd", "lq", "vl"], help="specify the quality to download", default="hd")
    parser.add_argument("-o", type=str, required=False, help="specify the path to download to")

    args = parser.parse_args()

    # some checks
    if not requests.get(args.m).ok:
        exit(f"main link is not responding: {args.m}")

    if not requests.get(args.m + '/' + args.s).ok:
        exit(f"season is not responding: {args.m}/{args.s}")

    if not args.o:
        args.o = "./"

    w = wbijam(main_link=args.m, series=args.s)
    for k, clink in enumerate(w.get_cLinks()):
        c = CDA(clink)
        raw_link = c.getRaw(ql=args.q)
        r = requests.get(raw_link)

        print("creating file: " + args.o + '/' + f"{k}-{c.playerID}.mp4")  # debug
        with open(args.o + '/' + f"{k}-{c.playerID}.mp4", "wb") as f:
            f.write(r.content)


