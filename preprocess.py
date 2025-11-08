import pandas as pd
import os
from logger import log

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def preprocess_data():
    log("📂 Loading raw CSV files...")

    movies = pd.read_csv(os.path.join(BASE_DIR, "movies_metadata.csv"), low_memory=False)
    ratings = pd.read_csv(os.path.join(BASE_DIR, "ratings.csv"))

    log("🔍 Converting ratings to 10-point scale...")
    ratings['rating_10'] = ratings['rating'] * 2

    log("🔢 Converting IDs to numeric...")
    movies['id'] = pd.to_numeric(movies['id'], errors='coerce')
    ratings['movieId'] = pd.to_numeric(ratings['movieId'], errors='coerce')
    movies = movies.dropna(subset=['id']).copy()
    ratings = ratings.dropna(subset=['movieId']).copy()
    movies['id'] = movies['id'].astype('int64')
    ratings['movieId'] = ratings['movieId'].astype('int64')

    log("🗓️ Extracting year from release_date...")
    if 'release_date' in movies.columns:
        movies['year'] = pd.to_datetime(movies['release_date'], errors='coerce').dt.year

    # Aggregate ratings by movie
    log("📊 Aggregating ratings by movie...")
    ratings_agg = ratings.groupby('movieId', as_index=False).agg(
        rating_count=('rating_10', 'size'),
        avg_rating=('rating_10', 'mean')
    )

    log("🔄 Merging aggregated ratings with movie info...")
    merged = pd.merge(movies, ratings_agg, left_on='id', right_on='movieId', how='left')

    # Fill missing ratings for movies with no ratings
    merged['rating_count'] = merged['rating_count'].fillna(0).astype('int')
    merged['avg_rating'] = merged['avg_rating'].fillna(0)

    log(f"✅ Final dataset: {len(merged)} rows")

    output_path = os.path.join(BASE_DIR, "data_fast.pkl")
    merged.to_pickle(output_path)
    log(f"💾 Saved preprocessed movie-level data to {output_path}")

if __name__ == "__main__":
    preprocess_data()
