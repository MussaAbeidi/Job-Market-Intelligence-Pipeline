# Real-Time Job Market Intelligence Pipeline 🚀

A full-stack data engineering tool that automates the extraction and analysis of real-world job data. I built this to move beyond static scraping and handle dynamic, JavaScript-heavy job boards like *We Work Remotely*.

## 🏗 Architecture
This project uses a "Modern Data Stack" approach:
1.  **Dynamic Extraction:** Uses **Selenium Webdriver** to launch a real browser instance, handling infinite scroll and dynamic DOM rendering that standard libraries (like `Requests`) cannot touch.
2.  **Defensive Parsing:** Implements a robust `try-except` strategy to handle missing HTML tags without crashing the pipeline.
3.  **Storage Layer:** Persists data to a local **SQLite** database for historical analysis.
4.  **Machine Learning:** Applies **Unsupervised Learning (K-Means)** to discover hidden job categories based on title semantics (TF-IDF).



## 🛠 Tech Stack
-   **Automation:** Selenium, ChromeDriverManager
-   **Database:** SQLite3
-   **Analysis:** Pandas, Matplotlib, NumPy
-   **Machine Learning:** Scikit-Learn (K-Means, TF-IDF Vectorization)

## ⚡ Key Features
-   **Browser Automation:** Navigates to live websites, scrolls to load lazy-loaded content, and mimics human behavior.
-   **Smart Clustering:** Uses the **Elbow Method** to mathematically validate the optimal number of job clusters ($k$).
-   **Centroid Analysis:** Automatically extracts the "defining keywords" for each job cluster (e.g., distinguishing "Backend" roles from "Data Science" roles).

## 🚀 How to Run
1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the Scraper:**
    *(Note: This will launch a visible Chrome window to demonstrate the automation)*
    ```bash
    python job_scraper.py
    ```
3.  **Run the Analysis:**
    ```bash
    python ml_analysis.py
    ```

## 📈 Results
The tool currently categorizes jobs into distinct market segments with high accuracy, visualizing the demand for specific skills like **Python**, **AWS**, and **React**.

![Market Trends Chart](market_trends.png)

## 📊 Live Results (Feb 2026)
The model successfully identified 3 distinct market segments from live job data:
1.  **Cluster 0 (US Remote):** High-paying roles restricted to US residents (`usa`, `100% remote`).
2.  **Cluster 1 (Core Engineering):** Traditional backend development roles (`backend`, `python`, `senior`).
3.  **Cluster 2 (AI/ML):** Emerging demand for Large Language Model engineering (`llm`, `ai`, `genai`).

**Silhouette Score:** 0.51 (indicating strong separation between clusters).