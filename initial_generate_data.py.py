# Databricks notebook source
# MAGIC %pip install faker
# MAGIC

# COMMAND ----------

# MAGIC %run "/Users/nishantkar24@gmail.com/Real-Time Data ingestion/delta_utils"
# MAGIC

# COMMAND ----------

#  Data Generation
def generate_fake_data(spark,num_rows=10):
    now= get_current_time()
    data= [(faker.name(), faker.address(), faker.email()) for _ in range(num_rows)]
    df=spark.createDataFrame(data, ["name", "address", "email"])
    return df.withColumn("ingest_time", lit(now))


# COMMAND ----------

def write_initial_delta_table(df,delta_path=DELTA_PATH):
    df.write.format("delta").mode("overwrite").save(delta_path)

# COMMAND ----------

