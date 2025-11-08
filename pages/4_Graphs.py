import streamlit as st
from data_loader import load_data
from logger import log
import altair as alt

st.set_page_config(page_title="Movie Graphs", layout="wide")
log("📄 Page 4_Graphs started")

df = load_data()

st.title("📊 Movie Analytics")
st.markdown("Interactive visualizations for top movies.")

# --- Subsection 1: Top Movies by Rating ---
st.subheader("🏆 Top Movies by Average Rating")
top_n = st.slider("Select top N movies to display:", 5, 50, 20)
top_movies = df.sort_values(['avg_rating','rating_count'], ascending=False).head(top_n)

# Ensure decade column exists
if 'decade' not in top_movies.columns:
    top_movies['decade'] = (top_movies['year'] // 10) * 10

# Horizontal bar chart colored by decade
chart = alt.Chart(top_movies).mark_bar().encode(
    y=alt.Y('title', sort='-x', title="Movie"),
    x=alt.X('avg_rating', title="Average Rating"),
    color=alt.Color('decade:N', legend=alt.Legend(title="Decade")),
    tooltip=['title', 'year', 'avg_rating', 'rating_count', 'decade']
).properties(width=900, height=400)

st.altair_chart(chart, use_container_width=True)

# --- Subsection 2: Rating vs Number of Votes ---
st.subheader("📈 Rating vs Number of Votes")
scatter = alt.Chart(top_movies).mark_circle(size=100).encode(
    x='rating_count',
    y='avg_rating',
    color=alt.Color('decade:N', legend=alt.Legend(title="Decade")),
    tooltip=['title', 'year', 'avg_rating', 'rating_count', 'decade']
).interactive()

st.altair_chart(scatter, use_container_width=True)

# --- Subsection 3: Optional Analysis ---
st.subheader("🔍 Optional Insights")
st.markdown("- Movies with high ratings but low number of votes might be underrated.")
st.markdown("- Movies with many votes and high ratings are usually popular classics.")

log("✅ 4_Graphs finished")
