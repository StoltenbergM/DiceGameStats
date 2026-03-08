import streamlit as st
import pandas as pd
import numpy as np
import matplotlib

#This script should be run in the terminal - not normal RUN
# In termianl: streamlit run battle_ui.py

from battle_stats import Card, team_vs_team_full

st.set_page_config(layout="wide")

st.title("Card Battle Simulator")

# -----------------------------
# Initialize teams
# -----------------------------

if "teams" not in st.session_state:

    st.session_state.teams = {

        "Jungle":[
            {"name":"Hexloth","spd":0,"atk":1,"df":4},
            {"name":"Toxylis","spd":1,"atk":1,"df":1},
            {"name":"Thymur","spd":4,"atk":3,"df":2},
            {"name":"Pantrix","spd":6,"atk":4,"df":3},
            {"name":"Gorvath","spd":4,"atk":6,"df":6},
            {"name":"Tigravos","spd":6,"atk":7,"df":6},
            {"name":"Zytherion","spd":6,"atk":8,"df":8},
        ],

        "Lumar":[
            {"name":"Elyra","spd":3,"atk":1,"df":1},
            {"name":"Lumina","spd":2,"atk":3,"df":2},
            {"name":"Fenriva","spd":3,"atk":4,"df":3},
            {"name":"Pegasus","spd":7,"atk":4,"df":2},
            {"name":"Griffax","spd":5,"atk":6,"df":5},
            {"name":"Skyradrake","spd":8,"atk":6,"df":4},
            {"name":"Seraph","spd":9,"atk":8,"df":6},
        ],

        "Greenhallow":[
            {"name":"H","spd":2,"atk":1,"df":1},
            {"name":"L","spd":4,"atk":2,"df":1},
            {"name":"3","spd":4,"atk":4,"df":3},
            {"name":"4","spd":2,"atk":4,"df":6},
            {"name":"5","spd":4,"atk":6,"df":6},
            {"name":"6","spd":7,"atk":7,"df":5},
            {"name":"7","spd":6,"atk":9,"df":8},
        ]
    }


# -----------------------------
# Helper functions
# -----------------------------

def convert(cards):

    return [
        Card(c["spd"], c["atk"], c["df"])
        for c in cards
    ]


def matchup_avg(team1, team2):

    h2h1, _, ava1, avg1 = team_vs_team_full(team1, team2)
    h2h2, _, ava2, avg2 = team_vs_team_full(team2, team1)

    ava2 = 1 - ava2.T

    avg_matrix = (ava1 + ava2) / 2

    avg = np.mean(avg_matrix)

    return avg_matrix, avg


# -----------------------------
# Layout
# -----------------------------

left, right = st.columns([1,1])

# =========================================================
# LEFT SIDE — TEAM + CARD EDITOR
# =========================================================

with left:

    st.header("Team Editor")

    team_names = list(st.session_state.teams.keys())

    new_team = st.text_input("New Team Name")

    if st.button("Create Team"):

        if new_team != "":
            st.session_state.teams[new_team] = []

    selected_team = st.selectbox(
        "Edit Team",
        team_names
    )

    cards = st.session_state.teams[selected_team]

    if st.button("Add Card"):

        cards.append({
            "name":"New Card",
            "spd":1,
            "atk":1,
            "df":1
        })

    for i, card in enumerate(cards):

        col1,col2,col3,col4 = st.columns(4)

        card["name"] = col1.text_input(
            "Name",
            card["name"],
            key=f"{selected_team}_name_{i}"
        )

        card["spd"] = col2.number_input(
            "SPD",
            value=card["spd"],
            key=f"{selected_team}_spd_{i}"
        )

        card["atk"] = col3.number_input(
            "ATK",
            value=card["atk"],
            key=f"{selected_team}_atk_{i}"
        )

        card["df"] = col4.number_input(
            "DEF",
            value=card["df"],
            key=f"{selected_team}_df_{i}"
        )


# =========================================================
# RIGHT SIDE — MATCHUP
# =========================================================

with right:

    st.header("Team Matchup")

    team_names = list(st.session_state.teams.keys())

    team1_name = st.selectbox(
        "Team 1",
        team_names
    )

    team2_name = st.selectbox(
        "Team 2",
        [t for t in team_names if t != team1_name]
    )

    team1 = convert(st.session_state.teams[team1_name])
    team2 = convert(st.session_state.teams[team2_name])

    h2h, avg_h2h, ava, avg_ava = team_vs_team_full(team1, team2)

    names1 = [c["name"] for c in st.session_state.teams[team1_name]]
    names2 = [c["name"] for c in st.session_state.teams[team2_name]]

    st.subheader("Head to Head")

    h2h_df = pd.DataFrame({
        team1_name:names1,
        team2_name:names2,
        "Win %":h2h
    })

    st.dataframe(h2h_df)

    st.metric("Average", round(avg_h2h,3))

    st.subheader("All vs All")

    matrix_df = pd.DataFrame(
        ava,
        index=names1,
        columns=names2
    )

    st.dataframe(
        matrix_df.style.background_gradient(cmap="RdYlGn")
    )

    st.metric("Average", round(avg_ava,3))


# =========================================================
# FULL FACTION BALANCE DASHBOARD
# =========================================================

st.header("Faction Balance Dashboard")

teams = list(st.session_state.teams.keys())

results = np.zeros((len(teams), len(teams)))

for i,t1 in enumerate(teams):

    for j,t2 in enumerate(teams):

        if i == j:
            continue

        team1 = convert(st.session_state.teams[t1])
        team2 = convert(st.session_state.teams[t2])

        _,avg = matchup_avg(team1,team2)

        results[i,j] = avg


balance_df = pd.DataFrame(
    results,
    index=teams,
    columns=teams
)

st.dataframe(
    balance_df.style.background_gradient(cmap="RdYlGn")
)