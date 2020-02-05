#----------------------------------------------------------------------------------------------------------------------
#       2019 LSDE GROUP 11 KAI ZHANG/YI ZHEN ZHAO/YU WANG
#       Last Update: 05-10-2019 11:16
#       Version: 1.1
#----------------------------------------------------------------------------------------------------------------------
#       # Description:
#           This Python script is target at grabbing data from `https://www.timeanddate.com`,
#----------------------------------------------------------------------------------------------------------------------
#       * Included:
#            * NYC 2009 - 2019's weather grabbed by python crawler
#----------------------------------------------------------------------------------------------------------------------
#       * Data Explanation:
#            * csv files:
#               - Location: data_dir/NYC_Weathers/csv
#               - Target: Save result files
#            * html files:
#               - Location: data_dir/NYC_Weathers/html
#               - Target: Save backup files
#----------------------------------------------------------------------------------------------------------------------
#       # Potential Problem:
#           * Weather before ten years from current month only have 01 st - 15 th data.
#----------------------------------------------------------------------------------------------------------------------
#       # Caution:
#           * If request weather data in future (which is obviously not exist), it will return today's weather.
#             So data after today should be deleted manually
#----------------------------------------------------------------------------------------------------------------------
import json
import re
import os
import requests
from bs4 import BeautifulSoup as bs

# Local mode
data_dir = "../Data"
## Group 11 Databricks mode
# data_dir = "/dbfs/mnt/group11/Data"

s_year = 2009
e_year = 2019

s_month = 1
e_month = 12
# Get weather from
for t_year in range(s_year, e_year + 1, 1):
    for t_month in range(s_month, e_month + 1, 1):
        # Request weather data page
        print("Start process " + str(t_year) + "." + str(t_month) + "'s weather.")
        url = "https://www.timeanddate.com/weather/usa/new-york/historic?month=" + str(t_month) + "&year=" + str(t_year)
        page = requests.get(url)
        # Make data dir
        weather_dir = data_dir + "/NYC_Weathers"
        html_dir = weather_dir + "/html/"
        csv_dir = weather_dir + "/csv/"
        if not os.path.exists(weather_dir):
            os.mkdir(weather_dir)
        if not os.path.exists(html_dir):
            os.mkdir(html_dir)
        if not os.path.exists(csv_dir):
            os.mkdir(csv_dir)
        if page.status_code == 200:
            # Write backup files
            backup_file_name = str(t_year) + "." + str(t_month) + ".html"
            file = open(html_dir + backup_file_name, "w+")
            file.write(page.text)
            file.close()
            soup = bs(page.content, 'html.parser')
            scripts = soup.find_all('script')
            # Extract weather data by regx
            for script in scripts:
                json_string = re.search(r'(?<=data=)({.*})', str(script))
                if json_string is not None:
                    js = json.loads(str(script)[json_string.start():json_string.end()])
                    details = js["detail"]
                    w_csv = str(t_year) + "_" + str(t_month) + "_" + "weather" + ".csv"
                    # d_csv = str(t_year) + "_" + str(t_month) + "_" + "date" + ".csv"
                    w_file = open(csv_dir + w_csv, "w+")
                    # d_file = open(d_csv, "w+")
                    w_file.write("time_stamp,"
                                 "time_duration,"
                                 "day_in_week,"
                                 "day_in_month,"
                                 "month,"
                                 "year,"
                                 "temp_h,"
                                 "temp_l,"
                                 "baro,"
                                 "wind,"
                                 "wd,"
                                 "hum,"
                                 "weather\n")
                    # Prepare to write csv result file
                    for detail in details:
                        e1 = detail["ts"]
                        date = detail["ds"].split(",")[0].split(" ")
                        e2 = detail["ds"].split(",")[1].rstrip()
                        e3 = date[0]
                        e4 = date[1]
                        e5 = date[2]
                        e6 = date[3]
                        if "temp" in detail.keys():
                            e7 = detail["temp"]
                        else:
                            e7 = "NULL"
                        if "templow" in detail.keys():
                            e8 = detail["templow"]
                        else:
                            e8 = "NULL"
                        e9 = detail["baro"]
                        e10 = detail["wind"]
                        e11 = detail["wd"]
                        e12 = detail["hum"]
                        weathers = detail["desc"].split(".")
                        for weather in weathers:
                            if weather.rstrip() != "":
                                d_result = str(e1).strip() + "," + \
                                           str(e2).split(" — ")[1] + "," + \
                                           str(e3) + "," + \
                                           str(e4) + "," + \
                                           str(e5) + "," + \
                                           str(e6) + "," + \
                                           str(e7) + "," + \
                                           str(e8) + "," + \
                                           str(e9) + "," + \
                                           str(e10) + "," + \
                                           str(e11) + "," + \
                                           str(e12) + "," + \
                                           str(weather).strip() + \
                                           "\n"
                                w_file.writelines(d_result)
                    w_file.close()
