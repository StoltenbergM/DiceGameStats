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

print(f"Player 1 starter - og vinder: {p1w_pl1start}")
print(f"Player 1 starter - og taber: {p2w_pl1start} \n")

print(f"Player 2 starter - og vinder: {p2w_pl2start}")
print(f"Player 2 starter - og taber: {p1w_pl2start}")