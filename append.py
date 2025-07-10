# Databricks notebook source
# MAGIC %run "/Users/nishantkar24@gmail.com/Real-Time Data ingestion/delta_utils"

# COMMAND ----------

# MAGIC %run "/Users/nishantkar24@gmail.com/Real-Time Data ingestion/initial_generate_data.py"

# COMMAND ----------

def append_to_delta_table(df, delta_path=DELTA_PATH):

    df.write.format("delta").mode("append").save(delta_path)


# COMMAND ----------

#Recent Records
def get_recent_records(spark, limit=10 , delta_path=DELTA_PATH):
    df= spark.read.format('delta').load(delta_path)
    return df.orderBy('ingest_time', ascending=False).limit(limit)




# COMMAND ----------

## Getting info regarding the latest version

def get_latest_version_info(spark, delta_path=DELTA_PATH):
    try:
        history_df= spark.sql(f"DESCRIBE HISTORY delta.`{delta_path}`")
        latest= history_df.orderBy("version", ascending=False).limit(1).collect()[0]
        if "userName" not in latest:
            person="unknown"
        else:
            person= latest["userName"]

        return {
            "version":latest["version"],
            "timestamp":latest["timestamp"],
            "operation":latest["operation"],
            "user" : person
        }
    except Exception as e:
        print(" Failed to get the latest version info", str(e))
        return{
            "version":'unknown',
            "timestamp":"unknown",
            "operation":"unknown",
            "user" : 'unknown'
        }

# COMMAND ----------

def export_combined_html(df_recent,version_info,html_path=HTML_PATH):
    # Convert Spark DataFrame to HTML table
    df_html=df_recent.toPandas().to_html(index=False,escape=False)

    # Build the full HTML content with version info
    html = f"""
    <h2>Delta Table Version: {version_info['version']}</h2>
    <p>Timestamp: {version_info["timestamp"]}</p>
    <p> User: {version_info['user']}</p>
    <p> Mode: {version_info['operation']}</p>
    <hr>
    <h2> Most Recent 10 Records</h2>
    {df_html}
    """

    # Save HTML to DBFS path
    dbutils.fs.put(html_path, html, overwrite=True)
    print(f"HTML summary exported to: {html_path}")
    return html


# COMMAND ----------

