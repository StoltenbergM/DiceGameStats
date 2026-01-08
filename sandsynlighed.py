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

def sp1_sp2_from_diffs(delta_A: int, delta_D: int):
    """
    Udregner sp1 og sp2 automatisk ud fra forskellene mellem Attack og Defense
    """
    M1 = delta_A
    M2 = -delta_D
    sp1 = p_hit_from_M(M1)  # P(P1 rammer P2)
    sp2 = p_hit_from_M(M2)  # P(P2 rammer P1)
    return sp1, sp2

def p1_win_given_sp(sp1: float, sp2: float, starter: str = "p1") -> float:
    denom = sp1 + sp2 - (sp1 * sp2)
    if denom == 0:
        return 0.5
    if starter == "p1":
        return sp1 / denom
    else:  # P2 starter
        return (sp1 * (1 - sp2)) / denom

'''
# Sandsynligheden for at player 1 vinder kampen, hvis P1 starter
p1w_pl1start = sp1 / (sp1 + sp2 - (sp1 * sp2))
p2w_pl1start = 1 - p1w_pl1start

# Sandsynligheden for at player 1 vinder kampen, hvis P2 starter
p1w_pl2start = (sp1 * (1 - sp2)) / (sp1 + sp2 - (sp1 * sp2))
p2w_pl2start = 1 - p1w_pl2start
'''

# --- Grid over ΔA, ΔD ---
delta_range = range(-5, 6)
delta_A_vals = list(delta_range)
delta_D_vals = list(delta_range)

P_p1_starter = np.zeros((len(delta_D_vals), len(delta_A_vals)))

for i, dD in enumerate(delta_D_vals):
    for j, dA in enumerate(delta_A_vals):
        sp1, sp2 = sp1_sp2_from_diffs(dA, dD)
        P_p1_starter[i, j] = p1_win_given_sp(sp1, sp2, starter="p1")

# --- Plot med procenttal i hver celle ---
fig, ax = plt.subplots(figsize=(8, 7))

im = ax.imshow(
    P_p1_starter,
    origin="lower",
    vmin=0, vmax=1,
    cmap="viridis",
    extent=[min(delta_A_vals)-0.5, max(delta_A_vals)+0.5,
            min(delta_D_vals)-0.5, max(delta_D_vals)+0.5]
)

ax.set_title("P(P1 vinder) – P1 starter (i %)")
ax.set_xlabel(r"$\Delta A = A_1 - A_2$")
ax.set_ylabel(r"$\Delta D = D_1 - D_2$")
ax.set_xticks(delta_A_vals)
ax.set_yticks(delta_D_vals)

# Skriv procenttal i hver celle
for i, dD in enumerate(delta_D_vals):
    for j, dA in enumerate(delta_A_vals):
        prob = P_p1_starter[i, j]
        text = f"{prob*100:.0f}%"  # heltal-procent
        # center-koordinater for cellen
        x = dA
        y = dD
        ax.text(x, y, text, ha="center", va="center", color="white", fontsize=8)

plt.colorbar(im, ax=ax, label="P(P1 vinder)")
plt.tight_layout()
plt.show()