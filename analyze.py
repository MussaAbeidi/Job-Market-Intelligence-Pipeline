import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def generate_market_report():
    # Load the dataset
    try:
        with sqlite3.connect("jobs.db") as conn:
            df = pd.read_sql("SELECT * FROM jobs", conn)
    except pd.io.sql.DatabaseError:
        print("Database not found. Please run job_scraper.py first.")
        return

    if df.empty:
        print("Database is empty. Nothing to analyze.")
        return

    print(f"Generating report for {len(df)} job postings...")

    # 1. Define the 'Tech Stack' we are interested in tracking
    # We use a case-insensitive search to catch 'python' and 'Python'
    target_skills = ['Python', 'Engineer', 'Manager', 'Developer', 'Data', 'Senior']
    
    skill_counts = {}
    for skill in target_skills:
        skill_counts[skill] = df['title'].str.contains(skill, case=False).sum()

    # 2. visualiztion
    # converting to a Series makes plotting with pandas much easier
    s_skills = pd.Series(skill_counts).sort_values(ascending=True)

    plt.figure(figsize=(10, 6))
    s_skills.plot(kind='barh', color='#2c3e50', alpha=0.9)
    
    plt.title("Most Demanded Keywords in Job Titles")
    plt.xlabel("Frequency")
    plt.tight_layout()
    
    # Save to disk so we can embed this in the README later
    plt.savefig("market_demand_chart.png")
    print("Report generated: market_demand_chart.png")

if __name__ == "__main__":
    generate_market_report()