import os
import random
import bokeh
import geopandas
from bokeh.io import show
from bokeh.models import LogColorMapper
from bokeh.plotting import figure
import pandas
from bokeh.plotting import figure, output_file, save
from random import randrange

print()

# Local mode
data_dir = "../../../Data"
zone_statistic_dir = data_dir + "/NYC_Zone_Static"
holiday_statistic_dir = zone_statistic_dir + "/holiday"
# Group 11 Databricks mode
# data_dir = "/dbfs/mnt/group11/Data"

shape_map_path = data_dir + "/NYC_Taxi_Zones/taxi_zones.shp"
soa_shape_map = geopandas.read_file(shape_map_path)
soa_shape_map_geo = soa_shape_map.to_crs(epsg=4326)

holiday_name_df = pandas.read_csv(data_dir + "/NYC_Holiday/holiday_id_name.csv")
for index, row in holiday_name_df.iterrows():
    holiday_name = row["holiday_name"].lower().replace(" ", "_").replace("'", "")
    print("System: processing " + holiday_name)
    csv_file = holiday_statistic_dir + "/" + holiday_name + ".csv"
    holiday_df = pandas.read_csv(csv_file)
    holiday_df = holiday_df[holiday_df["sum"] > 50][["p_id", "sum", "percentage"]].reset_index()
    # idx = holiday_df['sum'] > 50
    # holiday_df = holiday_df[idx][['p_id', 'sum','percentage']][['p_id', 'sum', 'percentage']]
    holiday_df["map_value"] = (((holiday_df["percentage"] - holiday_df["percentage"].min()) /(holiday_df["percentage"].max() - holiday_df["percentage"].min())) + 1) * 100

    zone_xs = []
    zone_ys = []
    zone_names = []
    value_list = []
    percentage_list = []
    count = 0
    for map_index, map_row in soa_shape_map_geo.iterrows():
        xs = []
        ys = []
        corrs = str(map_row["geometry"]) \
            .replace("MULTIPOLYGON (", "") \
            .replace("POLYGON (", "") \
            .replace("(", "") \
            .replace(")", "") \
            .split()
        for i in range(0, len(corrs), 2):
            xs.append(float(corrs[i]))
            ys.append(float(corrs[i + 1].replace(",", "")))
        zone_xs.append(xs)
        zone_ys.append(ys)
        zone_names.append(map_row['zone'])

        value = list(holiday_df.loc[holiday_df['p_id'] == count + 1]["map_value"])
        perc = list(holiday_df.loc[holiday_df['p_id'] == count + 1]["percentage"])
        if len(value) > 0:
            # if (abs(value[0]) > 400):
            #     value_list.append(400)
            # else:
            #     value_list.append(value[0])
            value_list.append(value[0])
            percentage_list.append(perc[0] * 100)
        else:
            value_list.append("Does not have rush hour")
            percentage_list.append("Does not have rush hour")
        count += 1

    color_mapper = LogColorMapper(palette=bokeh.palettes.viridis(256))

    data = dict(
        x=zone_xs,
        y=zone_ys,
        name=zone_names,
        value_list=value_list,
        percentage=percentage_list,
    )

    TOOLS = "pan,wheel_zoom,reset,hover,save"

    p = figure(
        title="%s of NYC" % row["holiday_name"], tools=TOOLS,
        x_axis_location=None, y_axis_location=None,
        sizing_mode='scale_width',
        tooltips=[
            ("Name", "@name"), ("Increase/Decrease Percentage", "@percentage%"), ("(Long, Lat)", "($x, $y)")
        ])
    p.grid.grid_line_color = None
    p.hover.point_policy = "follow_mouse"

    p.patches('x', 'y', source=data,
              fill_color={'field': 'value_list', 'transform': color_mapper},
              fill_alpha=1, line_color="white", line_width=1)
    www_dir = "../../www"
    html_dir = www_dir + "/html"
    holiday_dir = html_dir + "/holiday"
    if not os.path.exists(www_dir):
        os.mkdir(www_dir)
    if not os.path.exists(html_dir):
        os.mkdir(html_dir)
    if not os.path.exists(holiday_dir):
        os.mkdir(holiday_dir)
    output_file(holiday_dir + "/" + holiday_name + '.html', mode='inline')

    save(p)
