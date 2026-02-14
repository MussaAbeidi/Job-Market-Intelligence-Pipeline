# Real-Time Job Market Intelligence Pipeline 🚀

A full-stack data engineering tool that automates the extraction and analysis of real-world job data. I built this to move beyond static scraping and handle dynamic, JavaScript-heavy job boards like *We Work Remotely*.

## 🏗 Architecture
This project uses a "Modern Data Stack" approach:
1.  **Dynamic Extraction:** Uses **Selenium Webdriver** to launch a real browser instance, handling infinite scroll and dynamic DOM rendering that standard libraries (like `Requests`) cannot touch.
2.  **Defensive Parsing:** Implements a robust `try-except` strategy to handle missing HTML tags without crashing the pipeline.
3.  **Storage Layer:** Persists data to a local **SQLite** database with automated de-duplication for historical analysis.
4.  **Machine Learning:** Applies **Unsupervised Learning (K-Means)** to discover hidden job categories based on title semantics (TF-IDF).

## 🛠 Tech Stack
-   **Automation:** Selenium, ChromeDriverManager
-   **Database:** SQLite3
-   **Analysis:** Pandas, Matplotlib, NumPy
-   **Machine Learning:** Scikit-Learn (K-Means, TF-IDF Vectorization)

## ⚡ Key Features
-   **Browser Automation:** Navigates to live websites, mimics human scrolling behavior, and handles lazy-loaded content.
-   **Smart Clustering:** Uses the **Elbow Method** logic to validate the optimal number of job clusters ($k$).
-   **Centroid Analysis:** Automatically extracts the "defining keywords" for each job cluster (e.g., distinguishing "Backend" roles from "Sales" roles).

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
4.  **Generate Visuals:**
    ```bash
    python analyze.py
    ```

## 📈 Results
The tool categorizes jobs into distinct market segments with high accuracy, visualizing the demand for specific skills.

![Market Trends Chart](market_trends.png)
*(Tracked Keywords: Python, JavaScript, TypeScript, Java, C++, SQL, React, AWS, Cloud, Data, AI)*

## 📊 Live Results (Feb 2026)
**Scale:** Analyzed **249 real-time job postings** across the entire platform.

**Market Insights:**
* **AI Dominance:** "AI" is the #1 most cited technology in the sample (16 mentions), outpacing traditional web frameworks like React and Django.
* **The "C++" Verification:** Analysis correctly filters for strict keyword matches, ensuring that common letters (like 'C') don't trigger false positives for languages like C++.
* **Cluster Analysis:** The K-Means algorithm ($k=5$) successfully separated roles into distinct categories without labeled training data:
    * **Cluster 0:** Product Engineering & Leadership
    * **Cluster 1:** Senior Web Development
    * **Cluster 2:** Sales & Operations
    * **Cluster 3:** Enterprise Business & Accounts
    * **Cluster 4:** Infrastructure, DevOps & AI

---
*Built by Mussa Abeidi as a Data Engineering Portfolio Project.*