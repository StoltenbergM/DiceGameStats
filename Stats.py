# delta_A og delta_D set fra Player 1 
delta_A = 5
delta_D = -5

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

sp1, sp2 = sp1_sp2_from_diffs(delta_A=delta_A, delta_D=delta_D)

# Sandsynligheden for at player 1 vinder kampen, hvis P1 starter
p1w_pl1start = sp1 / (sp1 + sp2 - (sp1 * sp2))
p2w_pl1start = 1 - p1w_pl1start

# Sandsynligheden for at player 1 vinder kampen, hvis P2 starter
p1w_pl2start = (sp1 * (1 - sp2)) / (sp1 + sp2 - (sp1 * sp2))
p2w_pl2start = 1 - p1w_pl2start

print(f"Player 1 starter - og vinder: {p1w_pl1start}")
print(f"Player 1 starter - og taber: {p2w_pl1start} \n")

print(f"Player 2 starter - og vinder: {p2w_pl2start}")
print(f"Player 2 starter - og taber: {p1w_pl2start}")