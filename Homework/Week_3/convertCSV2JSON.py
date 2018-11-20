import csv

with open("wind.txt") as txtfile:
    file = csv.reader(txtfile, delimiter=',')
    print(file)
