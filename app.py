import streamlit as st
import pandas as pd
import numpy as np

# Page Configuration
st.set_page_config(page_title="Prop Value Analyzer", layout="wide")
st.title("🏀 PrizePicks Edge Identifier")

# 1. Mock Data Loading (Replace with an API call in the future)
def get_live_props():
    data = {
        "Player": ["LeBron James", "Jayson Tatum", "Stephen Curry", "Luka Dončić"],
        "Prop_Type": ["Points", "Rebounds", "Points", "Assists"],
        "PrizePicks_Line": [25.5, 8.5, 29.5, 9.5],
        "Mean_Last_10": [27.2, 7.8, 30.1, 10.2],
        "Std_Dev_Last_10": [2.1, 1.2, 3.5, 1.1]
    }
    return pd.DataFrame(data)

df = get_live_props()

# 2. Mathematical Logic
# Calculate Edge Percentage
df['Edge_Percentage'] = ((df['Mean_Last_10'] - df['PrizePicks_Line']) / df['PrizePicks_Line']) * 100
df['Z_Score'] = (df['Mean_Last_10'] - df['PrizePicks_Line']) / df['Std_Dev_Last_10']

# Determine Decision
def get_decision(row):
    if row['Z_Score'] > 0.5: return "YES (Over)"
    elif row['Z_Score'] < -0.5: return "YES (Under)"
    else: return "PASS"

df['Decision'] = df.apply(get_decision, axis=1)

# 3. UI Display
def color_decision(val):
    if "YES" in val: return 'background-color: #2ecc71; color: white'
    return 'background-color: #e74c3c; color: white'

# Display Table
#st.dataframe(df.style.map(color_decision, subset=['Decision']))


# Sidebar Refresh
st.sidebar.info("System Refreshes Every 15 Minutes")
import streamlit as st
import pandas as pd
import numpy as np
from services.data_fetcher import get_player_id, get_player_stats

st.title("🏀 NBA Live Stats Analyzer")

player_name = st.text_input("Enter Player Name (e.g., LeBron James):")

if player_name:
    pid = get_player_id(player_name)
    if pid:
        stats = get_player_stats(pid)
        df = pd.DataFrame(stats)
        
        # Calculate key metrics
        pts_list = [game['pts'] for game in stats]
        mean_pts = np.mean(pts_list)
        std_pts = np.std(pts_list)
        
        st.subheader(f"Stats for {player_name}")
        st.write(f"Last 10 Games Average: {mean_pts:.2f} pts")
        
        # Display the table
        st.dataframe(df[['pts', 'ast', 'reb', 'min']])
    else:
        st.error("Player not found.")
       