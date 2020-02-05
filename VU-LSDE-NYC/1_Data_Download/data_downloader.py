#----------------------------------------------------------------------------------------------------------------------
#       2019 LSDE GROUP 11 KAI ZHANG/YI ZHEN ZHAO/YU WANG
#       Last Update: 05-10-2019 10:54
#       Version: 1.1
#----------------------------------------------------------------------------------------------------------------------
#       # Description:
#         This Python script is target at grabbing all data from remote websites,
#----------------------------------------------------------------------------------------------------------------------
#       * Included:
#            * 2009 - 2019 Yellow Taxi's Trip Data
#            * 2013 - 2019 Green Taxi's Trip Data
#            * 2015 - 2019 FHV Taxi's Trip Data
#            * 2019 HFHV Taxi's Trip Data
#            * NYC Taxi Zone's Data
#            * NYC Map's Data
#----------------------------------------------------------------------------------------------------------------------
#       * Not Included:
#            * NYC 2009 - 2019's weather grabbed by python crawler
#            * NYC 2009 - 2019's financial grabbed by manual input
#            * NYC 2009 - 2019's population grabbed by manual input
#            * NYC 2009 - 2019's holiday grabbed by manual input
#----------------------------------------------------------------------------------------------------------------------
#       # Potential Problem:
#           * You may encounter `Exception： OSError: Could not find libspatialindex_c library file`,
#             you can use `sudo apt install libspatialindex-dev` to solve this problem.
#----------------------------------------------------------------------------------------------------------------------

import urllib.request
import shutil
import os
from zipfile import ZipFile
import osmnx as ox

# Local mode
data_dir = "../Data"
# Group 11 Databricks mode
# data_dir = "/dbfs/mnt/group11/Data"

clean_all_data = False
# Check if need to clean all data
if clean_all_data:
    shutil.rmtree(data_dir)
# Create root Data folder
if not os.path.exists(data_dir):
    os.mkdir(data_dir)
# Create [NYC Taxi Zones Folder] Data folder
if not os.path.exists(data_dir + "/NYC_Taxi_Zones"):
    os.mkdir(data_dir + "/NYC_Taxi_Zones")
# Create [NYC Map Folder] Data folder
if not os.path.exists(data_dir + "/NYC_Route_Map"):
    os.mkdir(data_dir + "/NYC_Route_Map")
# Create [NYC Trip Data folder] (Store all taxi trip data)
if not os.path.exists(data_dir + "/NYC_Trip_Data"):
    os.mkdir(data_dir + "/NYC_Trip_Data")
# Create [NYC Trip Data folder - Yellow Trip Data folder]
if not os.path.exists(data_dir + "/NYC_Trip_Data/yellow_tripdata"):
    os.mkdir(data_dir + "/NYC_Trip_Data/yellow_tripdata")
# Create [NYC Trip Data folder - Green Trip Data folder]
if not os.path.exists(data_dir + "/NYC_Trip_Data/green_tripdata"):
    os.mkdir(data_dir + "/NYC_Trip_Data/green_tripdata")
# Create [NYC Trip Data folder - FHV Trip Data folder]
if not os.path.exists(data_dir + "/NYC_Trip_Data/fhv"):
    os.mkdir(data_dir + "/NYC_Trip_Data/fhv")
# Create [NYC Trip Data folder - FHVHV Trip Data folder]
if not os.path.exists(data_dir + "/NYC_Trip_Data/fhvhv"):
    os.mkdir(data_dir + "/NYC_Trip_Data/fhvhv")
# Create [NYC Trip Data folder - FHVHV Trip Data folder]
if not os.path.exists(data_dir + "/NYC_Trip_Data/fhv/fhv_tripdata_2015"):
    os.mkdir(data_dir + "/NYC_Trip_Data/fhv/fhv_tripdata_2015")
if not os.path.exists(data_dir + "/NYC_Trip_Data/fhv/fhv_tripdata_2017"):
    os.mkdir(data_dir + "/NYC_Trip_Data/fhv/fhv_tripdata_2017")


def get_yellow_taxi():
    dest = data_dir + "/NYC_Trip_Data/yellow_tripdata/yellow_tripdata_"
    reso = "https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_"
    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    for year in range(2017, 2020):
        for month in months:
            file_extension = str(year) + "-" + str(month) + ".csv"
            try:
                resource_file = reso + file_extension
                dest_file = dest + file_extension
                urllib.request.urlretrieve(reso + file_extension, dest + file_extension)
                print("System : " + str(year) + " " + month + "'s yellow trip data downloaded")
            except urllib.error.HTTPError:
                print("HTTP  Exception : " + str(year) + " " + month + "'s yellow trip data is not downloaded")
            except urllib.error.URLError:
                print("URL   Exception : " + str(year) + " " + month + "'s yellow trip data is not downloaded")


def get_green_taxi():
    dest = data_dir + "/NYC_Trip_Data/green_tripdata/green_tripdata_"
    reso = "https://s3.amazonaws.com/nyc-tlc/trip+data/green_tripdata_"
    monthes = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    for year in range(2013, 2020):
        for month in monthes:
            file_extension = str(year) + "-" + str(month) + ".csv"
            try:
                urllib.request.urlretrieve(reso + file_extension, dest + file_extension)
                print("System : " + str(year) + " " + month + "'s green trip data downloaded")
            except urllib.error.HTTPError:
                print("Exception : " + str(year) + " " + month + "'s green trip data is not downloaded")


def get_fhv_taxi_before_2017():
    dest = data_dir + "/NYC_Trip_Data/fhv/fhv_tripdata_2015/fhv_tripdata_"
    reso = "https://s3.amazonaws.com/nyc-tlc/trip+data/fhv_tripdata_"
    monthes = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    for year in range(2015, 2017):
        for month in monthes:
            file_extension = str(year) + "-" + str(month) + ".csv"
            try:
                urllib.request.urlretrieve(reso + file_extension, dest + file_extension)
                print("System : " + str(year) + " " + month + "'s fhv before 2017 trip data downloaded")
            except urllib.error.HTTPError:
                print("Exception : " + str(year) + " " + month + "'s fhv before 2017 trip data is not downloaded")


def get_fhv_taxi_after_2017():
    dest = data_dir + "/NYC_Trip_Data/fhv/fhv_tripdata_2017/fhv_tripdata_"
    reso = "https://s3.amazonaws.com/nyc-tlc/trip+data/fhv_tripdata_"
    monthes = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    for year in range(2017, 2020):
        for month in monthes:
            file_extension = str(year) + "-" + str(month) + ".csv"
            try:
                urllib.request.urlretrieve(reso + file_extension, dest + file_extension)
                print("System : " + str(year) + " " + month + "'s fhv after 2017 trip data downloaded")
            except urllib.error.HTTPError:
                print("Exception : " + str(year) + " " + month + "'s fhv after 2017 trip data is not downloaded")


def get_hfhv_taxi():
    dest = data_dir + "/NYC_Trip_Data/fhvhv/fhvhv_tripdata_"
    reso = "https://s3.amazonaws.com/nyc-tlc/trip+data/fhvhv_tripdata_"
    monthes = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    for year in range(2019, 2020):
        for month in monthes:
            file_extension = str(year) + "-" + str(month) + ".csv"
            try:
                urllib.request.urlretrieve(reso + file_extension, dest + file_extension)
                print("System : " + str(year) + " " + month + "'s hvfhv trip data downloaded")
            except urllib.error.HTTPError:
                print("Exception : " + str(year) + " " + month + "'s hvfhv trip data is not downloaded")


def get_taxi_zone():
    dest = data_dir + "/NYC_Taxi_Zones/"
    reso = "http://172.105.84.249/taxi_zones.zip"
    try:
        urllib.request.urlretrieve(reso, dest + "zones.zip")
        zf = ZipFile(dest + "zones.zip", 'r')
        zf.extractall(dest)
        zf.close()
        os.remove(dest + "zones.zip")
        print("System  : Taxi data zone's data is downloaded")
    except urllib.error.HTTPError:
        print("Exception : Taxi data zone's data is not downloaded")


def get_nyc_map():
    try:
        nyc_map = ox.graph_from_place('New York City, New York, USA', network_type='drive')
        ox.save_graphml(nyc_map, "../" + data_dir + "/NYC_Route_Map/NYC.mph")
        print("System : NYC Map's data is downloaded")
    except Exception:
        print("Exception : NYC Map's data is not downloaded")


# get_yellow_taxi()
# get_green_taxi()
# get_fhv_taxi_before_2017()
# get_fhv_taxi_after_2017()
# get_hfhv_taxi()
# get_taxi_zone()
# get_nyc_map()
