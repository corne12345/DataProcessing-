"""


Chose to compare two weather stations in stead of 3 later on. This means the input
file is bigger and contains unnecessary data.
"""

import csv
import json

vlieland = []
maastricht = []
dates = []
with open("wind.csv", newline='') as csvfile:
    file = csv.reader(csvfile, delimiter=',')
    for row in file:
        if len(row) == 3:
            row[0] = row[0].lstrip()
            row[2] = row[2].lstrip()
            if row[0] == "242":
                vlieland.append(row[2])
                dates.append(row[1])
            elif row[0] == "380":
                maastricht.append(row[2])
winds = list(zip(vlieland, maastricht))
wind_dict = dict(zip(dates, winds))

with open("data.json", "w") as f:
    json.dump(wind_dict,f)
