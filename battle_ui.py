import streamlit as st
import pandas as pd
import numpy as np

#This script should be run in the terminal - not normal RUN

# In termianl: streamlit run battle_ui.py

from battle_stats import Card, team_vs_team_full

st.set_page_config(layout="wide")

st.title("Card Battle Simulator")

# ----------------------------
# Card Input
# ----------------------------

st.sidebar.header("Team Setup")

def create_team_input(team_name, default_cards):

    st.sidebar.subheader(team_name)

    cards = []

    for i, card in enumerate(default_cards):

        cols = st.sidebar.columns(4)

        name = cols[0].text_input(
            f"{team_name} Card {i+1} Name",
            value=card["name"],
            key=f"{team_name}_name_{i}"
        )

        spd = cols[1].number_input(
            "SPD",
            value=card["spd"],
            key=f"{team_name}_spd_{i}"
        )

        atk = cols[2].number_input(
            "ATK",
            value=card["atk"],
            key=f"{team_name}_atk_{i}"
        )

        df = cols[3].number_input(
            "DEF",
            value=card["df"],
            key=f"{team_name}_df_{i}"
        )

        cards.append({"name": name, "spd": spd, "atk": atk, "df": df})

    return cards


# Default cards
team1_defaults = [
    {"name":"T1-A","spd":0,"atk":1,"df":4},
    {"name":"T1-B","spd":1,"atk":1,"df":1},
    {"name":"T1-C","spd":4,"atk":3,"df":2},
    {"name":"T1-D","spd":6,"atk":4,"df":3},
    {"name":"T1-E","spd":4,"atk":6,"df":6},
    {"name":"T1-F","spd":6,"atk":7,"df":6},
    {"name":"T1-G","spd":6,"atk":8,"df":8},
]

team2_defaults = [
    {"name":"T2-A","spd":3,"atk":1,"df":1},
    {"name":"T2-B","spd":2,"atk":3,"df":2},
    {"name":"T2-C","spd":3,"atk":4,"df":3},
    {"name":"T2-D","spd":7,"atk":4,"df":2},
    {"name":"T2-E","spd":5,"atk":6,"df":5},
    {"name":"T2-F","spd":8,"atk":6,"df":4},
    {"name":"T2-G","spd":9,"atk":8,"df":6},
]

team1_cards = create_team_input("Team 1", team1_defaults)
team2_cards = create_team_input("Team 2", team2_defaults)

# ----------------------------
# Buff Controls
# ----------------------------

st.sidebar.header("Team Buffs")

buff1_spd = st.sidebar.number_input("Team1 SPD Buff", value=0)
buff1_atk = st.sidebar.number_input("Team1 ATK Buff", value=0)
buff1_df  = st.sidebar.number_input("Team1 DEF Buff", value=0)

buff2_spd = st.sidebar.number_input("Team2 SPD Buff", value=0)
buff2_atk = st.sidebar.number_input("Team2 ATK Buff", value=0)
buff2_df  = st.sidebar.number_input("Team2 DEF Buff", value=0)

# ----------------------------
# Build Card Objects
# ----------------------------

def apply_buff(cards, spd, atk, df):

    return [
        Card(
            c["spd"] + spd,
            c["atk"] + atk,
            c["df"] + df
        )
        for c in cards
    ]

team1 = apply_buff(team1_cards, buff1_spd, buff1_atk, buff1_df)
team2 = apply_buff(team2_cards, buff2_spd, buff2_atk, buff2_df)

# ----------------------------
# Run Battles
# ----------------------------

h2h_1, avg_h2h_1, ava_1, avg_ava_1 = team_vs_team_full(team1, team2)
h2h_2, avg_h2h_2, ava_2, avg_ava_2 = team_vs_team_full(team2, team1)

# flip second matrix perspective
ava_2 = 1 - ava_2.T

# average
h2h_avg = [(a + (1-b)) / 2 for a, b in zip(h2h_1, h2h_2)]
ava_avg = (ava_1 + ava_2) / 2

avg_h2h = np.mean(h2h_avg)
avg_ava = np.mean(ava_avg)

names1 = [c["name"] for c in team1_cards]
names2 = [c["name"] for c in team2_cards]

# ----------------------------
# Display Results
# ----------------------------

st.header("Head-to-Head")

h2h_df = pd.DataFrame({
    "Team1 Card": names1,
    "Team2 Card": names2,
    "Win Prob Team1": h2h_avg
})

st.dataframe(h2h_df)

st.metric("Average Head-to-Head", round(avg_h2h,3))

st.header("All vs All Matrix")

matrix_df = pd.DataFrame(
    ava_avg,
    index=names1,
    columns=names2
)

st.dataframe(matrix_df)

st.metric("Average All vs All", round(avg_ava,3))