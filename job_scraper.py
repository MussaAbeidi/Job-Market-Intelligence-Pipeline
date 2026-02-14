import requests
from bs4 import BeautifulSoup
import sqlite3

def init_db():
    # Setup the local table if it doesn't exist yet
    with sqlite3.connect("jobs.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                title TEXT,
                company TEXT,
                location TEXT
            )
        """)
        conn.commit()

def run_scraper():
    url = "https://realpython.github.io/fake-jobs/"
    
    # Fetch the page; add a check to make sure the site is up
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch data. Status: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, "html.parser")
    # Narrow down to the container holding all the job cards
    results = soup.find(id="ResultsContainer")
    job_cards = results.find_all("div", class_="card-content")

    with sqlite3.connect("jobs.db") as conn:
        cursor = conn.cursor()
        
        # Flush the old table so we aren't doubling up on data
        cursor.execute("DELETE FROM jobs")
        
        print(f"Syncing {len(job_cards)} jobs to the database...")

        for card in job_cards:
            title = card.find("h2", class_="title").text.strip()
            company = card.find("h3", class_="company").text.strip()
            location = card.find("p", class_="location").text.strip()

            cursor.execute("INSERT INTO jobs VALUES (?, ?, ?)", (title, company, location))
        
        conn.commit()
    
    print("Refresh complete. jobs.db is up to date.")

if __name__ == "__main__":
    init_db()
    run_scraper()