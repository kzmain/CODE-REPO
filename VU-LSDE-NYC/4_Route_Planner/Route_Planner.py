import os
import shutil
import time
from multiprocessing import Process
from multiprocessing.pool import Pool
from pathlib import Path

import geopandas as gpd
import networkx as nx
import osmnx as ox
import pandas
import pyarrow

# data_dir = '/dbfs/mnt/group11/Data'  # ZK的数据存放体系结构中
data_dir = '../Data'
map_path = data_dir + '/NYC_Route_Map'
router_planner_path = data_dir + '/NYC_Route_Planner_Result'

if os.path.exists(router_planner_path):
    shutil.rmtree(router_planner_path)
os.mkdir(router_planner_path)
# 加载NYC地图
try:
    nyc_map = ox.load_graphml("NYC.mph", folder=map_path)
    gdf_nodes, gdf_edges = ox.graph_to_gdfs(nyc_map, nodes=True, edges=True)
    nodes_df = pandas.DataFrame(gdf_nodes)[['osmid', 'x', 'y']]
    nodes_df.to_csv(router_planner_path + "/nodes.csv", index=False)
    print('System: New York Map loaded.')
except FileNotFoundError as e:
    print('Exception: New York Map cannot be loaded.')
    exit(1)

print()


def make_route(row, outer_file_name):
    s_yx = (row["p_lat"], row["p_lon"])
    e_yx = (row["d_lat"], row["d_lon"])
    route = []

    try:
        # Find the closest origin and target nodes from the graph (the ids of them)
        s_node = ox.get_nearest_node(nyc_map, s_yx, method='euclidean')
        e_node = ox.get_nearest_node(nyc_map, e_yx, method='euclidean')
        if s_node == e_node:
            # Todo Exception 写出
            print('Start point is same as end point, no route in trip ', row["id"])
            return route
        else:
            # Get nodes in geodataframe, indexed in osmid
            s_close = gdf_nodes.loc[s_node]
            e_close = gdf_nodes.loc[e_node]
            # Create a GeoDataFrame from the origin and target points
            # find graph nodes nearest to some set of points
            od_nodes = gpd.GeoDataFrame([s_close, e_close], geometry='geometry', crs=gdf_nodes.crs)
            od_nodes.head()
            # Calculate the shortest path
            # if not nx.has_path(nyc_map, source=s_node, target=e_node):
            #     # Todo Exception 写出
            #     print("No Path in trip ", row["id"])
            #     return route
            # else:
            try:
                route = nx.shortest_path(G=nyc_map, source=s_node, target=e_node, weight='length')
                for index in range(1, len(route), 1):
                    bigger = route[index - 1] if route[index - 1] >= route[index] else route[index]
                    smaller = route[index - 1] if route[index - 1] < route[index] else route[index]
                    out_csv = open(outer_file_name, "a+")
                    out_csv.writelines(str(smaller) + "," + str(bigger) + "\n")
                    out_csv.close()
                return []
            except nx.exception.NetworkXNoPath:
                # Todo Exception 写出
                return []
    except nx.exception as ex:
        print(ex)
        print('Error in trip_id ', row["id"] + '\n')
        return []


def process_route(hour_dataframe, outer_file_name, in_specific_hour):
    print("System: Start processing " + taxi_type + " " + in_specific_hour + "'s taxi data. (" + str(
        len(hour_dataframe)) + ") rows.")
    s_time = time.time()
    hour_dataframe.apply(make_route, args=(outer_file_name,), axis=1)
    e_time = time.time()
    print("System: " + taxi_type + " " + in_specific_hour + " " + str(len(hour_dataframe)) + " need " + str(
        (e_time - s_time) / 60) + " mins.")
    y_time_log = open(router_planner_path + "/" + taxi_type + "_route_time_log.txt", "a+")
    y_time_log.writelines(
        "System: " + taxi_type + " " + in_specific_hour + " has " + str(
            len(hour_dataframe)) + " rows of data and took " + str(
            (e_time - s_time) / 60) + " mins.\n")
    y_time_log.close()


def pre_process_day_data(in_year, in_month, in_day, in_type):
    date_parquet_dir = "result_" + in_year + "_" + in_month + ".parquet" + "/p_date=" + in_year + "-" + in_month + "-" + in_day
    raw_file_path = data_dir + "/NYC_Trip_Data/" + in_type + "_tripdata/" + date_parquet_dir
    # Get all separate parquet files location
    parquet_file_list = []
    for root, dirs, files in os.walk(raw_file_path, topdown=False):
        for name in files:
            file_name = os.path.join(root, name)
            if Path(file_name).suffix == '.parquet':
                parquet_file_list.append(file_name)
    try:
        # Read in all separate parquet files
        day_group = pandas.concat(
            pandas.read_parquet(path=parquet_file)
            for parquet_file in parquet_file_list
        ).groupby("p_hour")
        return day_group
    except ValueError as ve:
        y_error_log = open(router_planner_path + "/" + in_type + "_route_error_log.txt", "a+")
        y_error_log.writelines(
            "Exception: VE " + taxi_type + " " + in_year + " " + in_month + " " + in_day + "'s data not processed." + "\n")
        y_error_log.close()
        print("Exception: VE " + taxi_type + " " + in_year + " " + in_month + " " + in_day + "'s data not processed.")
        return None
    except pyarrow.lib.ArrowIOError as ae:
        y_error_log = open(router_planner_path + "/" + in_type + "_route_error_log.txt", "a+")
        y_error_log.writelines(
            "Exception: AE " + taxi_type + " " + in_year + " " + in_month + " " + in_day + "'s data not processed." + "\n")
        y_error_log.close()
        print("Exception: AE " + taxi_type + " " + in_year + " " + in_month + " " + in_day + "'s data not processed.")
        return None


if __name__ == '__main__':
    start = time.time()
    taxi_types = ["green", "yellow"]
    #            Light snow          /Fog                  /Clear                /Snow                 /Heavy rain
    date_list = [["2015", "01", "27"], ["2015", "01", "12"], ["2015", "01", "07"], ["2014", "02", "03"], ["2014", "04", "30"]]
    for taxi_type in taxi_types:
        error_log = open(router_planner_path + "/" + taxi_type + "_route_error_log.txt", "w+")
        error_log.close()
        time_log = open(router_planner_path + "/" + taxi_type + "_route_time_log.txt", "w+")
        time_log.close()
        for i in range(0, len(date_list), 1):
            day_data_group = pre_process_day_data(date_list[i][0], date_list[i][1], date_list[i][2], taxi_type)
            if day_data_group is not None:
                if not os.path.exists(router_planner_path):
                    os.mkdir(router_planner_path)
                # print("System: Start loading data")
                specific_date = str(date_list[i][0]) + "_" + str(date_list[i][1]) + "_" + str(date_list[i][2])
                router_planner_date_path = router_planner_path + "/" + specific_date + "_" + taxi_type
                if not os.path.exists(router_planner_date_path):
                    os.mkdir(router_planner_date_path)
                out_file_name = router_planner_date_path + "/" + specific_date
                with Pool(processes=12) as pool:
                    for hour in range(0, 24, 1):
                        specific_hour = specific_date + "_" + "h" + str(hour)
                        pool.apply_async(process_route, (day_data_group.get_group(str(hour).zfill(2)),
                                                                 out_file_name + "_" + "h" + str(hour) + ".csv",
                                                                 specific_hour))  # runs in *only* one process
                    pool.close()
                    pool.join()

                # for hour in range(0, 24, 8):
                        # specific_hour = specific_date + "_" + "h" + str(hour + 0)
                        # p1 = Process(target=process_route, args=(day_data_group.get_group(str(hour + 0).zfill(2)),
                        #                                          out_file_name + "_" + "h" + str(hour + 0) + ".csv",
                        #                                          specific_hour))
                        # specific_hour = specific_date + "_" + "h" + str(hour + 1)
                        # p2 = Process(target=process_route, args=(day_data_group.get_group(str(hour + 1).zfill(2)),
                        #                                          out_file_name + "_" + "h" + str(hour + 1) + ".csv",
                        #                                          specific_hour))
                        #
                        #
                        # specific_hour = specific_date + "_" + "h" + str(hour + 2)
                        # p3 = Process(target=process_route, args=(day_data_group.get_group(str(hour + 2).zfill(2)),
                        #                                          out_file_name + "_" + "h" + str(hour + 2) + ".csv",
                        #                                          specific_hour))
                        #
                        # specific_hour = specific_date + "_" + "h" + str(hour + 3)
                        # p4 = Process(target=process_route, args=(day_data_group.get_group(str(hour + 3).zfill(2)),
                        #                                          out_file_name + "_" + "h" + str(hour + 3) + ".csv",
                        #                                          specific_hour))
                        #
                        # specific_hour = specific_date + "_" + "h" + str(hour + 4)
                        # p5 = Process(target=process_route, args=(day_data_group.get_group(str(hour + 4).zfill(2)),
                        #                                          out_file_name + "_" + "h" + str(hour + 4) + ".csv",
                        #                                          specific_hour))
                        #
                        # specific_hour = specific_date + "_" + "h" + str(hour + 5)
                        # p6 = Process(target=process_route, args=(day_data_group.get_group(str(hour + 5).zfill(2)),
                        #                                          out_file_name + "_" + "h" + str(hour + 5) + ".csv",
                        #                                          specific_hour))
                        #
                        # specific_hour = specific_date + "_" + "h" + str(hour + 6)
                        # p7 = Process(target=process_route, args=(day_data_group.get_group(str(hour + 6).zfill(2)),
                        #                                          out_file_name + "_" + "h" + str(hour + 6) + ".csv",
                        #                                          specific_hour))
                        #
                        # specific_hour = specific_date + "_" + "h" + str(hour + 7)
                        # p8 = Process(target=process_route, args=(day_data_group.get_group(str(hour + 7).zfill(2)),
                        #                                          out_file_name + "_" + "h" + str(hour + 7) + ".csv",
                        #                                          specific_hour))
                        # p1.start()
                        # p2.start()
                        # p3.start()
                        # p4.start()
                        # p5.start()
                        # p6.start()
                        # p7.start()
                        # p8.start()
                        #
                        # p1.join()
                        #
                        # p2.join()
                        #
                        # p3.join()
                        #
                        # p4.join()
                        #
                        # p5.join()
                        #
                        # p6.join()
                        #
                        # p7.join()
                        #
                        # p8.join()

