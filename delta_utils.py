# Databricks notebook source
# MAGIC %pip install faker

# COMMAND ----------

from faker import Faker
from datetime import datetime
import pytz
from pyspark.sql.functions import lit
import pandas as pd

# Initialize Faker and config
faker = Faker()
TIMEZONE = "Asia/Kolkata"
DELTA_PATH = "/dbfs/delta/fake_people_table"
HTML_PATH = "/FileStore/html/summary.html"


# Timestamp Utilities

def get_current_time():
    return datetime.now(pytz.timezone(TIMEZONE))



# COMMAND ----------

spark.conf.get("spark.databricks.clusterUsageTags.clusterId") 

# COMMAND ----------

