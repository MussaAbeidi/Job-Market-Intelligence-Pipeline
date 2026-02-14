import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_NAME = "job_market.db"

def generate_visuals():
    with sqlite3.connect(DB_NAME) as conn:
        df = pd.read_sql("SELECT * FROM jobs", conn)

    if df.empty:
        print("No data available to analyze.")
        return

    print(f"Analyzing {len(df)} total records...")

    # Define the tech stack we want to measure
    keywords = [
        'Python', 'JavaScript', 'TypeScript', 'Java', 'C++', 
        'SQL', 'React', 'AWS', 'Cloud', 'Data', 'AI'
    ]
    
    # Count occurrences (Case Insensitive)
    counts = {}
    for tech in keywords:
        counts[tech] = df['title'].str.contains(tech, case=False, regex=False).sum()

    # Create DataFrame for plotting
    stats = pd.Series(counts).sort_values()

    # Plot
    plt.figure(figsize=(10, 6))
    stats.plot(kind='barh', color='#4a90e2')
    plt.title(f"Tech Stack Demand (Sample Size: {len(df)})")
    plt.xlabel("Number of Job Postings")
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig("market_trends.png")
    print("Graph saved: market_trends.png")

if __name__ == "__main__":
    generate_visuals()