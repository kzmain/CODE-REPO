# import requests
# from bs4 import BeautifulSoup as bs
#
# # url = "https://www.museumkaart.nl/museumkaartgeldig#tab-Drenthe"
# url = "https://www.museumkaart.nl/museum/Fries+Scheepvaartmuseum.aspx"
# page = requests.get(url)
# if page.status_code == 200:
#     soup = bs(page.content, 'html.parser')
#     print()
# print()
import pandas as pd

df = pd.DataFrame([[1, 2], [4, 5], [7, 8]], index=['cobra', 'viper', 'sidewinder'], columns=['max_speed', 'shield'])
test = df.loc[df['shield'] > 0]
print()