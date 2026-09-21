import mysql.connector
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ==========================================
# 1. CONNECT TO MYSQL
# ==========================================

password = input("Enter MySQL password: ")

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="jp"
)

print("\nConnected to MySQL successfully!")


# ==========================================
# 2. PLAYER SEARCH BY POSITION
# ==========================================

position = input(
    "\nEnter position "
    "(Forward/Defender/Midfielder/Goalkeeper): "
).strip().title()

query = f"""
SELECT player_name, primary_club
FROM players_stat
WHERE position = '{position}'
"""

players = pd.read_sql(query, db)

print("\nPLAYERS")
print("-------")

if len(players) > 0:
    print(players)
else:
    print("No players found.")


# ==========================================
# 3. PLAYER SEARCH BY NAME
# ==========================================

player = input("\nEnter player name: ").strip()

query = f"""
SELECT player_name, position, primary_club
FROM players_stat
WHERE LOWER(player_name) = LOWER('{player}')
"""

player_result = pd.read_sql(query, db)

if len(player_result) > 0:

    print("\nPLAYER FOUND")
    print("------------")

    print(player_result)

else:

    print("\nPlayer not found.")


# ==========================================
# 4. JAPAN WORLD CUP DATA
# ==========================================

world_cup_data = {
    'Stage': ['Group F', 'Group F', 'Group F', 'Round of 32'],
    'Date': ['2026-06-14', '2026-06-20', '2026-06-25', '2026-06-29'],
    'Opponent': ['Netherlands', 'Tunisia', 'Sweden', 'Brazil'],
    'Japan_Goals': [2, 4, 1, 1],
    'Opponent_Goals': [2, 0, 1, 2],
    'Match_Result': ['D', 'W', 'D', 'L']
}

df = pd.DataFrame(world_cup_data)


# ==========================================
# 5. MATCH SEARCH
# ==========================================

opponent = input("\nEnter opponent team: ").strip()

match = df[
    df["Opponent"].str.lower() == opponent.lower()
]

if len(match) > 0:

    for index, row in match.iterrows():

        print("\nMATCH FOUND")
        print("-----------")

        print("Opponent:", row["Opponent"])
        print("Stage:", row["Stage"])
        print("Date:", row["Date"])

        print(
            "Score:",
            row["Japan_Goals"],
            "-",
            row["Opponent_Goals"]
        )

        print("Result:", row["Match_Result"])

else:

    print("\nNo match found.")


# ==========================================
# 6. SAMURAI BLUE ANALYSIS
# ==========================================

print("\nSAMURAI BLUE ANALYSIS")
print("---------------------")

match_points = []
goal_scored = 0
goal_conceded = 0


for index, row in df.iterrows():

    result = row['Match_Result']

    if result == 'W':
        match_points.append(3)

    elif result == 'D':
        match_points.append(1)

    else:
        match_points.append(0)

    goal_scored += row['Japan_Goals']
    goal_conceded += row['Opponent_Goals']


average_group_form = np.mean(match_points[:3])

goal_differential = goal_scored - goal_conceded


# ==========================================
# 7. DISPLAY ANALYSIS
# ==========================================

print("\nANALYSIS")
print("--------")

print("Points earned:", match_points[:3])

print(
    f"Form index (0.0 to 3.0): "
    f"{average_group_form:.2f}"
)

print("Goals scored:", goal_scored)

print("Goals conceded:", goal_conceded)

print(
    f"Goal difference: "
    f"{goal_differential:+d}"
)


# ==========================================
# 8. PERFORMANCE TRACKER
# ==========================================

print("\nPERFORMANCE TRACKER")
print("-------------------")


for index, row in df.iterrows():

    if row['Match_Result'] == 'W':
        outcome = "✅ WIN"

    elif row['Match_Result'] == 'D':
        outcome = "🤝 DRAW"

    else:
        outcome = "❌ LOSS"

    print(
        f"{row['Stage']} vs {row['Opponent']}: "
        f"{row['Japan_Goals']}-{row['Opponent_Goals']} "
        f"({outcome})"
    )


# ==========================================
# 9. GRAPH
# ==========================================

print("\nCreating graph...")


plt.plot(
    df['Opponent'],
    df['Japan_Goals'],
    marker='o',
    label="Japan Goals"
)

plt.plot(
    df['Opponent'],
    df['Opponent_Goals'],
    marker='x',
    label="Opponent Goals"
)

plt.title("Match Goals Comparison")
plt.xlabel("Opponent Teams")
plt.ylabel("Goals")
plt.legend()

plt.savefig("match_goals_comparison.png")

plt.show()


# ==========================================
# 10. CLOSE DATABASE
# ==========================================

db.close()

print("\nDatabase connection closed.")
