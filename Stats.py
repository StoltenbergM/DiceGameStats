'''
# Sandsynlighed for sejr når P1 angriber = sp1
# Sandsynlighed for sejr når P2 angriber = sp2
sp1 = 1/3
sp2 = 1/2

# Sandsynligheden for at player 1 vinder kampen, hvis P1 starter
p1w_pl1start = sp1 / (sp1 + sp2 - (sp1 * sp2))
p2w_pl1start = 1 - p1w_pl1start

# Sandsynligheden for at player 1 vinder kampen, hvis P2 starter
p1w_pl2start = (sp1 * (1 - sp2)) / (sp1 + sp2 - (sp1 * sp2))
p2w_pl2start = 1 - p1w_pl2start
'''


# delta_A og delta_D set fra Player 1 
p1a = 0
p1d = 0

p2a = 0
p2d = 1

# Fordeling for X = d6_a - d6_d
DIFF_PROBS = {
    -5: 1/36, -4: 2/36, -3: 3/36, -2: 4/36, -1: 5/36,
     0: 6/36,  1: 5/36,  2: 4/36,  3: 3/36,  4: 2/36,  5: 1/36
}

def hit_prob(att_A: int, def_D: int) -> float:
    """
    P(hit) når angriber har attack = att_A og forsvarer defense = def_D.
    """
    M = att_A - def_D
    threshold = -M               # vi vil have P(X > threshold)
    return sum(prob for x, prob in DIFF_PROBS.items() if x > threshold)

def sp1_sp2_from_stats(A1: int, D1: int, A2: int, D2: int):
    """
    sp1 = P(P1 rammer P2 i ét angreb)
    sp2 = P(P2 rammer P1 i ét angreb)
    """
    sp1 = hit_prob(A1, D2)  # P1 angriber P2
    sp2 = hit_prob(A2, D1)  # P2 angriber P1
    return sp1, sp2


sp1, sp2 = sp1_sp2_from_stats(p1a, p1d, p2a, p2d)

# Sandsynligheden for at player 1 vinder kampen, hvis P1 starter
p1w_pl1start = sp1 / (sp1 + sp2 - (sp1 * sp2))
p2w_pl1start = 1 - p1w_pl1start

# Sandsynligheden for at player 1 vinder kampen, hvis P2 starter
p1w_pl2start = (sp1 * (1 - sp2)) / (sp1 + sp2 - (sp1 * sp2))
p2w_pl2start = 1 - p1w_pl2start

print(f"Player 1 starter - player 1 vinder: {p1w_pl1start}")
print(f"Player 2 starter - player 1 vinder: {p1w_pl2start}")