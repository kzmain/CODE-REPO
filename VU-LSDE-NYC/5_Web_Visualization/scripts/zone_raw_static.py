import os
from multiprocessing import Process

import openpyxl
import pandas
import pyspark

from pyspark.sql.functions import col
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StringType, StructType, IntegerType

data_dir = "../../Data"
# data_dir = "/mnt/group11/Data"

default_dir = data_dir + "/NYC_Trip_Data"
alternative_dir = data_dir + "/NYC_Trip_Data_Loc_To_Zone"

java8_location = '/Library/Java/JavaVirtualMachines/liberica-jdk-1.8.0_202/Contents/Home'  # Set your own
os.environ['JAVA_HOME'] = java8_location
spark = SparkSession.builder.master('local').appName('zone_statistic').getOrCreate()


def static_zone(in_year, in_month, in_day):
    index_field = [StructField("p_id", IntegerType(), True), StructField("p_hour", StringType(), True)]
    index_schema = StructType(index_field)
    index_df = spark.createDataFrame(index_list, schema=index_schema)

    field = [StructField("p_id", IntegerType(), True), StructField("p_hour", StringType(), True),
             StructField("count", IntegerType(), True)]
    schema = StructType(field)
    try:
        green_df = spark.read.parquet(
            default_dir + "/green_tripdata/result_" + in_year + "_" + in_month + ".parquet/p_date=" + in_year + "-" + in_month + "-" + in_day)
        green_df = green_df.groupBy('p_id', 'p_hour').count()
    except pyspark.sql.utils.AnalysisException:
        try:
            green_df = spark.read.parquet(
                alternative_dir + "/green_tripdata/result_" + in_year + "_" + in_month + ".parquet/p_date=" + in_year + "-" + in_month + "-" + in_day)
            green_df = green_df.select(col("LocationID").alias("p_id"), col("p_hour")).groupBy('p_id',
                                                                                               'p_hour').count()
        except pyspark.sql.utils.AnalysisException:
            green_df = spark.createDataFrame(spark.sparkContext.emptyRDD(), schema)
            print("System: Green taxi " + in_year + " " + in_month + " " + in_day + " 's data does not exist.")
    green_df = green_df.where(green_df.p_id.isNotNull()).select(col("p_id").alias("gp_id"),
                                                                col("p_hour").alias("gp_hour"),
                                                                col("count").alias("gcount"))
    try:
        yellow_df = spark.read.parquet(
            default_dir + "/yellow_tripdata/result_" + in_year + "_" + in_month + ".parquet/p_date=" + in_year + "-" + in_month + "-" + in_day)
        yellow_df = yellow_df.select(col("p_Id").alias("p_id"), col("p_hour")).groupBy('p_id',
                                                                                             'p_hour').count()
    except pyspark.sql.utils.AnalysisException:
        try:
            yellow_df = spark.read.parquet(
                alternative_dir + "/yellow_tripdata/result_" + in_year + "_" + in_month + ".parquet/p_date=" + in_year + "-" + in_month + "-" + in_day)
            yellow_df = yellow_df.select(col("LocationID").alias("p_id"), col("p_hour")).groupBy('p_id',
                                                                                                 'p_hour').count()
        except pyspark.sql.utils.AnalysisException:
            yellow_df = spark.createDataFrame(spark.sparkContext.emptyRDD(), schema)
            print("System: Yellow taxi " + in_year + " " + in_month + " " + in_day + " 's data does not exist.")
    yellow_df = yellow_df.where(yellow_df.p_id.isNotNull()).select(col("p_id").alias("yp_id"),
                                                                   col("p_hour").alias("yp_hour"),
                                                                   col("count").alias("ycount"))
    try:
        fhvhv_df = spark.read.parquet(
            default_dir + "/fhvhv/result_" + in_year + "_" + in_month + ".parquet/p_date=" + in_year + "-" + in_month + "-" + in_day)
        fhvhv_df = fhvhv_df.groupBy('p_id', 'p_hour').count()
    except pyspark.sql.utils.AnalysisException:
        fhvhv_df = spark.createDataFrame(spark.sparkContext.emptyRDD(), schema)
        print("System: FHVHV taxi " + in_year + " " + in_month + " " + in_day + " 's data does not exist.")
    fhvhv_df = fhvhv_df.where(fhvhv_df.p_id.isNotNull()).select(col("p_id").alias("hfp_id"),
                                                                col("p_hour").alias("hfp_hour"),
                                                                col("count").alias("hfcount"))
    try:
        fhv_df = spark.read.parquet(
            default_dir + "/fhv/fhv_tripdata_2017/result_" + in_year + "_" + in_month + ".parquet/p_date=" + in_year + "-" + in_month + "-" + in_day)
        fhv_df = fhv_df.groupBy('p_id', 'p_hour').count()
    except pyspark.sql.utils.AnalysisException:
        fhv_df = spark.createDataFrame(spark.sparkContext.emptyRDD(), schema)
        print("System: FHV taxi " + in_year + " " + in_month + " " + in_day + " 's data does not exist.")
    fhv_df = fhv_df.where(fhv_df.p_id.isNotNull()).select(col("p_id").alias("fp_id"),
                                                          col("p_hour").alias("fp_hour"),
                                                          col("count").alias("fcount"))
    index_df = index_df.join(yellow_df,
                             (index_df.p_hour == yellow_df.yp_hour) & (index_df.p_id == yellow_df.yp_id),
                             how='full')
    index_df = index_df.join(green_df,
                             (index_df.p_hour == green_df.gp_hour) & (index_df.p_id == green_df.gp_id),
                             how='full')
    index_df = index_df.join(fhvhv_df,
                             (index_df.p_hour == fhvhv_df.hfp_hour) & (index_df.p_id == fhvhv_df.hfp_id),
                             how='full')
    index_df = index_df.join(fhv_df, (index_df.p_hour == fhv_df.fp_hour) & (index_df.p_id == fhv_df.fp_id),
                             how='full')
    index_df = index_df.select(col("p_id"), col("p_hour"), col("ycount"), col("gcount"), col("hfcount"),
                               col("fcount")).where(index_df.p_id.isNotNull())
    # index_df.orderBy(["p_id"], ascending=True)
    index_df = index_df.na.fill(0)
    index_df = index_df.toPandas().sort_values(['p_id', 'p_hour'])
    index_df["sum"] = index_df["ycount"] + index_df["gcount"] + index_df["hfcount"] + index_df["fcount"]
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    target_path = save_dir + "/" + "hourly_" + year + "_" + month + "_" + day + ".csv"
    index_df.to_csv(target_path, index=False)

    hourly_df = index_df

    target_path = save_dir + "/" + "yellow_max_hour_" + year + "_" + month + "_" + day + ".csv"
    idx = hourly_df.groupby(['p_id'])['ycount'].transform(max) == hourly_df['ycount']
    y_df = hourly_df[idx][['p_id', 'p_hour', 'ycount']].drop_duplicates('p_id')
    y_df.to_csv(target_path, index=False)

    target_path = save_dir + "/" + "green_max_hour_" + year + "_" + month + "_" + day + ".csv"
    idx = hourly_df.groupby(['p_id'])['gcount'].transform(max) == hourly_df['gcount']
    g_df = hourly_df[idx][['p_id', 'p_hour', 'gcount']].drop_duplicates('p_id')
    g_df.to_csv(target_path, index=False)

    target_path = save_dir + "/" + "fhv_max_hour_" + year + "_" + month + "_" + day + ".csv"
    idx = hourly_df.groupby(['p_id'])['fcount'].transform(max) == hourly_df['fcount']
    f_df = hourly_df[idx][['p_id', 'p_hour', 'fcount']].drop_duplicates('p_id')
    f_df.to_csv(target_path, index=False)

    target_path = save_dir + "/" + "hvfhv_max_hour_" + year + "_" + month + "_" + day + ".csv"
    idx = hourly_df.groupby(['p_id'])['hfcount'].transform(max) == hourly_df['hfcount']
    hf_df = hourly_df[idx][['p_id', 'p_hour', 'hfcount']].drop_duplicates('p_id')
    hf_df.to_csv(target_path, index=False)

    target_path = save_dir + "/" + "all_max_hour_" + year + "_" + month + "_" + day + ".csv"
    idx = hourly_df.groupby(['p_id'])['sum'].transform(max) == hourly_df['sum']
    sum_df = hourly_df[idx][['p_id', 'p_hour', 'sum']].drop_duplicates('p_id')
    sum_df.to_csv(target_path, index=False)

    daily_df = index_df.groupby(['p_id'])['ycount', 'gcount', 'hfcount', "fcount", "sum"].sum().reset_index()
    target_path = save_dir + "/" + "daily_" + year + "_" + month + "_" + day + ".csv"
    daily_df.to_csv(target_path, index=False)


if __name__ == '__main__':
    save_dir = data_dir + "/NYC_Zone_Static"
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    index_list = []
    date_list = []
    for location_id in range(1, 264, 1):
        for hour in ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
            index_list.append([location_id, hour])
    for year in ["2018", "2019"]:
        for month in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
            for day in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
                        "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                        "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]:
                static_zone(year, month, day)
    #             date_list.append([year, month, day])
    # for i in range(0, len(date_list), 8):
    #     try:
    #         p1 = Process(target=static_zone, args=(date_list[i + 0][0], date_list[i + 0][1], date_list[i + 0][2]))
    #         p1.start()
    #     except Exception:
    #         pass
    #     try:
    #         p2 = Process(target=static_zone, args=(date_list[i + 1][0], date_list[i + 1][1], date_list[i + 1][2]))
    #         p2.start()
    #     except Exception:
    #         pass
    #     try:
    #         p3 = Process(target=static_zone, args=(date_list[i + 2][0], date_list[i + 2][1], date_list[i + 2][2]))
    #         p3.start()
    #     except Exception:
    #         pass
    #     try:
    #         p4 = Process(target=static_zone, args=(date_list[i + 3][0], date_list[i + 3][1], date_list[i + 3][2]))
    #         p4.start()
    #     except Exception:
    #         pass
    #     try:
    #         p5 = Process(target=static_zone, args=(date_list[i + 4][0], date_list[i + 4][1], date_list[i + 4][2]))
    #         p5.start()
    #     except Exception:
    #         pass
    #     try:
    #         p6 = Process(target=static_zone, args=(date_list[i + 5][0], date_list[i + 5][1], date_list[i + 5][2]))
    #         p6.start()
    #     except Exception:
    #         pass
    #     try:
    #         p7 = Process(target=static_zone, args=(date_list[i + 6][0], date_list[i + 6][1], date_list[i + 6][2]))
    #         p7.start()
    #     except Exception:
    #         pass
    #     try:
    #         p8 = Process(target=static_zone, args=(date_list[i + 7][0], date_list[i + 7][1], date_list[i + 7][2]))
    #         p8.start()
    #     except Exception:
    #         pass
    #     try:
    #         p1.join()
    #     except Exception:
    #         pass
    #     try:
    #         p2.join()
    #     except Exception:
    #         pass
    #     try:
    #         p3.join()
    #     except Exception:
    #         pass
    #     try:
    #         p4.join()
    #     except Exception:
    #         pass
    #     try:
    #         p5.join()
    #     except Exception:
    #         pass
    #     try:
    #         p6.join()
    #     except Exception:
    #         pass
    #     try:
    #         p7.join()
    #     except Exception:
    #         pass
    #     try:
    #         p8.join()
    #     except Exception:
    #         pass
