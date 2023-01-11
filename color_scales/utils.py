import numpy as np

import colour


def parse_rgb(s):
    rgb = s[:2], s[2:4], s[4:6]
    return np.array([int(x, 16) for x in rgb]) / 255


def hsvs(party):
    rgb = np.array([parse_rgb(s) for s in party])
    return colour.RGB_to_HSV(rgb)


def normalized_hsvs(v):
    v = np.array(v)
    v[:, 0] = np.round(np.mean(v[:, 0]) * 360) / 360
    return v


def to_hex(rgb):
    return "%02x%02x%02x" % tuple((rgb * 255).round().astype(np.uint8))


def to_rgb_ramp(hsvs):
    return [to_hex(rgb) for rgb in colour.HSV_to_RGB(hsvs)]


def to_rgb_ramps(ramps):
    return {k: to_rgb_ramp(v) for k, v in ramps.items()}
