from .utils import to_hex, parse_rgb


def add_extra(ramp):
    return [to_hex((parse_rgb(ramp[0]) + 1) / 2), *ramp]


def add_extra_to_all(ramps):
    return {k: add_extra(ramp) for k, ramp in ramps.items()}
