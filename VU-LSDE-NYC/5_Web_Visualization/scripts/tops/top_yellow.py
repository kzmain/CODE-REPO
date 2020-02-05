import random
import bokeh
import geopandas
from bokeh.io import show
from bokeh.models import LogColorMapper
from bokeh.plotting import figure
import pandas

# palette.reverse()

data_dir = "../../../Data"
# data_dir = "/dbfs/mnt/group11/Data"
shape_map_path = data_dir + "/NYC_Taxi_Zones/taxi_zones.shp"
soa_shape_map = geopandas.read_file(shape_map_path)
soa_shape_map_geo = soa_shape_map.to_crs(epsg=4326)

year_statistic = "2018"
year_df = pandas.read_csv(data_dir + "/NYC_Zone_Static/" + year_statistic + "_zone_statistic.csv")

county_xs = []
county_ys = []
county_names = []
county_rates = []
count = 0
top_10 = list(year_df.nlargest(20, ['ycount'])['ycount'])
for index, row in soa_shape_map_geo.iterrows():
    xs = []
    ys = []
    corrs = str(row["geometry"])\
        .replace("MULTIPOLYGON (", "")\
        .replace("POLYGON (", "")\
        .replace("(", "")\
        .replace(")", "")\
        .split()
    for i in range(0, len(corrs), 2):
        xs.append(float(corrs[i]))
        ys.append(float(corrs[i + 1].replace(",", "")))
    county_xs.append(xs)
    county_ys.append(ys)
    county_names.append(row['zone'])
    if year_df.iloc[count]['ycount'] in top_10:
        county_rates.append(year_df.iloc[count]['ycount'])
    else:
        county_rates.append("Not Top Area")
    count += 1

color_mapper = LogColorMapper(palette=bokeh.palettes.viridis(4))

data = dict(
    x=county_xs,
    y=county_ys,
    name=county_names,
    rate=county_rates,
)

TOOLS = "pan,wheel_zoom,reset,hover,save"

p = figure(
    title="TOP 10 YELLOW TAXI ZONES", tools=TOOLS,
    x_axis_location=None, y_axis_location=None,
    tooltips=[
        ("Name", "@name"), ("Usage", "@rate"), ("(Long, Lat)", "($x, $y)")
    ])
p.grid.grid_line_color = None
p.hover.point_policy = "follow_mouse"

p.patches('x', 'y', source=data,
          fill_color={'field': 'rate', 'transform': color_mapper},
          fill_alpha=1, line_color="white", line_width=1)
p.sizing_mode = 'scale_width'
show(p)
