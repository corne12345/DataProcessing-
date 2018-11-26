"""
Corné Heijnen
12230170
This script is used to convert a csv-file into a json for loading into used d3

"""

import csv
import json
FILENAME = "data.csv"
print(FILENAME)

total = []
with open("data.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    out = json.dumps([row for row in reader])
    f = open("data.json", "w")
    f.write(out)
