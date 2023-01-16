import subprocess

areas = [
    (46,6),
    (47,6),
    (45,7),
    (46,"7L"),
    (46,"7R"),
    (47,7),
    (45,8),
    (46,"8L"),
    (46,"8R"),
    (47,8),
    (45,9),
    (46,9),
    (47,9)
]

for lat, long in areas:
    step = 1
    suffix = ""
    prefix = long
    if isinstance(long, str) and long.endswith("L"):
        step = 0.5
        prefix = long[:-1]
        suffix = long[-1]
        long=int(prefix)
    elif isinstance(long, str) and long.endswith("R"):
        step=0.5
        prefix = long[:-1]
        suffix = long[-1]
        long = int(prefix) + 0.5

    cmd = ["src/osmosis/bin/osmosis","--read-xml","enableDateParsing=no","file=out.osm","--lp","--bounding-box",f"top={lat+1}",f"left={long}",f"bottom={lat}",f"right={long+step}","--write-xml",f"file={lat}{prefix}{suffix}.osm"]
    print(" ".join(cmd))
    subprocess.run(cmd)

