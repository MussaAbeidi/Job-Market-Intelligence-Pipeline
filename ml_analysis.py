import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def cluster_jobs():
    with sqlite3.connect("jobs.db") as conn:
        df = pd.read_sql("SELECT title FROM jobs", conn)

    if df.empty:
        print("Empty dataset. Skipping ML.")
        return

    print(f"Clustering {len(df)} titles...")

    # Vectorize the text: ignore common english filler words
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df['title'])

    # Using 3 clusters to differentiate between Eng, Dev, and Admin/Management
    # k-means++ ensures a smarter initial placement of centroids
    model = KMeans(n_clusters=3, init='k-means++', n_init=10, random_state=42)
    model.fit(X)

    df['group'] = model.labels_

    print("\n--- ML Categorization Results ---")
    for group_id in range(3):
        print(f"\nGroup {group_id} Samples:")
        # Show top titles for each found cluster
        print(df[df['group'] == group_id]['title'].head(5).to_string(index=False))

if __name__ == "__main__":
    cluster_jobs()