from wbijam import wbijam, async_get, async_get_stream, video
import requests
from aiofiles import open as async_open
import asyncio
from os import path
from re import findall


async def async_download(vid: video, filename: str) -> None:  # I/O
    url = await vid.direct_link()
    req = requests.get(url, stream=True, timeout=5)
    filesize = int(req.headers.get("content-length"))

    if path.exists(filename):
        if path.getsize(filename) == filesize:
            print(f"{filename} already exists")
            return

    async with async_open(filename, 'wb') as af:
        done = 0

        for chunk in req.iter_content(chunk_size=4096):
            print(f"\r{filename} {done}/{filesize} ({round(done / filesize * 100, 2)}%)", end='')

            done += len(chunk)
            await af.write(chunk)

    print('\n', end='')


async def main() -> None:
    wbj = await wbijam()
    if not wbj.ok:
        exit("Could not communicate with the wbijam.pl server")

    path = "D:/offline/videos/Suisei-no-Gargantia/S1/"
    series = await wbj.get_top_series()
    seasons = await series["sng"].seasons
    episodes = await seasons["pierwsza-seria"].episodes

    for ep in episodes:
        n, name = findall("([0-9][0-9]).*?\"(.*)\"", str(ep))[0]
        name = name.translate({ord(' '): '-', ord(','): '', ord('.'): '', ord('!'): '', ord('?'): ''})
        file = path + n + '-' + name + ".mp4"

        retry_time = 5
        while True:
            try:
                await async_download(ep, file)
            except requests.exceptions.ConnectionError:
                print(f"\ndownload failed, retrying in {retry_time}s")
                await asyncio.sleep(retry_time)
                retry_time = retry_time + 5
                continue
            else:
                break


if __name__ == '__main__':
    asyncio.run(main())
