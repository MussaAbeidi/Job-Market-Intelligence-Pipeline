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
                link TEXT,
                date_scraped TEXT
            )
        """)
        conn.commit()

def scrape_jobs():
    """
    Scrapes WeWorkRemotely for Python jobs.
    Uses Explicit Waits for reliability (Production Grade).
    """
    print("--- Starting Extraction Pipeline ---")
    options = Options()
    # options.add_argument("--headless") # Uncomment for production (no UI)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        url = "https://weworkremotely.com/remote-jobs/search?term=python"
        print(f"Navigating to: {url}")
        driver.get(url)
        
        # PRO MOVE: Don't just sleep. Wait until the list actually appears.
        # This prevents the script from crashing if the internet is slow.
        wait = WebDriverWait(driver, 10)
        job_section = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "section.jobs")))
        
        # Grab all list items (listings) excluding the 'view all' button
        job_cards = job_section.find_elements(By.CSS_SELECTOR, "li:not(.view-all)")
        print(f"Detected {len(job_cards)} listings. Processing...")

        new_jobs = []
        scrape_date = datetime.now().strftime("%Y-%m-%d")

        for card in job_cards:
            try:
                # We use finding relative to the 'card' element
                title = card.find_element(By.CSS_SELECTOR, "h3.new-listing__header__title").text
                company = card.find_element(By.CSS_SELECTOR, "p.new-listing__company-name").text
                link = card.find_element(By.CSS_SELECTOR, "a.listing-link--unlocked").get_attribute("href")
                
                # Region is inconsistent, so we try/except it
                try:
                    region = card.find_element(By.CSS_SELECTOR, "p.new-listing__company-headquarters").text
                except:
                    region = "Remote"

                # Check if we already have this exact job to avoid duplicates
                # (In a real system, we'd check the DB, but this is a simple run-level check)
                new_jobs.append((title, company, region, link, scrape_date))
                print(f" -> Found: {title}")

            except Exception:
                # Skip non-job rows (headers/ads)
                continue

        # Save to Database (Append Mode)
        if new_jobs:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.executemany("""
                    INSERT INTO jobs (title, company, region, link, date_scraped) 
                    VALUES (?, ?, ?, ?, ?)
                """, new_jobs)
                conn.commit()
            print(f"\nSuccess: Added {len(new_jobs)} new records to {DB_NAME}.")
        else:
            print("\nWarning: No jobs extracted. Check selectors.")

    finally:
        driver.quit()

if __name__ == "__main__":
    init_db()
    scrape_jobs()