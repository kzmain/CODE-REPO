from pyspark.sql.functions import col
from pyspark.sql.session import SparkSession
from pyspark.sql import SQLContext

import os

java8_location = '/Library/Java/JavaVirtualMachines/liberica-jdk-1.8.0_202/Contents/Home'  # Set your own
os.environ['JAVA_HOME'] = java8_location


data_dir = "../Data"
year_statistic = "result_2018"

spark = SparkSession.builder.master('local').appName('weather_statistic').getOrCreate()
# sqlContext = SQLContext(sc)
spark.read.parquet(data_dir + "/NYC_Trip_Data/yellow_tripdata/" + year_statistic + "*").toPandas()
print()
# rush_hour_sta = spark.read \
#     .option("header", "true") \
#     .option("delimiter", ",") \
#     .option("inferschema", "true") \
#     .format("csv") \
#     .load(data_dir + "/NYC_Trip_Data/yellow_tripdata/" + year_statistic + "*.parquet")

rush_hour_sta = rush_hour_sta.groupBy('p_hour').sum()\
    .select(col("surcharge"))
rush_hour_sta = rush_hour_sta.toPandas()
print()