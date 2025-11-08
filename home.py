import streamlit as st
from logger import log

st.set_page_config(page_title="Movie Analysis App", layout="wide")

log("🏠 Home page started")

st.title("🎬 Welcome to the Movie Analysis App!")
st.write("Choose a page from the left sidebar 👈")

log("✅ Home page loaded successfully")
