import streamlit as st
import pandas as pd
import plotly.express as px

st.title("IPL Project Setup Test")
df = pd.DataFrame({"team": ["MI", "CSK", "RCB"], "titles": [5, 5, 0]})
st.plotly_chart(px.bar(df, x="team", y="titles"))