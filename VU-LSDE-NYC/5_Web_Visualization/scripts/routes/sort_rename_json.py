#            Light snow          /Fog                  /Clear                /Snow                 /Heavy rain
import os
import re
import shutil

js_dir = "../../www/js/route_js"

date_weather_dict = {
    "2015_01_27": "light_snow",
    "2015_01_12": "fog",
    "2015_01_07": "clear",
    "2014_02_03": "snow",
    "2014_04_30": "heavy_rain",
}

for root, dirs, files in os.walk(js_dir, topdown=False):
    for name in files:
        path = os.path.join(root, name)
        if ".js" in path:
            m = re.search(r"\d{4}_\d{2}_\d{2}", str(path))
            date = path[m.start(): m.end()]
            move_target_dir = js_dir + "/" + date_weather_dict[date]
            if not os.path.exists(move_target_dir):
                os.mkdir(move_target_dir)
            # Move a file from the directory d1 to d2
            shutil.move(path, move_target_dir + "/" +path[m.end() + 1:])
# print(date_weather_dict)
