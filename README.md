# poorlak_downloading
for downloadig entire series from wbijam.pl

try:
`python dir/download-wbijam.py -h`
for help, optionally here are some examples:
`python dir/download-wbijam.py -m "https://sng.wbijam.pl" -s "pierwsza_seria.html"`           -  will download the Suisei No Gagrantia series
`python dir/download-wbijam.py -m "https://sng.wbijam.pl" -s "pierwsza_seria.html" -t 4`      - use 4 cores for downloading
`python dir/download-wbijam.py -m "https://sng.wbijam.pl" -s "pierwsza_seria.html" -t 4 -l`   - just create `list` and `alt-list` (sources)
`python dir/download-wbijam.py -m "https://sng.wbijam.pl" -s "pierwsza_seria.html" -o "/dir"` - specify output path (otherwise will download in current)
`python dir/download-wbijam.py -m "https://sng.wbijam.pl" -s "pierwsza_seria.html" -q "sd"`   - download in standard definition (720p, default is HD, and will download highest possible if specified is not avaliable)



required additional libraries:

-requests `pip install requests`


