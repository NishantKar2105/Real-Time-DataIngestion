# Real-Time-DataIngestion

# 🚀 Real-Time Delta Table Ingestion on Databricks Community Edition (CE)

This project demonstrates a **real-time data ingestion pipeline** built entirely on **Databricks Community Edition (CE)** using Delta Lake. It appends synthetic records at regular intervals and emails an HTML summary after each run.

---

## 📌 Why Databricks CE?

Due to several challenges with production-grade setups:

- ❌ **Azure Credits Unavailable** — Limited access to premium cloud resources.
- ❌ **ABFSS protocol incompatibility** — Spark read/write limitations with ADLS Gen2 via CE.
- ❌ **Local Spark is Complex** — Requires JVM setup, Hadoop compatibility, Delta config, and high memory.
  
We chose **Databricks CE** for:
- ✅ No infrastructure setup
- ✅ Built-in Delta Lake & Spark
- ✅ Notebooks and jobs-ready development environment

---

## 🛠 Features

### 🔁 Real-Time Ingestion
- Data appended at configurable intervals (e.g., every 5 minutes)
- Uses Faker to simulate:
  - Full name
  - Email
  - Address

### 📧 Email Notification
- Sends a styled HTML email after each append
- Includes:
  - 📦 Delta Table Version Info
  - 🕒 Timestamp
  - 🧾 Last 10 Records

### ⚙️ Parameterization
- Widgets let you dynamically set:
  - Number of rows to generate
  - Delta path
  - Output HTML path

---

## 📂 Code Components

### `append.py`
- Appends new data to the Delta table
- Adds `ingest_time` automatically to track when the data was written

### `initial_generate_data.py`
- Generates the Delta table with an initial dataset
- Safe to run only once

### `delta_utils.py`
Contains reusable helpers:
- `generate_fake_data()` – Fake name/email/address
- `get_recent_records()` – Get latest 10 records
- `get_latest_version_info()` – Return version, operation, timestamp, and user from Delta log
- `export_combined_html()` – Create combined HTML summary of version + data
- `send_email()` – Sends summary email using Gmail SMTP

### `full_pipeline.py`
- Executes the full pipeline:
  1. Generates data
  2. Appends to Delta
  3. Gets recent records + version info
  4. Exports HTML
  5. Sends email
  6. Repeats at intervals (via `time.sleep()`)

---

## ✅ Getting Started

1. Clone this repo:
   ```bash
   git clone https://github.com/<your-username>/real-time-delta-ingestion.git
   cd real-time-delta-ingestion
2.Upload files to Databricks CE

3.Create a new notebook and %run ./full_pipeline to begin automated ingestion.

## 📝 Requirements
Databricks Community Edition

Gmail App Password (for send_email())

## 📧 Email Setup Instructions
Turn on 2FA on your Gmail account
Create an App Password from Google Account > Security

Use it inside send_email():
- sender_email = "your@gmail.com"
- receiver_email = "you_or_team@gmail.com"
- password = "your_16_char_app_password"

## Future Improvements
Airflow/DAG-based scheduling
Add Slack notifications
Historical dashboard via Delta streaming

🧠 Author
Nishant Kar
