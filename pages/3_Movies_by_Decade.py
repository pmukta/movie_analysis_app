import pandas as pd
import os
import streamlit as st
from logger import log

# Correct BASE_DIR: one level up from pages/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load preprocessed data
data_path = os.path.join(BASE_DIR, "data_fast.pkl")
log(f"📂 Loading preprocessed data from {data_path}...")
df = pd.read_pickle(data_path)

# Drop movies with no year
df = df.dropna(subset=['year']).copy()

# Create a decade column
df['decade'] = (df['year'] // 10) * 10

# Get unique decades sorted
decade_options = sorted(df['decade'].unique())

# Streamlit UI
st.title("🎬 Movies by Decade")

# Dropdown to select decade
selected_decade = st.selectbox(
    "Select a decade:",
    decade_options,
    index=decade_options.index(2000) if 2000 in decade_options else 0
)

# Number of movies to display
num_records = st.number_input(
    "Number of movies to display:",
    min_value=1,
    max_value=1000,
    value=20,
    step=1
)

# Filter movies by selected decade
movies_in_decade = df[df['decade'] == selected_decade].copy()

# Sort by average rating
movies_in_decade = movies_in_decade.sort_values('avg_rating', ascending=False)

# Display top N movies
if not movies_in_decade.empty:
    st.dataframe(
        movies_in_decade[['title', 'year', 'avg_rating', 'rating_count']].head(num_records).reset_index(drop=True)
    )
else:
    st.write(f"No movies found for the {selected_decade}s.")
