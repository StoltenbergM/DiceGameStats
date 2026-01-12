import numpy as np
import matplotlib.pyplot as plt

# Sandsynlighed for sejr når P1 angriber = sp1
# Sandsynlighed for sejr når P2 angriber = sp2
DIFF_PROBS = {
    -5: 1/36, -4: 2/36, -3: 3/36, -2: 4/36, -1: 5/36,
     0: 6/36,  1: 5/36,  2: 4/36,  3: 3/36,  4: 2/36,  5: 1/36
}

def p_hit_from_M(M: int) -> float:
    """
    P(hit) ved modifikator M = A_att - D_def.
    Hit når d6_a + A_att > d6_d + D_def  <=>  X = d6_a - d6_d > -M.
    """
    threshold = -M
    return sum(prob for x, prob in DIFF_PROBS.items() if x > threshold)

def p_hit_from_M(M: int) -> float:
    threshold = -M
    return sum(prob for x, prob in DIFF_PROBS.items() if x > threshold)

def p1_win_given_sp(sp1: float, sp2: float, starter: str = "p1") -> float:
    denom = sp1 + sp2 - sp1 * sp2
    if denom == 0:
        return 0.5
    if starter == "p1":
        return sp1 / denom
    else:
        return sp1 * (1 - sp2) / denom

'''
# Sandsynligheden for at player 1 vinder kampen, hvis P1 starter
p1w_pl1start = sp1 / (sp1 + sp2 - (sp1 * sp2))
p2w_pl1start = 1 - p1w_pl1start

# Sandsynligheden for at player 1 vinder kampen, hvis P2 starter
p1w_pl2start = (sp1 * (1 - sp2)) / (sp1 + sp2 - (sp1 * sp2))
p2w_pl2start = 1 - p1w_pl2start
'''

# --- Grid over x = A1-D2 og y = D1-A2 ---
M_atk_range = range(-6, 7)   # x-akse: A1 - D2
M_def_range = range(-6, 7)   # y-akse: D1 - A2
x_vals = list(M_atk_range)
y_vals = list(M_def_range)

P_p1_start  = np.zeros((len(y_vals), len(x_vals)))
P_p1_second = np.zeros_like(P_p1_start)

for i, y in enumerate(y_vals):
    for j, x in enumerate(x_vals):
        # sp1: P1 rammer P2, modifier = x = A1-D2
        sp1 = p_hit_from_M(x)
        # sp2: P2 rammer P1, modifier = A2-D1 = -y
        sp2 = p_hit_from_M(-y)

        P_p1_start[i, j]  = p1_win_given_sp(sp1, sp2, starter="p1")
        P_p1_second[i, j] = p1_win_given_sp(sp1, sp2, starter="p2")

def plot_heat_with_labels(ax, data, title):
    im = ax.imshow(
        data,
        origin="lower",
        vmin=0, vmax=1,
        cmap="viridis",
        extent=[min(x_vals)-0.5, max(x_vals)+0.5,
                min(y_vals)-0.5, max(y_vals)+0.5]
    )
    ax.set_title(title)
    ax.set_xlabel(r"$x = A_1 - D_2$  (P1 atk vs P2 def)")
    ax.set_ylabel(r"$y = D_1 - A_2$  (P1 def vs P2 atk)")
    ax.set_xticks(x_vals)
    ax.set_yticks(y_vals)
    cbar = plt.colorbar(im, ax=ax, label="P(P1 vinder)")

    # Skriv procenttal i hver celle
    for i, y in enumerate(y_vals):
        for j, x in enumerate(x_vals):
            prob = data[i, j]
            text = f"{prob*100:.0f}%"   # heltals-procent
            ax.text(x, y, text, ha="center", va="center",
                    color="white", fontsize=7)

if __name__ == "__main__":
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), constrained_layout=True)

    plot_heat_with_labels(axes[0], P_p1_start,
                          "P1 vinder (%) – P1 starter (højere speed)")
    plot_heat_with_labels(axes[1], P_p1_second,
                          "P1 vinder (%) – P2 starter (lavere speed)")

    plt.show()