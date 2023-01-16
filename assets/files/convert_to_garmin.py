from pathlib import Path
import subprocess
import shutil

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

base_path = Path("coros_map")

for lat, long in areas:
        path = base_path / "0" / str(lat) / "0" / f"S0{lat}000{long}"
        if path.exists():
                continue
        path.mkdir(parents=True, exist_ok=True)
        cmd = ["java", "-jar", "src/mkgmap-r4905/mkgmap.jar", "--latin1", "--style=swisstopo", "--style-file=styles/swisstopo.zip", "--check-styles", f"--output-dir={path}", "--verbose", f"{lat}{long}.osm", "--keep-going"]
        print(" ".join(cmd))
        subprocess.run(cmd)

for lat, long in areas:
        path = base_path / "0" / str(lat) / "0" / f"S0{lat}000{long}" / "63240001.img"
        target_path = base_path / "0" / str(lat) / "0" / f"C0{lat}000{long}.csm"
        if target_path.exists():
                continue
        shutil.move(path, target_path)
