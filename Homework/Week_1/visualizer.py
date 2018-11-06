#!/usr/bin/env python
# Name:
# Student number:
"""
This script visualizes data obtained from a .csv file
"""

import csv
import matplotlib.pyplot as plt

# Global constants for the input file, first and last year
INPUT_CSV = "movies.csv"
START_YEAR = 2008
END_YEAR = 2018

# Global dictionary for the data
data_dict = {str(key): [] for key in range(START_YEAR, END_YEAR)}

if __name__ == "__main__":

    # read the csv file, line by line, skipping first line(indeces)
    with open(INPUT_CSV, newline='') as csvfile:
        file = csv.reader(csvfile, delimiter = ',')
        next(file)

        # Add the rating to the year the movie was released
        for row in file:
            data_dict[row[-1]].append(float(row[1]))

# Calculate the average rating by looping over a copy of the dictionary
average_list = []
for k, v in data_dict.items():
    average_list.append(sum(v)/len(v))

# Save keys and values in lists to create plot
years = list(data_dict.keys())

# Make a list of the average rating per year to plot in the graph
average_year = [sum(average_list)/len(average_list)] * len(average_list)

# Create plot with average rating per year and the total average
plt.plot(years, average_list, years, average_year)
plt.ylabel('Rating')
plt.xlabel('Year')
plt.title('Average rating of top 50 movies per year')
plt.show()

# The average rating per year of the films in the top 50 is in my opinion not the
# best indicator for the succes of a certain year. The amount of movies in this top
# 50 is at least equally important. Another approach would be to calculate the
# cumulative score per year (summing all scores per year). This would give higher
# peaks for years that show more movies. Powering teither the amount of entries or
# the score is an option to change the relative importance of either. For the next
# example I have chosen to take the square root of the amount of entries to give
# more importance to the average score.

# Make another copy of the data_dict and calculate cumulative score
cumulative_list = []
for k,v in data_dict.items():
    cumulative_list.append(sum(v)/(len(v)**0.5))

# Save scores as seperate lisst(years exists already) and create average
average_score = [sum(cumulative_list)/len(cumulative_list)] * len(cumulative_list)

# Create plot of cumulative score
plt.plot(years, cumulative_list, 'r', years, average_score)
plt.ylabel('Cumulative score')
plt.xlabel('Year')
plt.title('Average cumulative score of top 50 movies per year')
plt.show()

# calculate normalized ratings and cumulative scores
values_normalized = []
for i in range(len(years)):
    values_normalized.append(average_list[i]/average_year[0])

scores_normalized = []
for i in range(len(years)):
    scores_normalized.append(cumulative_list[i]/average_score[0])

# plot both normalized cumulative scores and normalized ratings
plt.plot(years, scores_normalized, years, values_normalized)
plt.ylabel('normalized scorre')
plt.xlabel('Year')
plt.title('Normalized score for each year based on IMDB top 50')
plt.show()

# The normalized graph shows a positive trend between the years and score,
# indicating a more positive score for more recent years. Since in the average
# score does not show a similar trend, this difference is mostly a result of
# more entries for recent years. This observation can not further be explained
# by the data alone and could be further investigated. To check the theory of
# more entries in recent years, another graph is created.

# Make a copy of the data_dict for entries
entries_list = []
for k,v in data_dict.items():
    entries_list.append(len(v))

average_entries = [sum(entries_list)/len(years)] * len(years)

plt.bar(years, entries_list)
plt.ylabel('Entries in top 50')
plt.xlabel('Year')
plt.title('Amount of entries in top 50 per year')
plt.show()
