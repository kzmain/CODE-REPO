import openpyxl
from pyspark.sql.session import SparkSession
import pandas

# Local mode
data_dir = "../Data"
# Group 11 Databricks mode
# data_dir = "/dbfs/mnt/group11/Data"

spark = SparkSession.builder.master('local').appName('weather_statistic').getOrCreate()
weather_data = spark.read \
    .option("header", "true") \
    .option("delimiter", ",") \
    .option("inferschema", "true") \
    .format("csv") \
    .load(data_dir + "/NYC_Zone_Static/daily*.csv")

weather_data.toPandas().to_excel(data_dir + "/NYC_Weathers/all_weather_data.xlsx")
weather_data.groupBy("weather").count().toPandas().to_excel(data_dir + "/NYC_Weathers/weather_static.xlsx")

print()
