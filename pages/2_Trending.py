import streamlit as st
from data_loader import load_data
from logger import log
import altair as alt

st.set_page_config(page_title="Trending Movies", layout="wide")
log("📄 Page 2_Trending started")

df = load_data()

st.title("🔥 Trending Movies")
st.markdown("Top 20 movies sorted by rating and popularity.")

# Take top 20 trending movies
trending = df.sort_values(['avg_rating','rating_count'], ascending=False).head(20)

# Metrics at the top
col1, col2, col3 = st.columns(3)
col1.metric("Top Rated", trending.iloc[0]['title'])
col2.metric("Avg Rating", f"{trending.iloc[0]['avg_rating']:.1f}")
col3.metric("Votes", trending.iloc[0]['rating_count'])

# Table
st.dataframe(trending[['title', 'year', 'avg_rating', 'rating_count']])

# Optional bar chart
chart = alt.Chart(trending).mark_bar(color="#FF6F61").encode(
    x=alt.X('title', sort='-y'),
    y='avg_rating',
    tooltip=['title', 'year', 'avg_rating', 'rating_count']
).properties(width=900, height=400)
st.altair_chart(chart, use_container_width=True)

log("✅ 2_Trending page finished")
