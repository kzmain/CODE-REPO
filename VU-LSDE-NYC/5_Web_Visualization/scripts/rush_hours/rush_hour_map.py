import random
import bokeh
import geopandas
from bokeh.io import show
from bokeh.models import LogColorMapper
from bokeh.plotting import figure
import pandas

# Local mode
data_dir = "../../../Data"
## Group 11 databricks mode
# data_dir = "/dbfs/mnt/group11/Data"


statistic_file_dir = data_dir + "/NYC_Zone_Static/statistic_rush_hour"
statistic_csv_path = statistic_file_dir + "/rush_hour_by_p_id.csv"

shape_map_path = data_dir + "/NYC_Taxi_Zones/taxi_zones.shp"
soa_shape_map = geopandas.read_file(shape_map_path)
soa_shape_map_geo = soa_shape_map.to_crs(epsg=4326)

year_df = pandas.read_csv(statistic_csv_path)
# year_df = year_df[year_df.count > 10]
idx = year_df['count'] > 150
year_df = year_df[idx][['p_id', 'p_hour', 'count']][['p_id', 'p_hour', 'count']]
year_df = year_df.sort_values(by=['p_id']).reset_index()
zone_xs = []
zone_ys = []
zone_names = []
rush_hours = []
count = 0
for index, row in soa_shape_map_geo.iterrows():
    xs = []
    ys = []
    print(row["geometry"])
    corrs = str(row["geometry"]) \
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
    zone_names.append(row['zone'])
    hour = list(year_df.loc[year_df['p_id'] == count + 1]["p_hour"])
    if len(hour) > 0:
        rush_hours.append(hour[0])
    else:
        rush_hours.append("Does not have rush hour")
    count += 1

color_mapper = LogColorMapper(palette=bokeh.palettes.viridis(24))

data = dict(
    x=zone_xs,
    y=zone_ys,
    name=zone_names,
    rush_hour=rush_hours,
)

TOOLS = "pan,wheel_zoom,reset,hover,save"

p = figure(
    title="Rush hour statistic of NYC", tools=TOOLS,
    x_axis_location=None, y_axis_location=None,
    tooltips=[
        ("Name", "@name"), ("Rush Hour", "@rush_hour"), ("(Long, Lat)", "($x, $y)")
    ])
p.grid.grid_line_color = None
p.hover.point_policy = "follow_mouse"

p.patches('x', 'y', source=data,
          fill_color={'field': 'rush_hour', 'transform': color_mapper},
          fill_alpha=1, line_color="white", line_width=1)
p.sizing_mode = 'scale_width'
show(p)
