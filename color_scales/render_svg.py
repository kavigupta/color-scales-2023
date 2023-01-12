import os
import re
import subprocess
import tempfile

import tqdm
from permacache import permacache

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
    dict(
        basemap="ga.svg",
        baseramp=current_down.rgb_strings,
        name="2020 ga sen special",
    ),
]


def ramp_dict(start, end):
    return dict(zip(start, end))


def ramp_fn(ramps, dems, gops, greens):
    rd = {
        **ramp_dict(ramps["dem"], dems),
        **ramp_dict(ramps["gop"], gops),
        # if not present it shouldn't be necessary
        **ramp_dict(ramps.get("green", []), greens),
        "BBBBBB": "BBBBBB",
        "808080": "808080",
        "FFFFFF": "FFFFFF",
        "000000": "000000",
    }
    rd = {k.upper(): v for k, v in rd.items()}
    return lambda x: rd[x.upper()]


@permacache("color_scales/render_svg/render_svg_2")
def render_svg(text):
    temp_path = tempfile.mktemp(suffix=".svg")
    temp_png = tempfile.mktemp(suffix=".png")

    with open(temp_path, "w") as f:
        f.write(text)
    subprocess.check_call(
        [
            "inkscape",
            "--export-width=2048",
            "--export-type=png",
            f"--export-filename={temp_png}",
            temp_path,
        ]
    )
    with open(temp_png, "rb") as f:
        return f.read()


def output(race, supername, proposal, dem, gop, green="green"):
    p = proposals[proposal]
    fn = ramp_fn(race["baseramp"], p[dem], p[gop], p[green])
    with open(os.path.join("basemaps", race["basemap"]), "r") as f:
        text = f.read()
    text = re.sub("fill:#([0-9A-Fa-f]{6})", lambda g: "fill:#" + fn(g.group(1)), text)
    name = f"{proposal}, {dem} vs {gop}" + (f" vs {green}" if green != "green" else "")
    text = text.replace("$X", name)

    img = render_svg(text)

    folder = f"images/{supername}/{race['name']}"
    try:
        os.makedirs(folder)
    except FileExistsError:
        pass

    with open(f"{folder}/{name}.png", "wb") as f:
        f.write(img)


def produce_outputs(dem_start, gop_start, green_start):
    for prop in proposals:
        colors = lambda start: [x for x in proposals[prop] if x.startswith(start)]
        for dem in colors(dem_start):
            for gop in colors(gop_start):
                for green in colors(green_start)[:1]:
                    for example_map in example_maps:
                        output(
                            example_map,
                            f"{dem_start}_{gop_start}"
                            + ("_" + green_start if green_start != "green" else ""),
                            prop,
                            dem,
                            gop,
                            green,
                        )
