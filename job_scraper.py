import time
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

DB_NAME = "real_jobs.db"

def init_db():
    """Initializes the database table for storing job listings."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                company TEXT,
                region TEXT,
                link TEXT,
                date_scraped TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def scrape_jobs():
    """
    Scrapes Python job listings from We Work Remotely.
    Uses Selenium to handle dynamic content loading.
    """
    print("Initializing browser...")
    options = Options()
    # options.add_argument("--headless")  # Uncomment to run without UI
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        url = "https://weworkremotely.com/remote-jobs/search?term=python"
        print(f"Navigating to source: {url}")
        driver.get(url)
        
        # Allow time for the initial DOM to render
        time.sleep(3)

        # Target the main job list, excluding the 'view all' button at the bottom
        job_cards = driver.find_elements(By.CSS_SELECTOR, "section.jobs li:not(.view-all)")
        print(f"Detected {len(job_cards)} listings. Extracting details...")

        data_payload = []

        for card in job_cards:
            try:
                # Extract details using specific class names found in the DOM
                title = card.find_element(By.CSS_SELECTOR, "h3.new-listing__header__title").text
                company = card.find_element(By.CSS_SELECTOR, "p.new-listing__company-name").text
                link = card.find_element(By.CSS_SELECTOR, "a.listing-link--unlocked").get_attribute("href")

                # Region is optional/variable, so handle gracefully
                try:
                    region = card.find_element(By.CSS_SELECTOR, "p.new-listing__company-headquarters").text
                except Exception:
                    region = "Remote"

                print(f" -> Parsed: {title} ({company})")
                data_payload.append((title, company, region, link))

            except Exception:
                # Skip non-job elements (e.g., ads or section headers injected into the list)
                continue

        # Transactional save to DB
        if data_payload:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM jobs")  # Clear previous session data
                cursor.executemany("INSERT INTO jobs (title, company, region, link) VALUES (?, ?, ?, ?)", data_payload)
                conn.commit()
            print(f"\nSuccess: Persisted {len(data_payload)} jobs to database.")
        else:
            print("\nWarning: No jobs found. Selector validation may be required.")

    finally:
        driver.quit()

if __name__ == "__main__":
    init_db()
    scrape_jobs()