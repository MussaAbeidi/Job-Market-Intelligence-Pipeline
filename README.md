# Job Market Analyzer + ML Clustering

I built this tool to get a better look at what's actually happening in the job market. It’s a full pipeline that scrapes job data, stores it in a database, and uses K-Means clustering to group roles based on their titles.

## How it works
1. **Scraping:** Uses `Requests` and `BeautifulSoup` to pull job listings from the web.
2. **Database:** Saves everything to a local `SQLite` database so I can run analysis without re-scraping.
3. **ML Clustering:** Uses `Scikit-Learn` (TF-IDF + K-Means) to categorize jobs. This helps find patterns between "Engineer" vs "Developer" vs "Management" roles automatically.
4. **Viz:** Generates bar charts with `Matplotlib` to show where the jobs are and what skills are trending.

## Tech Used
- **Python** (Pandas, Scikit-Learn, Matplotlib, BS4)
- **SQL** (SQLite3)
- **Git** for version control

## Setup
- `pip install -r requirements.txt`
- Run `job_scraper.py` to get the data.
- Run `ml_analysis.py` to see the machine learning clusters.