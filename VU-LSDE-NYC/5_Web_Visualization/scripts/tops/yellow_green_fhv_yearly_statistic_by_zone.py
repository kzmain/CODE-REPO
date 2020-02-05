from pyspark.sql.functions import col
from pyspark.sql.session import SparkSession
import openpyxl
import pandas

# Local mode
import java8
data_dir = "../../../Data"

# Group 11 Databricks mode
# data_dir = "/dbfs/mnt/group11/Data"

year_statistic = "2018"

spark = SparkSession.builder.master('local').appName('weather_statistic').getOrCreate()
weather_data = spark.read \
    .option("header", "true") \
    .option("delimiter", ",") \
    .option("inferschema", "true") \
    .format("csv") \
    .load(data_dir + "/NYC_Zone_Static/daily_" + year_statistic + "*.csv")
weather_data = weather_data.groupBy('p_id').sum()\
    .select(col("p_id"), col("sum(ycount)").alias("ycount"), col("sum(gcount)").alias("gcount"), col("sum(hfcount)").alias("hfcount"), col("sum(fcount)").alias("fcount"), col("sum(sum)").alias("sum"))\
    .sort(col("p_id"))
weather_data = weather_data.toPandas()
weather_data["fhvcount"] = weather_data["hfcount"] + weather_data["fcount"]
weather_data = weather_data[['p_id', 'ycount', 'gcount', 'fhvcount', 'sum']]
weather_data.to_csv(data_dir + "/NYC_Zone_Static/" + year_statistic + "_zone_statistic.csv")

