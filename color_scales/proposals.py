from color_scales.interpolate import create_for_hue
from .utils import hsvs, normalized_hsvs
from .data.proposal_2022 import proposal_2022_strings


class proposal_2022:
    rgb_strings = proposal_2022_strings

    hsv = {k: hsvs(v) for k, v in rgb_strings.items()}


class proposal_2022_normalized:
    hsv = {k: normalized_hsvs(v) for k, v in proposal_2022.hsv.items()}


class proposal_2023_for_hues:
    names = {
        int(360 * normalized_hsvs(v)[:, 0].mean()): k
        for k, v in proposal_2022_normalized.hsv.items()
    }

    def __init__(self, hues):
        self.hsv = {
            self.names.get(h, "")
            + f" [{h}]": create_for_hue(h, proposal_2022_normalized.hsv)
            for h in hues
        }
