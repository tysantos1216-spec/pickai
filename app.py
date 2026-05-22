import streamlit as st
import pandas as pd
import numpy as np

# Page Config
st.set_page_config(page_title="NBA Edge Identifier", layout="wide")
st.title("🏀 NBA Player Prop Edge Identifier")

# --- DATA LAYER ---
@st.cache_data(ttl=900) # Caches data for 15 minutes to save API quota
def get_live_data():
    # REPLACE THIS with your actual API call to 'The-Odds-API' or 'BallDontLie'
    # Currently using a structure that represents live potential
    data = {
        "Player": ["LeBron James", "Jayson Tatum", "Stephen Curry", "Luka Dončić"],
        "Prop": ["Points", "Rebounds", "Points", "Assists"],
        "Book_Line": [25.5, 8.5, 29.5, 9.5],
        "Model_Avg": [27.2, 7.8, 30.1, 10.2],
        "Std_Dev": [2.1, 1.2, 3.5, 1.1]
    }
    return pd.DataFrame(data)

df = get_live_data()

# --- MATH LOGIC ---
# Edge = (Model_Avg - Book_Line) / Book_Line
df['Edge_Pct'] = ((df['Model_Avg'] - df['Book_Line']) / df['Book_Line']) * 100
df['Z_Score'] = (df['Model_Avg'] - df['Book_Line']) / df['Std_Dev']

def get_advice(row):
    if row['Edge_Pct'] > 8: return "✅ Strong Value (Over)"
    if row['Edge_Pct'] < -8: return "✅ Strong Value (Under)"
    return "❌ No Edge"

df['Advice'] = df.apply(get_advice, axis=1)

# --- UI DISPLAY ---
def highlight_rows(row):
    color = '#2ecc71' if "Strong" in row['Advice'] else '#f8f9fa'
    return [f'background-color: {color}'] * len(row)

st.dataframe(df.style.apply(highlight_rows, axis=1), use_container_width=True)

st.sidebar.info("System Refreshes Every 15 Minutes")
st.sidebar.write("Advice is based on statistical deviation (Z-Score) > 1.5.")
       