import os

import pyspark.sql.functions as pyspark_func
from pyspark.sql.session import SparkSession
import openpyxl
import pandas

# Local mode
import java8
data_dir = "../../../Data"
statistic_file_dir = data_dir + "/NYC_Zone_Static/statistic_rush_hour"
statistic_csv_path = statistic_file_dir + "/rush_hour_by_p_id.csv"

## Group 11 Databricks mode
# data_dir = "/dbfs/mnt/group11/Data"

spark = SparkSession.builder.master('local').appName('weather_statistic').getOrCreate()
weather_data = spark.read \
    .option("header", "true") \
    .option("delimiter", ",") \
    .option("inferschema", "true") \
    .format("csv") \
    .load(data_dir + "/NYC_Zone_Static/all_max_hour_*.csv")

weather_data = weather_data.filter((pyspark_func.col('sum') > 5))
weather_data = weather_data.groupBy('p_id', 'p_hour').count()
weather_data = weather_data.toPandas()
idx = weather_data.groupby(['p_id'])['count'].transform(max) == weather_data['count']
rush_hour_df = weather_data[idx][['p_id', 'p_hour', 'count']].drop_duplicates('p_id')

if not os.path.exists(statistic_file_dir):
    os.mkdir(statistic_file_dir)
rush_hour_df.to_csv(statistic_csv_path)
