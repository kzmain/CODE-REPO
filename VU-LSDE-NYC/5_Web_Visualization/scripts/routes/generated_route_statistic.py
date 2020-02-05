import os
from pathlib import Path
import pandas
import openpyxl


from colour import Color


def get_color(row):
    shang = int(row['count'] / 10)
    yushu = row['count'] % 10
    if yushu < 0:
        shang -= 1
    return colors[shang].get_hex()


def get_weight(row):
    weight = row['count'] / max_value * 10
    if weight > 2:
        weight = 2
    return weight


data_dir = '../../../Data'
# data_dir = '/dbfs/mnt/group11/Data'  # ZK的数据存放体系结构中
map_path = data_dir + '/NYC_Route_Map'
router_planner_path = data_dir + '/NYC_Route_Planner_Result'
node_path = router_planner_path + "/nodes.csv"
nodes_df = pandas.read_csv(node_path, index_col=None).rename(columns={"osmid": 'p_id'})
print(len(nodes_df))
# csv_file_list = []
max_value = 0
for root, dirs, files in os.walk(router_planner_path, topdown=False):
    for name in files:
        file_name = os.path.join(root, name)
        if Path(file_name).suffix == '.csv':
            if "nodes" in file_name or "statistic_" in file_name:
                continue

            csv_path = Path(file_name)
            csv_folder = csv_path.parent
            # csv_file_list.append(file_name)
            print("System: Pre-processing " + file_name)
            routes_df = pandas.read_csv(csv_path, header=None, index_col=None)
            routes_df = routes_df.groupby([0, 1]).size()
            routes_df.to_csv(str(csv_folder) + "/statistic_" + name)
            static_df = pandas.read_csv(str(csv_folder) + "/statistic_" + name, header=None, index_col=None)
            static_df = static_df.rename(columns={0: 'p1_id', 1: 'p2_id', 2: 'count'})
            result_df = static_df.merge(nodes_df, left_on='p1_id', right_on='p_id').rename(
                columns={"x": 'p1_x', "y": 'p1_y'})
            result_df = result_df.merge(nodes_df, left_on='p2_id', right_on='p_id').rename(
                columns={"x": 'p2_x', "y": 'p2_y'})
            result_df = result_df[["p1_x", "p1_y", "p2_x", "p2_y", "count"]]
            # Generate gradient color
            result_df = result_df.sort_values(by=['count'], ascending=False)
            df_max = result_df['count'].iloc[0]
            if df_max >= max_value:
                max_value = result_df['count'].iloc[0]
for root, dirs, files in os.walk(router_planner_path, topdown=False):
    for name in files:
        file_name = os.path.join(root, name)
        if Path(file_name).suffix == '.csv':
            if "nodes" in file_name or "statistic_" in file_name:
                continue

            csv_path = Path(file_name)
            csv_folder = csv_path.parent
            print("System: Processing " + file_name)
            routes_df = pandas.read_csv(csv_path, header=None, index_col=None)
            routes_df = routes_df.groupby([0, 1]).size()
            routes_df.to_csv(str(csv_folder) + "/statistic_" + name)
            static_df = pandas.read_csv(str(csv_folder) + "/statistic_" + name, header=None, index_col=None)
            static_df = static_df.rename(columns={0: 'p1_id', 1: 'p2_id', 2: 'count'})
            result_df = static_df.merge(nodes_df, left_on='p1_id', right_on='p_id').rename(
                columns={"x": 'p1_x', "y": 'p1_y'})
            result_df = result_df.merge(nodes_df, left_on='p2_id', right_on='p_id').rename(
                columns={"x": 'p2_x', "y": 'p2_y'})
            result_df = result_df[["p1_x", "p1_y", "p2_x", "p2_y", "count"]]
            # Generate gradient color
            result_df = result_df.sort_values(by=['count'], ascending=False)
            color_count = int(max_value / 10) + 1
            colors = list(Color("blue").range_to(Color("Red"), color_count))
            result_df['color'] = result_df.apply(get_color, axis=1)
            result_df['weight'] = result_df.apply(get_weight, axis=1)
            result_df.to_csv(str(csv_folder) + "/statistic_" + name, index=False)
