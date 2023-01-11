import os
import re
import subprocess
import tempfile
from .proposals import current_down, current_pres, proposals

example_maps = [
    dict(
        basemap="2020.svg",
        baseramp=current_pres.rgb_strings,
        name="2020 pres",
    ),
    dict(
        basemap="texas.svg",
        baseramp=current_down.rgb_strings,
        name="2006 tx gov",
    ),
]


def ramp_dict(start, end):
    return dict(zip(start, end))


def ramp_fn(ramps, dems, gops, greens):
    rd = {
        **ramp_dict(ramps["dem"], dems),
        **ramp_dict(ramps["gop"], gops),
        **ramp_dict(ramps["green"], greens),
        "BBBBBB": "BBBBBB",
        "808080": "808080",
        "FFFFFF": "FFFFFF",
        "000000": "000000",
    }
    rd = {k.upper(): v for k, v in rd.items()}
    return lambda x: rd[x.upper()]


def output(race, supername, proposal, dem, gop, green="green"):
    p = proposals[proposal]
    fn = ramp_fn(race["baseramp"], p[dem], p[gop], p[green])
    with open(race["basemap"], "r") as f:
        text = f.read()
    text = re.sub("fill:#([0-9A-Fa-f]{6})", lambda g: "fill:#" + fn(g.group(1)), text)
    name = f"{proposal}, {dem} vs {gop}"
    text = text.replace("$X", name)

    temp_path = tempfile.mktemp(suffix=".svg")

    with open(temp_path, "w") as f:
        f.write(text)
    folder = f"images/{supername}/{race['name']}"
    try:
        os.makedirs(folder)
    except FileExistsError:
        pass
    subprocess.check_call(
        [
            "inkscape",
            "--export-width=2048",
            "--export-type=png",
            f"--export-filename={folder}/{name}.png",
            temp_path,
        ]
    )


def produce_outputs(dem_start, gop_start, green_start):
    for prop in proposals:
        for dem in [x for x in proposals[prop] if x.startswith(dem_start)]:
            for gop in [x for x in proposals[prop] if x.startswith(gop_start)]:
                for green in [x for x in proposals[prop] if x.startswith(green_start)]:
                    print(prop, dem, gop, green)
                    for example_map in example_maps:
                        output(example_map, "dem_gop", prop, dem, gop, green)
