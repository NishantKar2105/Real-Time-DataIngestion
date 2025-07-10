# Databricks notebook source
# MAGIC %run "/Users/nishantkar24@gmail.com/Real-Time Data ingestion/delta_utils"

# COMMAND ----------

# MAGIC %run "/Users/nishantkar24@gmail.com/Real-Time Data ingestion/initial_generate_data.py"

# COMMAND ----------

# MAGIC %run "/Users/nishantkar24@gmail.com/Real-Time Data ingestion/append"

# COMMAND ----------

import os
from dotenv import load_dotenv

load_dotenv()

sender_email = os.getenv("EMAIL_USER")
receiver_email = os.getenv("EMAIL_TO")
Password = os.getenv("EMAIL_PASS")


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(html, sender_email, receiver_email, password):
    sender_email =sender_email
    receiver_email = receiver_email
    password = Password 

    msg =MIMEMultipart("alternative")
    msg["Subject"] = "Delta Pipeline UpdaTe"
    msg["From"]= sender_email
    msg["To"]= receiver_email

    part =MIMEText(html_content, "html")
    msg.attach(part)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Email sent successfully.")
    except Exception as e:
        print("Failed to send email:", e)


# COMMAND ----------

import time

dbutils.widgets.text("num_rows", "5", "Number of rows to generate")
num_rows = int(dbutils.widgets.get("num_rows"))
print(f"Generating {num_rows} rows")


while True:
    df =generate_fake_data(spark,num_rows)
    append_to_delta_table(df)
    df_recent = get_recent_records(spark, 10)
    display(df_recent)

    version_info = get_latest_version_info(spark)
    print(f" Version: {version_info['version']}")
    print(f" Timestamp: {version_info['timestamp']}" )
    print(f" Operation: {version_info['operation']}")
    print(f" User : {version_info['user']}")

    html=export_combined_html(df_recent, version_info)
    send_email(
        html,
        sender_email=sender_email,
        receiver_email=receiver_email,
        password=password
    )   

    print("Sleeping 5 minutes...")
    time.sleep(5*60)


# COMMAND ----------

