import csv
import json


vlieland = []
vlissingen = []
maastricht = []
with open("wind.csv", newline='') as csvfile:
    file = csv.reader(csvfile, delimiter=',')
    for row in file:
        if len(row) == 3:
            row[0] = row[0].lstrip()
            row[2] = row[2].lstrip()
            if row[0] == "242":
                vlieland.append(row[1:])
            elif row[0] == "310":
                vlissingen.append(row[1:])
            elif row[0] == "380":
                maastricht.append(row[1:])

print(maastricht)
rows = [vlieland, vlissingen, maastricht]
with open("test.json", "w") as f:
    json.dump(rows,f)
