# Job Market Intelligence Pipeline 📊

A full-stack data engineering project designed to scrape, store, and analyze job market data using Python. I built this to move beyond simple keyword matching and use Unsupervised Machine Learning to discover hidden categories in job titles.

## Architecture
1. **ETL Pipeline:** - **Extract:** Scrapes job data using `Requests` + `BeautifulSoup`. Includes defensive error handling for robust parsing.
   - **Transform:** Cleanses text and standardizes data formats.
   - **Load:** Persists data into a `SQLite` database for historical tracking.
2. **Analysis Engine:**
   - **Statistical:** `Pandas` for aggregation and `Matplotlib` for trend visualization.
   - **Machine Learning:** `Scikit-Learn` implementation of K-Means Clustering to group jobs automatically.
   - **Validation:** Uses the **Elbow Method** to mathematically determine the optimal number of job clusters.

## Key Technical Decisions
- **Why SQLite?** For a project of this scale (<100k records), a lightweight, serverless database is more performant than Postgres/MySQL and removes the need for complex docker containers.
- **Why TF-IDF?** Simple word counts (Bag of Words) ignore context. TF-IDF helps weight unique technical terms (like "Kubernetes") higher than generic terms (like "Manager").
- **Why K-Means?** It is efficient for unlabelled textual data. I implemented the **Elbow Method** to validate my choice of `k=3` clusters, minimizing the inertia (sum of squared distances).

## Quick Start
1. Install dependencies:
   ```bash
   pip install -r requirements.txt