import sqlite3
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

DB_NAME = "job_market.db"

def init_db():
    """Ensures the database exists with the correct schema."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                company TEXT,
                region TEXT,
                link TEXT UNIQUE,
                date_scraped TEXT
            )
        """)
        conn.commit()

def scrape_jobs():
    """
    Scrapes WeWorkRemotely for Python jobs.
    Includes De-Duplication and Explicit Waits.
    """
    print("--- Starting Extraction Pipeline ---")
    
    # 1. Load existing links to prevent duplicates
    try:
        with sqlite3.connect(DB_NAME) as conn:
            # We fetch all links into a simple set for fast checking
            existing_links = set(row[0] for row in conn.execute("SELECT link FROM jobs"))
    except sqlite3.OperationalError:
        existing_links = set()

    options = Options()
    # options.add_argument("--headless") # Uncomment for production (no UI)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        url = "https://weworkremotely.com/remote-jobs/search?term=python"
        print(f"Navigating to: {url}")
        driver.get(url)
        
        # Wait for the job section to load (max 10 seconds)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "section.jobs")))
        
        # Expanded selector to find ALL jobs on the page
        job_cards = driver.find_elements(By.CSS_SELECTOR, "section.jobs li:not(.view-all)")
        print(f"Detected {len(job_cards)} listings. Processing...")

        new_jobs = []
        scrape_date = datetime.now().strftime("%Y-%m-%d")

        for card in job_cards:
            try:
                # Extract link first to check for duplicates
                link = card.find_element(By.CSS_SELECTOR, "a.listing-link--unlocked").get_attribute("href")
                
                if link in existing_links:
                    continue # Skip this job, we already have it

                title = card.find_element(By.CSS_SELECTOR, "h3.new-listing__header__title").text
                company = card.find_element(By.CSS_SELECTOR, "p.new-listing__company-name").text
                
                try:
                    region = card.find_element(By.CSS_SELECTOR, "p.new-listing__company-headquarters").text
                except:
                    region = "Remote"

                new_jobs.append((title, company, region, link, scrape_date))
                print(f" -> Found New Job: {title}")

            except Exception:
                continue

        # Transactional Save
        if new_jobs:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.executemany("""
                    INSERT OR IGNORE INTO jobs (title, company, region, link, date_scraped) 
                    VALUES (?, ?, ?, ?, ?)
                """, new_jobs)
                conn.commit()
            print(f"\nSuccess: Added {len(new_jobs)} new records to {DB_NAME}.")
        else:
            print("\nPipeline Complete. No new jobs found since last run.")

    finally:
        driver.quit()

if __name__ == "__main__":
    init_db()
    scrape_jobs()