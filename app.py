import streamlit as st
import pandas as pd
from utils import calculate_edge, get_advice
import plotly.express as px

st.set_page_config(page_title="Prop Edge Analyzer", layout="wide")

st.title("🏀 NBA Prop Edge Identifier")

# --- DATA FETCHING ---
@st.cache_data(ttl=900)
def load_data():
    # Replace this with your actual API call using st.secrets["API_KEY"]
    # Example: response = requests.get(URL, headers={"Authorization": st.secrets["API_KEY"]})
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

# --- UI LAYER ---
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("Filter Opportunities")
    min_edge = st.slider("Min Edge %", 0.0, 20.0, 5.0)
    filtered_df = df[df['Edge_Pct'] >= min_edge]

with col2:
    st.subheader("Live Prop Dashboard")
    st.dataframe(filtered_df, use_container_width=True)
    
    # Interactive Visualization
    fig = px.scatter(df, x="Book_Line", y="Model_Avg", color="Advice", 
                     hover_data=['Player'], title="Projection vs. Market Line")
    st.plotly_chart(fig, use_container_width=True)
    