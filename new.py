import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_formula1_results(year, place):
  race_id = 808  # Replace with correct value
  url = f"https://www.formula1.com/en/results/{year}/races/{race_id}/{place}/race-result"
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  return soup

def find_results_table(soup):
  return soup.find("table", class_="f1-table f1-table-with-data w-full").find('tbody').find_all('tr')

year = "2007"
place = "australia"
soup = get_formula1_results(year, place)
results_table = find_results_table(soup)
#print(results_table)


if results_table:
  with open("tdata_in_html_format", "w") as f:
    f.write(str(results_table))
  print("Results table saved to table_code")
  print(len(results_table))
else:
  print("Results table not found")
 


# Extract the winner's time

for result in results_table:
    position = result.find_all('td')[0].text.strip()
    if position == "1":
        p1_time = result.find_all('td')[5].text.strip()
        break

print(f"Winner's time: {p1_time}")

drivers_list = []
for result in results_table:
    dic = {}
    dic['driver'] = result.find_all('td')[2].select("p > span")[1].text.strip()

    # p1_time = result.find_all('td')[5].text.strip()
    # print(p1_time)

    if dic['driver'] in ["Hamilton", "Verstappen"]:
        dic['position'] = result.find_all('td')[0].text.strip()
        dic['laps'] = result.find_all('td')[4].text.strip()
        dic['time'] = result.find_all('td')[5].text.strip()
        dic['points'] = result.find_all('td')[6].text.strip()
        drivers_list.append(dic)

        # Add the winner's time to Hamilton's or Verstappen's time
        # if p1_time:
        #     time1 = p1_time.split(":")
        #     time2 = dic['time'].split(":")
        #     total_seconds = (int(time1[0]) * 60 + float(time1[1])) + (int(time2[0]) * 60 + float(time2[1]))
        #     dic['total_time'] = f"{int(total_seconds // 60)}:{total_seconds % 60:.3f}"

print(drivers_list)

