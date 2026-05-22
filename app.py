import streamlit as st
import pandas as pd
import numpy as np
import requests

# Page Configuration
st.set_page_config(page_title="Prop Value Analyzer", layout="wide")
st.title("🏀 PrizePicks Edge Identifier")

# --- DATA FETCHING ---
# We keep this simple for deployment. 
# Replace the API_KEY with your actual key in Streamlit Secrets (Settings > Secrets)
@st.cache_data(ttl=900) # Caches data for 15 minutes
def get_player_stats_mock():
    # If you haven't set up the API yet, this ensures the app doesn't crash
    data = {
        "Player": ["LeBron James", "Jayson Tatum", "Stephen Curry", "Luka Dončić"],
        "Prop_Type": ["Points", "Rebounds", "Points", "Assists"],
        "PrizePicks_Line": [25.5, 8.5, 29.5, 9.5],
        "Mean_Last_10": [27.2, 7.8, 30.1, 10.2],
        "Std_Dev_Last_10": [2.1, 1.2, 3.5, 1.1]
    }
    return pd.DataFrame(data)

# --- MATH LOGIC ---
df = get_player_stats_mock()

df['Edge_Percentage'] = ((df['Mean_Last_10'] - df['PrizePicks_Line']) / df['PrizePicks_Line']) * 100
df['Z_Score'] = (df['Mean_Last_10'] - df['PrizePicks_Line']) / df['Std_Dev_Last_10']

def get_decision(row):
    if row['Z_Score'] > 0.5: return "YES (Over)"
    elif row['Z_Score'] < -0.5: return "YES (Under)"
    else: return "PASS"

df['Decision'] = df.apply(get_decision, axis=1)

# --- UI DISPLAY ---
st.subheader("Live Prop Analysis")

# Color formatting
def color_decision(val):
    color = '#2ecc71' if "YES" in val else '#e74c3c'
    return f'background-color: {color}; color: white'

# Use st.dataframe with mapping
styled_df = df.style.map(color_decision, subset=['Decision'])
st.dataframe(styled_df, use_container_width=True)

st.sidebar.info("System Refreshes Every 15 Minutes")
def calculate_edge(win_prob, decimal_odds):
    """
    win_prob: Your model's predicted probability (0.0 to 1.0)
    decimal_odds: The payout odds from the book (e.g., 1.91 for -110)
    """
    # Expected Value = (Probability of Win * Profit) - (Probability of Loss * Stake)
    ev = (win_prob * (decimal_odds - 1)) - (1 - win_prob)
    return ev * 100  # Return as percentage

# Example Usage:
# If you think LeBron has a 60% chance to go Over 25.5 points
# and the book offers 1.91 odds:
edge = calculate_edge(0.60, 1.91) 
# If edge > 0, it's a +EV play.def get_ai_rationale(row):
    if row['Edge_Percentage'] > 5:
        return "✅ Strong Play: Model shows 5%+ edge over market."
    elif row['Edge_Percentage'] > 0:
        return "⚠️ Lean: Positive edge, but within margin of error."
    else:
        return "❌ Stay Away: No statistical advantage found."

df['Advice'] = df.apply(get_ai_rationale, axis=1)
       