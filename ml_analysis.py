import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

DB_NAME = "job_market.db"

def run_ml_pipeline():
    """
    Reads job data from SQLite and performs Unsupervised Learning (K-Means)
    to discover hidden market segments in job titles.
    """
    
    # 1. Load Data
    try:
        with sqlite3.connect(DB_NAME) as conn:
            df = pd.read_sql("SELECT title FROM jobs", conn)
    except sqlite3.OperationalError:
        print("Error: Database not found. Please run job_scraper.py first.")
        return

    # Safety Check: We need enough data to form meaningful groups
    if len(df) < 5:
        print(f"Not enough data ({len(df)} records). Run the scraper again to get more jobs.")
        return

    print(f"--- Starting ML Analysis on {len(df)} job titles ---")

    # 2. Vectorization (The Translator)
    # Convert text titles into numerical vectors so the math can work.
    # stop_words='english' removes useless words like 'the', 'and', 'for'.
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df['title'])

    # 3. Clustering (The Sorter)
    # We ask the model to find 5 distinct groups of jobs.
    true_k = 5
    model = KMeans(n_clusters=true_k, init='k-means++', n_init=10, random_state=42)
    model.fit(X)

    # 4. Evaluation (The Grader)
    # Silhouette Score ranges from -1 to 1. 
    # A score > 0.1 means the clusters are reasonably distinct.
    score = silhouette_score(X, model.labels_)
    print(f"Clustering Confidence (Silhouette Score): {score:.3f}")

    # 5. Extract Insights
    print("\n--- Discovered Market Segments ---")
    
    # Grab the top words that define each cluster center
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()

    for i in range(true_k):
        print(f"\nCluster {i} Theme:")
        
        # Print the top 3 keywords that define this group
        top_terms = [terms[ind] for ind in order_centroids[i, :3]]
        print(f" -> Keywords: {', '.join(top_terms)}")
        
        # Show 2 actual job titles from this group as proof
        sample_jobs = df.iloc[model.labels_ == i]['title'].head(2).tolist()
        print(f" -> Examples: {sample_jobs}")

if __name__ == "__main__":
    run_ml_pipeline()