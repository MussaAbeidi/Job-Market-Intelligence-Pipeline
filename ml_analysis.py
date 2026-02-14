import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def run_clustering_pipeline():
    # 1. Load Data
    with sqlite3.connect("jobs.db") as conn:
        df = pd.read_sql("SELECT title FROM jobs", conn)

    if len(df) < 10:
        print("Not enough data to run meaningful clustering.")
        return

    print(f"Vectorizing {len(df)} job titles...")

    # 2. Feature Engineering (TF-IDF)
    # We strip out English 'stop words' (and, the, is) to focus on the nouns/verbs.
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    X = vectorizer.fit_transform(df['title'])

    # 3. Determine Optimal K (Elbow Method)
    # We test k=1 to k=10 to see where the 'inertia' (error) levels off.
    inertias = []
    k_range = range(1, 10)
    
    print("Calculating Elbow curve (optimal k)...")
    for k in k_range:
        model = KMeans(n_clusters=k, n_init=10, random_state=42)
        model.fit(X)
        inertias.append(model.inertia_)

    # Save the Elbow plot for the report
    plt.figure(figsize=(8, 4))
    plt.plot(k_range, inertias, 'bx-')
    plt.xlabel('k (Number of Clusters)')
    plt.ylabel('Inertia')
    plt.title('Elbow Method For Optimal k')
    plt.savefig("elbow_method.png")

    # 4. Apply Final Clustering
    # Based on the elbow plot for this specific dataset, k=3 is usually the inflection point.
    true_k = 3
    model = KMeans(n_clusters=true_k, n_init=10, random_state=42)
    model.fit(X)
    
    # 5. Extract Insights (Centroids)
    print("\n--- Cluster Analysis ---")
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()

    for i in range(true_k):
        print(f"\nCluster {i} Top Terms:", end=" ")
        # Print the top 5 words that are 'closest' to the center of this cluster
        for ind in order_centroids[i, :5]:
            print(f"[{terms[ind]}]", end=" ")
        print()

if __name__ == "__main__":
    run_clustering_pipeline()