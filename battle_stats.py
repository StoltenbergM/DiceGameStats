from dataclasses import dataclass
from typing import List, Tuple
import numpy as np
import math

## Player 1 starter hvis uafjort (P1 angriber)

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


def duel_p1_win(S1: int, A1: int, D1: int, 
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
    spd: int
    atk: int
    df: int

Team = List[Card]


def team_vs_team_full(team1: Team, team2: Team):
    """
    Returnerer:
      - head_to_head: liste med P(Team1 vinder) for position i vs i
      - avg_head_to_head: gennemsnit af head_to_head

      - all_vs_all: 2D matrix hvor [i][j] = P(team1[i] slår team2[j])
      - avg_all_vs_all: gennemsnit over alle matchups
    """
    n1 = len(team1)
    n2 = len(team2)

    # Head-to-head (position vs position)
    head_to_head = []
    for c1, c2 in zip(team1, team2):
        p = duel_p1_win(c1.spd, c1.atk, c1.df,
                        c2.spd, c2.atk, c2.df)
        head_to_head.append(p)
    avg_head_to_head = sum(head_to_head) / len(head_to_head)

    # All-vs-all
    all_vs_all = np.zeros((n1, n2))
    for i, c1 in enumerate(team1):
        for j, c2 in enumerate(team2):
            p = duel_p1_win(c1.spd, c1.atk, c1.df,
                            c2.spd, c2.atk, c2.df)
            all_vs_all[i, j] = p
    avg_all_vs_all = np.mean(all_vs_all)

    return head_to_head, avg_head_to_head, all_vs_all, avg_all_vs_all


# --- Eksempel ---

if __name__ == "__main__":
    team1 = [
        Card(-1, 0, 1),
        Card(-1, 0, 2),
        Card(-1, 0, 3),
        Card(-1, 0, 4),
    ]

    team2 = [
        Card(0, 1, 0),
        Card(0, 2, 0),
        Card(0, 3, 0),
        Card(0, 4, 0),
    ]

    h2h, avg_h2h, ava, avg_ava = team_vs_team_full(team1, team2)

    print("=== Head-to-head (position vs position) ===")
    for i, p in enumerate(h2h):
        print(f"  Duel {i+1}: {p:.3f}")
    print(f"  Gennemsnit: {avg_h2h:.3f}")

    print("\n=== All-vs-all matrix ===")
    print("  (rækker = Team1 kort, kolonner = Team2 kort)")
    print(np.round(ava, 3))
    print(f"  Gennemsnit: {avg_ava:.3f}")