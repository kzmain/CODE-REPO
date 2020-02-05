import os
import time
from multiprocessing import Process
from pathlib import Path
import geopandas as gpd
import pandas
import pyarrow

data_dir = "../Data"
# data_dir = "/dbfs/mnt/group11/Data"
trip_data_dest_loc = data_dir + "/NYC_Trip_Data_Loc_To_Zone/"
shape_map_path = data_dir + "/NYC_Taxi_Zones/taxi_zones.shp"
yellow_trip_data_dir = data_dir + "/NYC_Trip_Data/yellow_tripdata/"
# ----------------------------------------------------Read Shapefile----------------------------------------------------
soa_shape_map = gpd.read_file(shape_map_path)
soa_shape_map_geo = soa_shape_map.to_crs(epsg=4326)


def process_yellow(in_year, in_month, in_day):
    s_time = time.time()
    date_parquet_dir = "result_" + in_year + "_" + in_month + ".parquet" + "/p_date=" + in_year + "-" + in_month + "-" + in_day
    raw_file_path = yellow_trip_data_dir + date_parquet_dir
    # Get all separate parquet files location
    parquet_file_list = []
    for root, dirs, files in os.walk(raw_file_path, topdown=False):
        for name in files:
            file_name = os.path.join(root, name)
            if Path(file_name).suffix == '.parquet':
                parquet_file_list.append(file_name)
    try:
        # Read in all separate parquet files
        full_df = pandas.concat(
            pandas.read_parquet(parquet_file)
            for parquet_file in parquet_file_list
        )
        print("System: " + in_year + " " + in_month + " " + in_day + "'s data start processing.")
        print(full_df.count())
        # Change pandas data frame to geo_pandas data frame
        geo_data_frame = gpd.GeoDataFrame(full_df, geometry=gpd.points_from_xy(full_df.p_lon, full_df.p_lat))
        # Get zone location
        geo_data_frame = gpd.sjoin(geo_data_frame, soa_shape_map_geo, how="inner", op="intersects")
        # Change geo_pandas data frame to pandas data frame
        result = pandas.DataFrame(geo_data_frame.drop(columns='geometry'))
        # Write out parquet
        # Set parquet file location
        tripdata_dest_loc = data_dir + "/NYC_Trip_Data_Loc_To_Zone/"
        if not os.path.exists(tripdata_dest_loc):
            os.mkdir(tripdata_dest_loc)
        yellow_trip_data_dest_loc = data_dir + "/NYC_Trip_Data_Loc_To_Zone/yellow_tripdata/"
        if not os.path.exists(yellow_trip_data_dest_loc):
            os.mkdir(yellow_trip_data_dest_loc)
        yellow_trip_parquet_dir_name = "result_" + in_year + "_" + in_month + ".parquet"
        yellow_trip_parquet_dir_name = yellow_trip_data_dest_loc + yellow_trip_parquet_dir_name
        if not os.path.exists(yellow_trip_parquet_dir_name):
            os.mkdir(yellow_trip_parquet_dir_name)
        yellow_trip_date_dir = "/p_date=" + in_year + "-" + in_month + "-" + in_day
        yellow_trip_date_dir = yellow_trip_parquet_dir_name + yellow_trip_date_dir
        if not os.path.exists(yellow_trip_date_dir):
            os.mkdir(yellow_trip_date_dir)
        result.to_parquet(yellow_trip_date_dir + "/p_date=" + in_year + "-" + in_month + "-" + in_day + ".parquet")
        # Save log
        e_time = time.time()
        y_time_log = open(trip_data_dest_loc + "yellow_time_log.txt", "a+")
        y_time_log.writelines("System: " + str(in_year) + " " + str(in_month) + " " + str(in_day) + " " +
                              "'s location to zone's total time: " + str((e_time - s_time) / 60) + " min." +
                              " Trip Size: " + str(len(result.index)) + "\n")
        y_time_log.close()
        print("A day's location to zone's total time: " + str((e_time - s_time) / 60) + " min.")
    except ValueError as e:
        y_error_log = open(trip_data_dest_loc + "yellow_error_log.txt", "a+")
        y_error_log.writelines(
            "Exception: VE " + in_year + " " + in_month + " " + in_day + "'s data not processed." + "\n")
        y_error_log.close()
        print("Exception: VE " + in_year + " " + in_month + " " + in_day + "'s data not processed.")
        exit(1)
    except pyarrow.lib.ArrowIOError as ex:
        y_error_log = open(trip_data_dest_loc + "yellow_error_log.txt", "a+")
        y_error_log.writelines(
            "Exception: AE " + in_year + " " + in_month + " " + in_day + "'s data not processed." + "\n")
        y_error_log.close()
        print("Exception: VE " + in_year + " " + in_month + " " + in_day + "'s data not processed.")
        exit(1)


# set the processes max number as 8 on local machine/ 60 on databricks
date_list = []
for year in range(2009, 2017):
    for month in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
        for day in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
                    "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                    "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
                    "31"]:
            year = str(year)
            date_list.append([year, month, day])

if __name__ == '__main__':
    if not os.path.exists(trip_data_dest_loc):
        os.mkdir(trip_data_dest_loc)
    error_log = open(trip_data_dest_loc + "yellow_error_log.txt", "w+")
    time_log = open(trip_data_dest_loc + "yellow_time_log.txt", "w+")
    error_log.close()
    time_log.close()
    for i in range(0, len(date_list), 8):
        try:
            p1 = Process(target=process_yellow, args=(date_list[i][0], date_list[i][1], date_list[i][2],))
            p2 = Process(target=process_yellow, args=(date_list[i + 1][0], date_list[i + 1][1], date_list[i + 1][2],))
            p3 = Process(target=process_yellow, args=(date_list[i + 2][0], date_list[i + 2][1], date_list[i + 2][2],))
            p4 = Process(target=process_yellow, args=(date_list[i + 3][0], date_list[i + 3][1], date_list[i + 3][2],))
            p5 = Process(target=process_yellow, args=(date_list[i + 4][0], date_list[i + 4][1], date_list[i + 4][2],))
            p6 = Process(target=process_yellow, args=(date_list[i + 5][0], date_list[i + 5][1], date_list[i + 5][2],))
            p7 = Process(target=process_yellow, args=(date_list[i + 6][0], date_list[i + 6][1], date_list[i + 6][2],))
            p8 = Process(target=process_yellow, args=(date_list[i + 7][0], date_list[i + 7][1], date_list[i + 7][2],))
            p1.start()
            p2.start()
            p3.start()
            p4.start()
            p5.start()
            p6.start()
            p7.start()
            p8.start()
            p1.join()
            p2.join()
            p3.join()
            p4.join()
            p5.join()
            p6.join()
            p7.join()
            p8.join()
        except IndexError:
            print("list index out of range")
