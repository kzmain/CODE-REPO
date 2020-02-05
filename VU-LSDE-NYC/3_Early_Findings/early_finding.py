# ----------------------------------------------------------------------------------------------------------------------
#       2019 LSDE GROUP 11 KAI ZHANG/YI ZHEN ZHAO/YU WANG
#       Last Update: 05-10-2019 11:31
#       Version: 1.1
#
#       # Description: This Python script is target at showing early findings,
#       * Included:
#            * Yearly Trending: 
#              1. show_portion_by_year():   Shows different types of taxis protion by year (Stack area chart)
#              2. show_quantity_by_month(): Shows different types of taxis
#              (monthly quantity)/(current year monthly quantity) (Line Chart)
#            * Monthly Trending:
#              1. show_quantity_by_year(): Shows different types of taxis yearly quantity
# ----------------------------------------------------------------------------------------------------------------------
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
import numpy as np
from matplotlib.pyplot import figure

# Make High Definition matplotlib figure setting
mpl.rcParams['figure.dpi'] = 300
# ----------------------------------------Set data value------------------------------------------------------------
yellow = [13360542, 12896505, 13930875, 13817006, 14312632, 13786317,
          13244718, 13295895, 13571573, 15123438, 13801691, 14104529,
          14375936, 10777183, 12430384, 14585797, 14896529, 14255642,
          14072908, 12011107, 14963072, 13684544, 13362186, 13255563,
          12908065, 13312535, 15121148, 13973817, 14878387, 14534507,
          14172441, 12690942, 13962843, 15071464, 13950676, 14335010,
          14386194, 14393399, 15510567, 14862342, 14919720, 14466366,
          13776195, 13767192, 13969853, 14007218, 13304521, 14194137,
          14294952, 13532296, 15248178, 14611867, 14216456, 13927315,
          13439245, 12214262, 13775621, 14647435, 13931402, 13553515,
          13416707, 12693812, 14972627, 14145242, 14244484, 13279859,
          12595005, 12188339, 12945168, 13838111, 12825826, 12616973,
          12354533, 12052671, 12934457, 12692325, 12794438, 11988575,
          11253688, 10832082, 10921803, 11977483, 10991754, 11136659,
          10603283, 11063902, 11879348, 11605911, 11533753, 10845480,
          10156994, 9810408, 9976229, 10709708, 9960987, 10300810,
          9582434, 9047212, 10147464, 9904713, 9960118, 9519745,
          8463632, 8302265, 8813714, 9630796, 9151633, 9370846,
          8640154, 8378000, 9297257, 9178506, 9094762, 8586664,
          7732770, 7733271, 7917229, 8682246, 8016862, 8041550,
          7553880, 6916732, 7720787, 7328512, 7450162, 6823156]

green = [0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0,
         0, 6001, 45347, 159451, 365037, 579102,
         772826, 969806, 1252447, 1268506, 1379288, 1298352,
         1235375, 1304634, 1325351, 1450588, 1504024, 1597428,
         1464519, 1530399, 1672144, 1615953, 1736308, 1592491,
         1498564, 1490796, 1453688, 1586334, 1488206, 1563990,
         1403853, 1470514, 1534169, 1502608, 1496911, 1367099,
         1298006, 1215312, 1133044, 1223376, 1120081, 1195121,
         1045429, 998879, 1131875, 1057355, 1035491, 954110,
         893766, 848016, 863444, 905436, 855052, 886157,
         775749, 754310, 819504, 782960, 779043, 723237,
         669434, 651583, 652143, 694830, 641666, 667441,
         612534, 558772, 583484, 499391, 489982, 456214]

fhv = [0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0,
       2746033, 3126401, 3281427, 3917789, 4296067, 4253883,
       4394463, 5283081, 6654426, 8672537, 8416512, 8824990,
       8756726, 9497970, 9724587, 10242362, 10852568, 10870256,
       11117893, 11305705, 11789427, 12719591, 12496635, 13911421,
       13657212, 13284950, 15703039, 14764853, 15397388, 15362154,
       15672672, 15905901, 16621439, 17890689, 18048534, 19971846,
       19808094, 19350693, 21985249, 21049377, 21565692, 21135283,
       21596443, 22116391, 22147421, 23286795, 22870474, 23854144,
       23130810, 1706745, 1329077, 1908099, 2040813, 1967953]

hvfhv = [0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0,
         0, 20153485, 23857720, 21728865, 22322856, 20995611]

population = [195226, 195777, 194985, 195745, 196280, 196563, 196614, 196416, 195907, 195422]

gdp = [127770, 134086, 136580, 143923, 147705, 154276, 161837, 166267, 171771, 173759]
# ----------------------------------------Create Dataframe------------------------------------------------------------
data = pd.DataFrame({'yellow': yellow, 'green': green, 'fhv': fhv, 'hvfhv': hvfhv, }, index=range(0, 126))
data["sum"] = data["yellow"] + data["green"] + data["fhv"] + data["hvfhv"]

# ----------------------------------------Monthly Data to Yearly Data------------------------------------------------------------
rows = []
for i in range(0, 126, 12):
    if i == 120:
        continue
    y_yellow = data.iloc[i]["yellow"] + data.iloc[i + 1]["yellow"] + data.iloc[i + 2]["yellow"] + \
               data.iloc[i + 3]["yellow"] + data.iloc[i + 4]["yellow"] + data.iloc[i + 5]["yellow"] + \
               data.iloc[i + 6]["yellow"] + data.iloc[i + 7]["yellow"] + data.iloc[i + 8]["yellow"] + \
               data.iloc[i + 9]["yellow"] + data.iloc[i + 10]["yellow"] + data.iloc[i + 11]["yellow"]
    y_green = data.iloc[i]["green"] + data.iloc[i + 1]["green"] + data.iloc[i + 2]["green"] + \
              data.iloc[i + 3]["green"] + data.iloc[i + 4]["green"] + data.iloc[i + 5]["green"] + \
              data.iloc[i + 6]["green"] + data.iloc[i + 7]["green"] + data.iloc[i + 8]["green"] + \
              data.iloc[i + 9]["green"] + data.iloc[i + 10]["green"] + data.iloc[i + 11]["green"]
    y_fhv = data.iloc[i]["fhv"] + data.iloc[i + 1]["fhv"] + data.iloc[i + 2]["fhv"] + \
            data.iloc[i + 3]["fhv"] + data.iloc[i + 4]["fhv"] + data.iloc[i + 5]["fhv"] + \
            data.iloc[i + 6]["fhv"] + data.iloc[i + 7]["fhv"] + data.iloc[i + 8]["fhv"] + \
            data.iloc[i + 9]["fhv"] + data.iloc[i + 10]["fhv"] + data.iloc[i + 11]["fhv"] + \
            data.iloc[i]["hvfhv"] + data.iloc[i + 1]["hvfhv"] + data.iloc[i + 2]["hvfhv"] + \
            data.iloc[i + 3]["hvfhv"] + data.iloc[i + 4]["hvfhv"] + data.iloc[i + 5]["hvfhv"] + \
            data.iloc[i + 6]["hvfhv"] + data.iloc[i + 7]["hvfhv"] + data.iloc[i + 8]["hvfhv"] + \
            data.iloc[i + 9]["hvfhv"] + data.iloc[i + 10]["hvfhv"] + data.iloc[i + 11]["hvfhv"]
    y_sum = data.iloc[i]["sum"] + data.iloc[i + 1]["sum"] + data.iloc[i + 2]["sum"] + \
            data.iloc[i + 3]["sum"] + data.iloc[i + 4]["sum"] + data.iloc[i + 5]["sum"] + \
            data.iloc[i + 6]["sum"] + data.iloc[i + 7]["sum"] + data.iloc[i + 8]["sum"] + \
            data.iloc[i + 9]["sum"] + data.iloc[i + 10]["sum"] + data.iloc[i + 11]["sum"]
    rows.append([y_yellow, y_green, y_fhv, y_sum])
year = pd.DataFrame(rows, columns=['y_taxi', 'g_taxi', 'fhv', "sum"])


# ----------------------------------------Functions Start------------------------------------------------------------
def show_portion_by_year():
    figure(num=None, figsize=(12, 6), dpi=80, facecolor='w', edgecolor='k')
    year_without_sum = year[['y_taxi', 'g_taxi', 'fhv']]
    # We need to transform the data from raw data to yearly percentage (fraction)
    year_without_sum_perc = year_without_sum.divide(year_without_sum.sum(axis=1), axis=0).multiply(100)
    plt.stackplot(range(0, 10), year_without_sum_perc["y_taxi"], year_without_sum_perc["g_taxi"],
                  year_without_sum_perc["fhv"],
                  labels=['Yellow', 'Green', 'FHV'], )
    plt.xlabel('Quantity')
    plt.ylabel('Year')
    plt.legend(loc='upper left')
    plt.margins(0, 0)
    plt.title('Taxi type market share')

    plt.title('Taxi Trip Market Share of 10 years')
    plt.xticks(np.arange(10), [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018])
    plt.xlabel('Year')
    plt.ylabel('Percentage')
    plt.savefig('year_portion_pattern.png')
    plt.show()


def show_quantity_by_month():
    figure(num=None, figsize=(12, 6), dpi=80, facecolor='w', edgecolor='k')
    plt.xticks(np.arange(12), ('January', 'February', 'March', 'April', 'May', 'June',
                               'July', 'August', 'September', 'October', 'November', 'December'))
    y1_s = data["sum"].iloc[0:12]
    y2_s = data["sum"].iloc[12:24]
    y3_s = data["sum"].iloc[24:36]
    y4_s = data["sum"].iloc[36:48]
    y5_s = data["sum"].iloc[48:60]
    y6_s = data["sum"].iloc[60:72]
    y7_s = data["sum"].iloc[72:84]
    y8_s = data["sum"].iloc[84:96]
    y9_s = data["sum"].iloc[96:108]
    y10_s = data["sum"].iloc[108:120]

    year_1 = y1_s.divide(y1_s.mean()).tolist()
    year_2 = y2_s.divide(y2_s.mean()).tolist()
    year_3 = y3_s.divide(y3_s.mean()).tolist()
    year_4 = y4_s.divide(y4_s.mean()).tolist()
    year_5 = y5_s.divide(y5_s.mean()).tolist()
    year_6 = y6_s.divide(y6_s.mean()).tolist()
    year_7 = y7_s.divide(y7_s.mean()).tolist()
    year_8 = y8_s.divide(y8_s.mean()).tolist()
    year_9 = y9_s.divide(y9_s.mean()).tolist()
    year_10 = y10_s.divide(y10_s.mean()).tolist()

    y_1_zn = (y1_s - y1_s.mean()).divide(y1_s.std()).tolist()
    y_2_zn = (y2_s - y2_s.mean()).divide(y2_s.std()).tolist()
    y_3_zn = (y3_s - y3_s.mean()).divide(y3_s.std()).tolist()
    y_4_zn = (y4_s - y4_s.mean()).divide(y4_s.std()).tolist()
    y_5_zn = (y5_s - y5_s.mean()).divide(y5_s.std()).tolist()
    y_6_zn = (y6_s - y6_s.mean()).divide(y6_s.std()).tolist()
    y_7_zn = (y7_s - y7_s.mean()).divide(y7_s.std()).tolist()
    y_8_zn = (y8_s - y8_s.mean()).divide(y8_s.std()).tolist()
    y_9_zn = (y9_s - y9_s.mean()).divide(y9_s.std()).tolist()
    y_10_zn = (y10_s - y10_s.mean()).divide(y10_s.std()).tolist()

    # plt.plot(year_1)
    # plt.plot(year_2)
    # plt.plot(year_3)
    # plt.plot(year_4)
    # plt.plot(year_5)
    # plt.plot(year_6)
    # plt.plot(year_7)
    # plt.plot(year_8)
    # plt.plot(year_9)
    # plt.plot(year_10)

    plt.plot(y_1_zn)
    plt.plot(y_2_zn)
    plt.plot(y_3_zn)
    plt.plot(y_4_zn)
    plt.plot(y_5_zn)
    plt.plot(y_6_zn)
    plt.plot(y_7_zn)
    plt.plot(y_8_zn)
    plt.plot(y_9_zn)
    plt.plot(y_10_zn)

    plt.legend(loc='upper left')
    plt.title('Taxi Trip Monthly Trending of 10 years')
    plt.xlabel('Month')
    plt.ylabel('Month Quantity/Monthly Mean Quantity')

    plt.savefig('monthly_quantity_pattern.png')
    plt.show()


def show_quantity_by_year():
    figure(num=None, figsize=(12, 6), dpi=80, facecolor='w', edgecolor='k')
    plt.xticks(np.arange(10), [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018])
    plt.plot(year["y_taxi"])
    plt.plot(year["g_taxi"])
    plt.plot(year["fhv"])
    plt.plot(year["sum"])

    plt.legend(loc='upper left')
    plt.xlabel('Year')
    plt.ylabel('Year Quantity')
    plt.title('Taxi Trip Quantity of 10 years')

    plt.savefig('yearly_quantity_pattern.png')
    plt.show()


# show_quantity_by_year()
# show_portion_by_year()
# show_quantity_by_month()
