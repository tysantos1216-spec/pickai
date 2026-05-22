import streamlit as st
import pandas as pd
from utils import get_advice

st.set_page_config(page_title="Prop Edge Analyzer", layout="wide")
st.title("🏀 NBA Prop Edge Identifier")

# --- DATA LAYER ---
@st.cache_data(ttl=900)
def load_data():
    # In a real app, use requests.get() here to fetch live JSON
    data = {
        "Player": ["LeBron James", "Jayson Tatum", "Stephen Curry", "Luka Dončić"],
        "Book_Line": [25.5, 8.5, 29.5, 9.5],
        "Model_Avg": [27.2, 7.8, 30.1, 10.2],
        "Std_Dev": [2.1, 1.2, 3.5, 1.1]
    }
    df = pd.DataFrame(data)
    df['Edge_Pct'] = ((df['Model_Avg'] - df['Book_Line']) / df['Book_Line']) * 100
    df['Advice'] = df.apply(get_advice, axis=1)
    return df

df = load_data()

# --- PROFESSIONAL DASHBOARD ---
col1, col2, col3 = st.columns(3)
# Show top play metrics
best_play = df.loc[df['Edge_Pct'].idxmax()]
col1.metric("Top Edge Play", best_play['Player'], f"{best_play['Edge_Pct']:.1f}% Edge")

# Filter for the best opportunities
st.subheader("High-Value Prop Opportunities")
st.dataframe(
    df.sort_values(by='Edge_Pct', ascending=False),
    column_config={
        "Edge_Pct": st.column_config.NumberColumn("Edge %", format="%.2f%%"),
        "Advice": st.column_config.TextColumn("Status")
    },
    use_container_width=True
)# utils.py
def calculate_implied_prob(american_odds):
    """Converts American odds to percentage probability."""
    if american_odds > 0:
        return 100 / (american_odds + 100) * 100
    else:
        return abs(american_odds) / (abs(american_odds) + 100) * 100

def get_advice(row):
    # Threshold: Only look for plays with an edge > 5%
    if row['Edge_Pct'] > 5:
        return "✅ Strong Value"
    elif row['Edge_Pct'] > 0:
        return "⚠️ Lean"
    return "❌ No Edge"
pickai/
├── app.py              # Main dashboard UI
├── utils.py            # Math logic and helper functions
├── requirements.txt    # streamlit, pandas, numpy, requests, plotly
└── .streamlit/
    └── secrets.toml    # Your API keys (never commit this to GitHub!)
    prize-picks-analyzer/
├── .streamlit/             # Configuration folder
│   └── config.toml         # Streamlit settings (themes, etc.)
├── pages/                  # Folder for additional app pages
│   └── 1_Analytics.py      # Example secondary page
├── services/               # Backend logic and API interaction
│   └── data_fetcher.py     # Scripts to pull data from APIs
├── utils/                  # Helper functions (math, formulas)
│   └── calculations.py     # Your EV and Probability formulas
├── .gitignore              # Prevents uploading venv, secrets, etc.
├── app.py                  # MAIN entry point (Home page)
├── requirements.txt        # Dependencies list
└── README.md               # Project documentation

prize-picks-analyzer/
├── app.py              # Your main "Home" page
├── pages/              # Folder for extra pages
│   ├── 2_Analytics.py  # This will automatically show up as "Analytics" in your sidebar
│   └── 3_Settings.py   # This will automatically show up as "Settings"
├── requirements.txt
└── .gitignore

streamlit
pandas
numpy
requests