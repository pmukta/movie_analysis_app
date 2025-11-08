import pandas as pd
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print("🔄 Rebuilding data_fast.pkl ...")
start = time.time()

# Load Movies Metadata
movies = pd.read_csv(
    os.path.join(BASE_DIR, "movies_metadata.csv"),
    usecols=['id', 'title', 'release_date', 'vote_average', 'vote_count'],
    low_memory=False
)
print("✅ movies_metadata.csv loaded")

# Fix ID
movies['id'] = pd.to_numeric(movies['id'], errors='coerce')
movies.dropna(subset=['id'], inplace=True)
movies['id'] = movies['id'].astype('int32')

# Extract Year
movies['year'] = movies['release_date'].astype(str).str[:4]
movies = movies[movies['year'].str.isdigit()]
movies['year'] = movies['year'].astype('int16')

# Load Ratings
ratings = pd.read_csv(
    os.path.join(BASE_DIR, "ratings.csv"),
    usecols=['movieId', 'rating'],
    dtype={'movieId': 'int32', 'rating': 'float16'}
)
print("✅ ratings.csv loaded")

# Convert MovieLens 0–5 scale to 0–10
ratings['rating_10'] = (ratings['rating'] * 2).astype('float16')

# Keep only valid ID matches
valid_ids = movies['id'].unique()
ratings = ratings[ratings['movieId'].isin(valid_ids)]

# Merge
print("🔗 Merging ...")
merged = ratings.merge(movies, left_on='movieId', right_on='id', how='inner')

# Save as fast format
output = os.path.join(BASE_DIR, "data_fast.pkl")
merged.to_pickle(output)

print(f"🎯 Saved to {output}")
print(f"⏱ Total Time: {(time.time() - start):.2f} sec")
print("🚀 Done!")
