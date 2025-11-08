import streamlit as st
from data_loader import load_data
from logger import log

st.set_page_config(page_title="Movie Search", layout="wide")
log("📄 Page 1_Search_Movies started")

df = load_data()
log("Data loaded successfully in 1_Search_Movies")

st.title("🎬 Search Movies")
st.markdown("Search for any movie and view its ratings and release year.")

search_term = st.text_input("🔍 Search for a movie:")
if search_term:
    results = df[df['title'].str.contains(search_term, case=False, na=False)]
    results = results.sort_values(['avg_rating','rating_count'], ascending=False)

    st.subheader(f"Results for '{search_term}' ({len(results)} found)")

    st.dataframe(results[['title', 'year', 'avg_rating', 'rating_count']])
else:
    st.info("Enter a movie name above to search.")

log("✅ 1_Search_Movies page finished")
