from pathlib import Path

import pandas
import os

js_start = '''
      function initMap() {
      '''
js_end = '''
          //Loops through all polyline paths and draws each on the map.
          for (let i = 0; i < points.length; i++) {
              var path = new google.maps.Polyline({
              path: points[i],
              geodesic: true,
              strokeColor: colors[i],
              strokeOpacity: 1.0,
              strokeWeight: weights[i],
              });
              path.setMap(map);
          }
      }'''
map_configs = '''
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 12,
          center: {lng: -73.946750, lat: 40.785778},
          mapTypeId: 'terrain',
          styles: [
          {
            "elementType": "geometry",
            "stylers": [
            {
              "color": "#212121"
            }
            ]
          },
          {
            "elementType": "labels.icon",
            "stylers": [
            {
              "visibility": "off"
            }
            ]
          },
          {
            "elementType": "labels.text.fill",
            "stylers": [
            {
              "color": "#757575"
            }
            ]
          },
          {
            "elementType": "labels.text.stroke",
            "stylers": [
            {
              "color": "#212121"
            }
            ]
          },
          {
            "featureType": "administrative",
            "elementType": "geometry",
            "stylers": [
            {
              "color": "#757575"
            }
            ]
          },
          {
            "featureType": "administrative.country",
            "elementType": "labels.text.fill",
            "stylers": [
            {
              "color": "#9e9e9e"
            }
            ]
          },
          {
            "featureType": "administrative.land_parcel",
            "stylers": [
            {
              "visibility": "off"
            }
            ]
          },
          {
            "featureType": "administrative.locality",
            "elementType": "labels.text.fill",
            "stylers": [
            {
              "color": "#bdbdbd"
            }
            ]
          },
          {
            "featureType": "poi",
            "elementType": "labels.text.fill",
            "stylers": [
            {
              "color": "#757575"
            }
            ]
          },
          {
            "featureType": "poi.park",
            "elementType": "geometry",
            "stylers": [
            {
              "color": "#181818"
            }
            ]
          },
          {
            "featureType": "poi.park",
            "elementType": "labels.text.fill",
            "stylers": [
            {
              "color": "#616161"
            }
            ]
          },
          {
            "featureType": "poi.park",
            "elementType": "labels.text.stroke",
            "stylers": [
            {
              "color": "#1b1b1b"
            }
            ]
          },
          {
            "featureType": "road",
            "elementType": "geometry.fill",
            "stylers": [
            {
              "color": "#2c2c2c"
            }
            ]
          },
          {
            "featureType": "road",
            "elementType": "labels.text.fill",
            "stylers": [
            {
              "color": "#8a8a8a"
            }
            ]
          },
          {
            "featureType": "road.arterial",
            "elementType": "geometry",
            "stylers": [
            {
              "color": "#373737"
            }
            ]
          },
          {
            "featureType": "road.highway",
            "elementType": "geometry",
            "stylers": [
            {
              "color": "#3c3c3c"
            }
            ]
          },
          {
            "featureType": "road.highway.controlled_access",
            "elementType": "geometry",
            "stylers": [
            {
              "color": "#4e4e4e"
            }
            ]
          },
          {
            "featureType": "road.local",
            "elementType": "labels.text.fill",
            "stylers": [
            {
              "color": "#616161"
            }
            ]
          },
          {
            "featureType": "transit",
            "elementType": "labels.text.fill",
            "stylers": [
            {
              "color": "#757575"
            }
            ]
          },
          {
            "featureType": "water",
            "elementType": "geometry",
            "stylers": [
            {
              "color": "#000000"
            }
            ]
          },
          {
            "featureType": "water",
            "elementType": "labels.text.fill",
            "stylers": [
            {
              "color": "#3d3d3d"
            }
            ]
          }
          ]
        });
        '''

data_dir = "../../../Data"
js_dir = "../../www/js/route_js"
csvs = []
for root, dirs, files in os.walk(data_dir + "/NYC_Route_Planner_Result/", topdown=False):
    for name in files:
        path = os.path.join(root, name)
        if "statistic" in path and ".csv" in path and "yellow" in path:
            csvs.append(path)

if not os.path.exists(js_dir):
    os.mkdir(js_dir)

for csv in csvs:
    path = Path(csv)
    file = open(js_dir + "/" + str(path.name).replace(".csv", ".js"), "w+")
    file.write(js_start + map_configs)
    file.write("\nvar points = [\n")
    # result_js = js_start + map_configs
    df = pandas.read_csv(csv)
    print("System: start processing " + csv)
    color_list = []
    weight_list = []
    count = 0
    for index, row in df.iterrows():
        var_str = '[{ lng: %s, lat: %s }, { lng: %s, lat: %s }],\n' % (
            str(row["p1_x"]), str(row["p1_y"]), str(row["p2_x"]), str(row["p2_y"]))
        file.write(var_str)
        color_list.append(row["color"])
        weight_list.append(row["weight"])
    file.write("\n]\n")
    file.write("var colors = " + str(color_list) + "\n")
    file.write("var weights = " + str(weight_list) + "\n")
    file.write(js_end)
    file.close()
