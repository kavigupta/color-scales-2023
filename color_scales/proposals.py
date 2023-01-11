from color_scales.extra_ramp import add_extra_to_all
from color_scales.interpolate import create_for_hue
from .utils import hsvs, normalized_hsvs, to_rgb_ramps
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

    def __init__(self, hue_name_mapping):
        if not isinstance(hue_name_mapping, dict):
            hue_name_mapping = {h: self.names.get(h, "") for h in hue_name_mapping}
        self.hsv = {
            hue_name_mapping[h]
            + f"_{h}": create_for_hue(h, proposal_2022_normalized.hsv)
            for h in hue_name_mapping
        }
        self.rgb_strings = to_rgb_ramps(self.hsv)


class current_pres:
    rgb_strings = dict(
        dem="D3E7FF B9D7FF 86B6F2 4389E3 1666CB 0645B4 002B84".split(),
        gop="FFCCD0 F2B3BE E27F90 CC2F4A D40000 AA0000 800000".split(),
        green_1912_progressive="C7FFAF C6E9AF AADE87 8DD35F 71C837 000000 000000 000000".split(),
        green_1924_progressive="D7F4D7 AFE9AF 73D873 42CA42 30A630 000000 000000 000000".split(),
        orange="FFCCAA FFB380 FF9955 FF7F2A FF6600 D45500 AA4400".split(),
    )


class current_down:
    rgb_strings = dict(
        dem="DFEEFF BDD3FF A5B0FF 7996E2 6674DE 584CDE 3933E5 0D0596".split(),
        gop="FFE0EA FFC8CD FFB2B2 E27F7F D75D5D D72F30 C21B18 A80000".split(),
        green="c0f0c0 aae5aa 87de87 5fd35f 37c837 2ca02c 217821 165016".split(),
        orange_socialist="ff8e65 ff7644 f8581e CD3700 973714 622e1b 000000".split(),
        orange_republican="FFDAC1 FFCCA9 FFB580 FF9A50 EE8E50 D69850 B98A35 9D7700".split(),
    )


proposals = dict(
    current_pres=add_extra_to_all(current_pres.rgb_strings),
    current_down=current_down.rgb_strings,
    prop_2022=add_extra_to_all(proposal_2022.rgb_strings),
    prop_2023=add_extra_to_all(
        proposal_2023_for_hues(
            {
                **proposal_2023_for_hues.names,
                25: "orange",
                90: "green",
                160: "green",
                210: "dem",
                230: "dem",
                240: "dem",
            }
        ).rgb_strings
    ),
)
