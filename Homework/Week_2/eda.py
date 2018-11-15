#!/usr/bin/#!/usr/bin/env python
"""
Corné Heijnen (12230170)
This project is part of the eda-assignment for the UvA-course Data Processing.
The aim of it is to import a given dataset, to clean and preprocess it, with
the main goal of doing some statistical analysis on it and to visualize part of
the data using pandas.
"""

import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
# import statsmodels.api as sm
import json

INPUT_FILE = "input.csv"


def clean_input (input):
    """
    This function loads an input file and stores all its values in seperate
    lists per column. Before storing it, the values in the column will be inspected
    and will be made eligible for input in a pandas DataFrame.
    """

    # Create lists to store the different columns in
    countries = []
    regions = []
    pop_dens = []
    inf_mort = []
    gdp = []
    birth_rates = []

    # Open CSV file and read line per line
    with open("input.csv", newline='') as csvfile:
        file = csv.reader(csvfile, delimiter = ',')

        # skip the first line containing the indices
        next(file)

        # loop over the rows and select only rows containg actual content
        for row in file:
            if len(row) > 0:

                # Add the countries to list countries, stripping the space at the end
                countries.append(row[0].rstrip())

                # Add the region to list regions, stripping whitespaces at the end
                regions.append(row[1].rstrip())

                # Add population density to list pop_dens
                pop_dens_str = row[4].replace(',' , '.')
                try:
                    float(pop_dens_str)
                except ValueError:
                    pop_dens_str = 0
                pop_dens.append(float(pop_dens_str))

                # Add Infant Mortality to list inf_mort and change , to . and set empty to 9999.9
                inf_mort_str = row[7].replace(',' , '.')
                try:
                    float(inf_mort_str)
                except ValueError:
                    inf_mort_str = 0
                inf_mort.append(float(inf_mort_str))

                # Add GDP to list gdp and convert unknown to 0
                gdp_str = row[8].rstrip(' dollars')
                if not gdp_str.isnumeric():
                    gdp_str = 0
                gdp.append(int(gdp_str))

                # Add birth rate to lit birth_rate (for bonus excercise)
                birth_rate_string = row[15].replace(',', '.')
                try:
                    float(birth_rate_string)
                except ValueError:
                    birth_rate_string = 0
                birth_rates.append(float(birth_rate_string))

    return countries, regions, pop_dens, inf_mort, gdp, birth_rates

def create_df (a, b, c, d, e, f):
    """"
    This function takes as argument 6 lists and adds them to a pandas dataframe.
    It then replaces the assigned 0's to NaN-values and return the dataframe.
    The use of NaN prevents the need to drop complete rows that are just missing
    1 value.
    """

    df = pd.DataFrame({'Countries': a, 'Regions': b, 'Population Density': c, 'Infant Mortality': d, 'GDP': e, 'Birth Rates': f})
    df.replace(0, np.NaN)
    df.loc[df['Infant Mortality']==0, 'Infant Mortality']= np.NaN
    df.loc[df['Birth Rates']==0, 'Birth Rates']= np.NaN
    return df

def statistics(df):
    """
    This function provides the user with some basic descriptive statistics
    for dataframes (mean, median, mode and standard deviation). It is void
    """
    print("The Mean of the GDP per capita is", df['GDP'].mean())
    print("The Median of the GDP per capita is", df['GDP'].median())
    print("The Node of the GDP per capita is", df['GDP'].mode())
    print("The standard deviation of the GDP per capita is", df['GDP'].std())

def descriptive_analysis(df, column):
    """"
    This functions performs descriptive analysis on the specified column of the
    used dataframe. It prints these results and remains void.
    """
    df_temp = df[column]
    print(df_temp.describe())

def create_histogram (df):
    """
    This function creates a histogram of the GDP data
    """
    hist = df['GDP'].hist(bins=50, color='red')
    hist.set_title('Histogram of Gross Domestic Products in the world')
    plt.ylabel('Freqency')
    plt.xlabel('Gross Domestic Product')
    plt.show()

def create_boxplot(df):
    """
    This function creates a boxplot of the infant mortality rate.
    """
    boxplot = df.boxplot(column='Infant Mortality')
    boxplot.set_title('Infant mortality boxplot')
    plt.axis([None, None, 0, 200])
    plt.ylabel('Mortality per 1000')
    plt.show()

def save_to_json (df):
    """
    This function saves the required columns of the dataframe in a .json file.
    The index layout is used, since this is specified
    """
    df_json = df.loc[:, ['Countries', 'Regions', 'Population Density', 'Infant Mortality', 'GDP']]
    df_json = df_json.set_index('Countries')
    df_json.to_json('Output.json', orient='index')

def make_scatter (df):
        df_asia = df[ df['Regions'] == 'ASIA (EX. NEAR EAST)']
        plt.scatter(df_asia['GDP'], df_asia['Birth Rates'], label="Asia")
        df_baltics = df[ df['Regions'] == 'BALTICS']
        plt.scatter(df_baltics['GDP'], df_baltics['Birth Rates'], label="Baltics")
        df_cwofindstates = df[ df['Regions'] == 'C.W. OF IND. STATES']
        plt.scatter(df_cwofindstates['GDP'], df_cwofindstates['Birth Rates'], label="Commonwealth of Independent States")
        df_easteur = df[df['Regions'] == 'EASTERN EUROPE']
        plt.scatter(df_easteur['GDP'], df_easteur['Birth Rates'], label='Eastern Europe')
        df_latin  = df[df['Regions'] == 'LATIN AMER. & CARIB']
        plt.scatter(df_latin['GDP'], df_latin['Birth Rates'], label='Latin America')
        df_neareast = df[df['Regions'] == 'NEAR EAST']
        plt.scatter(df_neareast['GDP'], df_neareast['Birth Rates'], label='Near East')
        df_nafrica = df[df['Regions'] == 'NORTHERN AFRICA']
        plt.scatter(df_nafrica['GDP'], df_nafrica['Birth Rates'], label='Northern Africa')
        df_america = df[df['Regions'] == 'NORTHERN AMERICA']
        plt.scatter(df_america['GDP'], df_america['Birth Rates'], label='Northern America')
        df_oceania = df[df['Regions'] == 'OCEANIA']
        plt.scatter(df_oceania['GDP'], df_oceania['Birth Rates'], label='Oceania')
        df_ssafrica = df[df['Regions'] == 'SUB-SAHARAN AFRICA']
        plt.scatter(df_ssafrica['GDP'], df_ssafrica['Birth Rates'], label='Southern Africa')
        df_westeur = df[df['Regions'] == 'WESTERN EUROPE']
        plt.scatter(df_westeur['GDP'], df_westeur['Birth Rates'], label='Western Europe', c='yellow')
        plt.title('GDP vs Birth Rate for all countries')
        plt.xlabel('GDP per capita ($)')
        plt.ylabel('Birth rate (per 1000)')
        plt.legend(loc='upper right')
        plt.show()

if __name__ == "__main__":
    a, b, c, d, e, f = clean_input(INPUT_FILE)
    df = create_df(a, b, c, d, e, f)
    statistics(df)

    # The standard deviation is way bigger than the mean, indicating one or
    # multiple outliers, probably in the upper part. This can be one or multiple,
    # which will probably be a type-O in the column. A histogram can probably
    # help out in this case. Therefore, a histogram is created.
    create_histogram(df)

    # This histogram shows 1 outlier with a GDP of nearly 400,000. Let's find the
    # value and the country it belongs to.
    value = df[df['GDP'] > 300000]
    # print(value)

    # This shows Suriname with a GDP of 400,000. This is not realistic of course
    # The acutal value should be 5900 (Wikipedia). This can be changed as follows:
    df.loc[193, ['GDP']] = 5900

    # there will be a huge effect on the mean and stdev. New statistical analysis
    # will show the impact of correcting the wrong value.
    statistics(df)

    # Infant mortality is analyzed using a five number summary and boxplotself.
    descriptive_analysis(df, 'Infant Mortality')
    create_boxplot(df)

    # The values in the describe method do not all visually match the boxplot. the
    # The boxplot function automatically detects outliers as being more than 1.5
    # times the length of the box away from one of the edges of the box. This results
    # in 5 outliers, which can be displayed
    value = df[df['Infant Mortality'] > 125]
    # print(value)

    # These 5 outliers are 4 Sub-Ssaharan African  countries and Afghanistan,
    # which obviously has suffered greatly from the war and recent unrest. These
    # are rather high, but probably no wrong values. In my opinion, there is
    # therefore no reason to leave out the results in the analysis.

    # Lately, there have been numerous reports about declining birth rate in
    # developed countries. It would therefore be an interesting plot to make a
    # scatter plot plotting GDP and birth_rate and color points based on region
    make_scatter(df)

    #  The scatter clearly shows a negative correlation between GDP and birth rate
    # indicating more developed countries reproduce less. This is partly because
    # the infant mortality is almost zero, so a born baby will be likely to
    # survive. It also clusters the different regions in the same parts of the
    # graph, indicating the coloring by regions is a descriptive function.
