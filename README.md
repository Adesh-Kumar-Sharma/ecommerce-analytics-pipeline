# E-commerce Analytics Pipeline & Dashboard

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-brightgreen.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-orange.svg)

An end-to-end data engineering project that builds a complete ETL pipeline for e-commerce data, stores it in a PostgreSQL data warehouse, and presents real-time business intelligence through an interactive Streamlit dashboard.

---

## 🚀 Live Demo

**[<-- View the Live Dashboard Here -->](https://ecom-etl-pipeline.streamlit.app/)**

---

## 📋 Table of Contents

- [Key Features](#✨-key-features)
- [Tech Stack](#🛠-tech-stack)
- [Data Pipeline Architecture](#🏗️-data-pipeline-architecture)
- [Local Setup and Usage](#⚙️-local-setup-and-usage)
- [Dashboard Features](#📊-dashboard-features)
- [Deployment](#☁️-deployment)
- [Homepage Screenshot](#📷-homepage-screenshot)
- [YouTube Demo](#📺-youtube-demo)

---

## ✨ Key Features

- **Automated ETL Pipeline**: Extracts raw data, cleans and transforms it with business logic, and loads it into a structured data warehouse.
- **Interactive Dashboard**: A multi-page Streamlit application for real-time BI, featuring KPIs, trend analysis, and forecasting.
- **Cloud-Native Database**: Utilizes a serverless PostgreSQL database from Neon.tech for scalable and efficient data storage.
- **Scheduled Updates**: The pipeline is designed with scheduling in mind, simulating daily full-loads and hourly incremental updates.
- **Business Intelligence**: Generates key metrics like customer lifetime value, product performance, revenue trends, and retention rates.

---

## 🛠 Tech Stack

| Category      | Technology                                                                                                                              |
|---------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| **ETL & Backend** | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white) |
| **Database** | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white) (Neon.tech)          |
| **Dashboard** | ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white) ![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)          |
| **Deployment** | ![Streamlit Cloud](https://img.shields.io/badge/Streamlit_Cloud-0D2A38?style=for-the-badge&logo=streamlit&logoColor=white)              |

---

## 🏗️ Data Pipeline Architecture

This project follows a standard Extract, Transform, Load (ETL) process:

1. **Extract**: Raw data (e.g., `customers.csv`, `orders.csv`) is extracted. If the data is not present, a synthetic data generation script creates it automatically.
2. **Transform**: The raw data is cleaned, validated, and enriched using Pandas. Business logic is applied to calculate new metrics and create analytical tables (e.g., `customer_metrics`, `monthly_summary`).
3. **Load**: The transformed, clean data is loaded into a PostgreSQL database hosted on Neon. The database schema is optimized with indexes and views for fast analytical queries.
4. **Analyze & Visualize**: The Streamlit dashboard queries the PostgreSQL database to visualize the data and provide real-time business insights.

---

## ⚙️ Local Setup and Usage

Follow these steps to run the project on your local machine.

1. **Prerequisites**

   - Python 3.11
   - Git

2. **Clone the Repository**

   ```bash
   git clone [https://github.com/your-username/ecommerce-analytics-pipeline.git](https://github.com/your-username/ecommerce-analytics-pipeline.git)
   cd ecommerce-analytics-pipeline
   ```

3. **Set Up the Environment**

   Create and activate a Python virtual environment:

   ```bash
   py -3.9 -m venv .venv
   ```

4. **Create the virtual environment**

   ```bash
   py -3.11 -m venv .venv
   ```

5. **Activate it**

   ```bash
   ./.venv/Scripts/Activate.ps1
   ```

6. **Install the required dependencies**

   ```bash
   pip install -r requirements.txt
   ```

7. **Configure the Database**

   - Sign up for a free PostgreSQL database at Neon.tech.

   - Create a file named .env in the root of the project.

   - Add your database connection string to the .env file:

      ```env
      DATABASE_URL="postgresql://user:password@host:port/dbname"
      ```

8. **Run the ETL Pipeline**

   Execute the main pipeline script to populate your database:

   ```bash
   python -m etl.pipeline
   ```

9. **Launch the Dashboard**

   Run the Streamlit app to view the interactive dashboard:

   ```bash
   streamlit run dashboard/app.py
   ```

   The dashboard will be available at [http://localhost:8501](http://localhost:8501) or a similar port depending on your machine.

## 📊 Dashboard Features

   The dashboard is organized into several pages for comprehensive analysis:

   1. **Overview**: High-level KPIs, daily revenue trends, and an orders vs. customers chart.

   2. **Customers**: Detailed analysis of customer segments and retention metrics.

   3. **Products**: Treemap of revenue by category and a list of the top-performing products.

   4. **Advanced** Analytics: Monthly performance, revenue growth rate, and forecasting.

## ☁️ Deployment

- The dashboard for this project is deployed on Streamlit Community Cloud.

- The app is linked to this GitHub repository.

- The DATABASE_URL is configured securely using Streamlit's secrets management.

- The app automatically redeploys upon any push to the main branch.

## 📷 Homepage Screenshot

![Homepage Screenshot](public/homepage-screenshot.png)

## 📺 YouTube Demo

Watch the full demo and walkthrough of this project on YouTube:  **[E-commerce ETL Pipeline Demo](https://www.youtube.com/watch?v=7NimOCNB0WQ)**
