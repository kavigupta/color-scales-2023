def create_for_hue(h, from_hues):
    v = compute_value(h, {v[0][0] * 360: v for v in from_hues.values()})
    v[:, 0] = h / 360
    return v


def compute_value(h, keypoints):
    keypoints_by_distance = [(wheel_dist(h, k), v) for k, v in keypoints.items()]
    (d1, v1), (d2, v2) = sorted(keypoints_by_distance, key=lambda x: x[0])[:2]
    #     print(d1, v1, d2, v2)
    l2, l1 = d1 / (d1 + d2), d2 / (d1 + d2)
    return l1 * v1 + l2 * v2


def wheel_dist(a, b):
    d = abs(a - b)
    if d > 180:
        d = 360 - d
    return d
