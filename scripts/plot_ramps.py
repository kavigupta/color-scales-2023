from matplotlib import pyplot as plt
import numpy as np

from color_scales.proposals import (
    proposal_2022,
    proposal_2022_normalized,
    proposal_2023_a_for_hues,
)
from color_scales.ramp_plots import plot_ramps

plt.title("2022 Proposal")
plot_ramps(proposal_2022.hsv)
plt.savefig("proposal_ramps/2022.png")
plt.close()

plt.title("2023 A Proposal [same selection as 2022]")
plot_ramps(proposal_2022_normalized.hsv)
plt.savefig("proposal_ramps/2023_a_selected_as_2022.png")
plt.close()

plt.figure(figsize=(3, 50))
plt.title("2023 A Proposal [all]")
plot_ramps(
    proposal_2023_a_for_hues(
        np.array([x for y in range(10) for x in range(360) if x % 10 == y])
    ).hsv
)
plt.savefig("proposal_ramps/2023_a_all.png")
plt.close()


plt.title("2023 A Proposal [selected]")
plot_ramps(
    proposal_2023_a_for_hues(
        np.array([2, 32, 48, 134, 180, 210, 220, 230, 240, 250, 280, 300, 330])
    ).hsv
)
plt.savefig("proposal_ramps/2023_a_selected.png")
plt.close()
