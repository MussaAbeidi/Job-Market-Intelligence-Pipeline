import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def generate_insights():
    # Load data into a dataframe
    with sqlite3.connect("jobs.db") as conn:
        df = pd.read_sql("SELECT * FROM jobs", conn)

    if df.empty:
        print("Nothing to analyze. Run the scraper first.")
        return

    # Check for specific tech terms in the titles
    stack = ['Python', 'Engineer', 'Manager', 'Developer', 'Data']
    
    # Calculate frequencies using pandas string methods
    counts = {word: df['title'].str.contains(word, case=False).sum() for word in stack}
    results = pd.Series(counts).sort_values(ascending=False)

    print("\n--- Market Demand (Title Keywords) ---")
    print(results)

    # Plot the results
    plt.figure(figsize=(10, 6))
    results.plot(kind='bar', color='teal', alpha=0.8)
    
    plt.title("Keyword Frequency in Job Market Data")
    plt.ylabel("Postings")
    plt.xticks(rotation=0)
    plt.tight_layout()
    
    plt.savefig("skills_chart.png")
    print("\nChart generated: skills_chart.png")

if __name__ == "__main__":
    generate_insights()