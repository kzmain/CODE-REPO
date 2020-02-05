import os

times = [0, 1, 2, 3, 4, 5, 6, 7,
         8, 9, 10, 11, 12, 13, 14, 15,
         16, 17, 18, 19, 20, 21, 22, 23]
weathers = ["clear", "fog", "heavy_rain", "light_snow", "snow"]
for weather in weathers:
    for time in times:
        time_one = str(time)
        time_two = str(time)
        if len(time_two) == 1:
            time_two = "0" + time_two
        html = """<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <style>
      /* Always set the map height explicitly to define the size of the div
       * element that contains the map. */
""" + "       #map {height: 100%;}" + \
               """      /* Optional: Makes the sample page fill the window. */
          html, body {
            height: 100%;
            margin: 0;
            padding: 0;
          }
        </style>
      </head>
      <body>
      """ + "<div id=\"map\"></div>\n" + \
               "  <script type=\"text/javascript\" src=\"../../../js/route_js/" + weather + "/h" + time_one + ".js\"></script>\n" + \
               "  <script async defer src=\"https://maps.googleapis.com/maps/api/js?key=AIzaSyBpo4t6BxgT9Z_gXPmnZPSIorxOCAUnxiI&callback=initMap\"></script>\n" + \
               """  </body>
</html>"""
        html_folder_route = "../../www/html"
        route_folder = html_folder_route + "/routes"
        target_folder = route_folder + "/" + weather
        if not os.path.exists(html_folder_route):
            os.mkdir(html_folder_route)
        if not os.path.exists(route_folder):
            os.mkdir(route_folder)
        if not os.path.exists(target_folder):
            os.mkdir(target_folder)
        file = open(target_folder + "/" + time_one + ".html", "w+")
        file.write(html)
        file.close()
