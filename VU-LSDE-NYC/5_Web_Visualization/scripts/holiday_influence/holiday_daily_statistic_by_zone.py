import os

from pyspark.sql.functions import col
from pyspark.sql.session import SparkSession
import openpyxl
import pandas


# Local mode
import java8

data_dir = "../../../Data"
zone_statistic_dir = data_dir + "/NYC_Zone_Static"
holiday_statistic_dir = zone_statistic_dir + "/holiday"
# Group 11 Databricks mode
# data_dir = "/dbfs/mnt/group11/Data"


year_statistic = "2018"

year_statistic_df = pandas.read_csv(data_dir + "/NYC_Zone_Static/" + year_statistic + "_zone_statistic.csv")
year_statistic_df["ycount"] = year_statistic_df["ycount"] / 365
year_statistic_df["gcount"] = year_statistic_df["gcount"] / 365
year_statistic_df["fhvcount"] = year_statistic_df["fhvcount"] / 365
year_statistic_df["sum"] = year_statistic_df["sum"] / 365
year_statistic_df = year_statistic_df[['ycount', 'gcount', 'fhvcount', 'sum']]

holiday_df = pandas.read_csv(data_dir + "/NYC_Holiday/holiday_id_date.csv")
holiday_df = holiday_df[(holiday_df.year == int(year_statistic))]
holiday_name_df = pandas.read_csv(data_dir + "/NYC_Holiday/holiday_id_name.csv")
holiday_df = pandas.merge(holiday_df, holiday_name_df, left_on='holiday_id', right_on='holiday_id')

holiday_df = holiday_df[(holiday_df.year == int(year_statistic))].reset_index()
spark = SparkSession.builder.master('local').appName('weather_statistic').getOrCreate()

for index, row in holiday_df.iterrows():
    year = str(row["year"])
    month = str(row["month"])
    day = str(row["day"])
    holiday_name = row["holiday_name"].lower().replace(" ", "_").replace("'", "")
    if len(month) == 1:
        month = "0" + month
    if len(day) == 1:
        day = "0" + day

    holiday_data = pandas.read_csv(data_dir + "/NYC_Zone_Static/daily_" + year + "_" + month + "_" + day + ".csv")
    holiday_data["difference"] = holiday_data["sum"] - year_statistic_df["sum"]
    holiday_data["percentage"] = holiday_data["difference"] / year_statistic_df["sum"]
    if not os.path.exists(zone_statistic_dir):
        os.mkdir(zone_statistic_dir)
    if not os.path.exists(holiday_statistic_dir):
        os.mkdir(holiday_statistic_dir)
    holiday_data.to_csv(holiday_statistic_dir + "/" + holiday_name + ".csv")
