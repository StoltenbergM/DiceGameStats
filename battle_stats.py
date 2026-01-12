from dataclasses import dataclass
from typing import List, Tuple
import math

# ---------- 1. Grund-sandsynligheder ----------

# Fordeling for X = d6_a - d6_d
DIFF_PROBS = {
    -5: 1/36, -4: 2/36, -3: 3/36, -2: 4/36, -1: 5/36,
     0: 6/36,  1: 5/36,  2: 4/36,  3: 3/36,  4: 2/36,  5: 1/36
}

def p_hit(att_A: int, def_D: int) -> float:
    """
    P(hit) når angriber har attack = att_A og forsvarer defense = def_D.
    Hit hvis: d6_a + A > d6_d + D  <=>  X = d6_a - d6_d > -(A-D).
    """
    M = att_A - def_D
    threshold = -M
    return sum(prob for x, prob in DIFF_PROBS.items() if x > threshold)


def p1_duel_win(S1: int, A1: int, D1: int, 
                S2: int, A2: int, D2: int) -> float:
    """
    Analytisk P(P1 vinder én duel med 1 HP, givet stats og speed-regel:
    - højere speed starter
    - ved lig speed starter P1
    """
    sp1 = p_hit(A1, D2)  # P(P1 rammer P2 i et angreb)
    sp2 = p_hit(A2, D1)  # P(P2 rammer P1 i et angreb)

    denom = sp1 + sp2 - sp1 * sp2
    if denom == 0:
        return 0.5  # ingen kan ramme nogen

    # hvem starter?
    if S1 > S2:
        starter = "p1"
    elif S2 > S1:
        starter = "p2"
    else:
        starter = "p1"  # tiebreak til P1

    if starter == "p1":
        return sp1 / denom
    else:
        return sp1 * (1 - sp2) / denom


# --- Kort og teams ---

@dataclass
class Card:
    atk: int
    df: int
    spd: int

Team = List[Card]


def team_vs_team_simple(team1: Team, team2: Team):
    """
    Returnerer:
      - liste med P(Team1-kort vinder) for hver position (0 vs 0, 1 vs 1, ...)
      - gennemsnitlig P(Team1 vinder) over alle dueller
    """
    assert len(team1) == len(team2), "Teams skal have samme størrelse"

    p_duels = []
    for c1, c2 in zip(team1, team2):
        p = p1_duel_win(c1.atk, c1.df, c1.spd,
                        c2.atk, c2.df, c2.spd)
        p_duels.append(p)

    avg_p = sum(p_duels) / len(p_duels)
    return p_duels, avg_p


# --- Eksempel ---

if __name__ == "__main__":
    team1 = [
        Card(1, 0, 0),
        Card(1, 0, 0),
        Card(1, 0, 0),
        Card(1, 0, 0),
        Card(1, 0, 0),
        Card(1, 0, 0),
        Card(1, 0, 0),
    ]

    team2 = [
        Card(0, 0, 2),
        Card(0, 0, 2),
        Card(0, 0, 2),
        Card(0, 0, 2),
        Card(0, 0, 2),
        Card(0, 0, 2),
        Card(0, 0, 2),
    ]

    p_duels, avg_p = team_vs_team_simple(team1, team2)

    print("P(Team1 vinder hver duel):")
    for i, p in enumerate(p_duels, start=1):
        print(f"  Duel {i}: {p:.3f}")

    print("\nGennemsnitlig P(Team1 vinder en duel):", avg_p)