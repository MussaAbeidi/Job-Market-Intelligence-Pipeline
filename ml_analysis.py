import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

DB_NAME = "job_market.db"

def run_ml_pipeline():
    # 1. Load Data
    with sqlite3.connect(DB_NAME) as conn:
        df = pd.read_sql("SELECT title FROM jobs", conn)

    # Need at least a few jobs to run clustering
    if len(df) < 5:
        print("Not enough data for Machine Learning yet. Run the scraper first!")
        return

    print(f"Training model on {len(df)} job titles...")

    # 2. Vectorization (Convert text to numbers)
    # TF-IDF penalizes common words (like "Senior") and boosts unique ones (like "Django")
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df['title'])

    # 3. Clustering (K-Means)
    # We use 3 clusters: usually splits into Data, Backend, and Fullstack/Web
    true_k = 3
    model = KMeans(n_clusters=true_k, init='k-means++', n_init=10, random_state=42)
    model.fit(X)

    # 4. Evaluation (Silhouette Score)
    # A score close to 1 is great, 0 is overlapping, -1 is wrong.
    score = silhouette_score(X, model.labels_)
    print(f"Clustering Performance (Silhouette Score): {score:.3f}")

    # 5. Insight Extraction (The "Why")
    print("\n--- Market Segmentation Results ---")
    
    # Get the top keywords for each cluster center
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()

    for i in range(true_k):
        print(f"\nCluster {i} (Key Themes):")
        # Print the top 4 words that define this group
        top_terms = [terms[ind] for ind in order_centroids[i, :4]]
        print(f" -> {', '.join(top_terms)}")
        
        # Show sample jobs from this cluster
        cluster_jobs = df.iloc[model.labels_ == i]['title'].head(3).tolist()
        print(f"    Examples: {cluster_jobs}")

if __name__ == "__main__":
    run_ml_pipeline()