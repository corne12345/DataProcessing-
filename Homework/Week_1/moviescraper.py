#!/usr/bin/env python
# Name:
# Student number:
"""
This script scrapes IMDB and outputs a CSV file with highest rated movies.
"""

import csv
import pandas as pd
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

TARGET_URL = "https://www.imdb.com/search/title?title_type=feature&release_date=2008-01-01,2018-01-01&num_votes=5000,&sort=user_rating,desc"
BACKUP_HTML = 'movies.html'
OUTPUT_CSV = 'movies.csv'


def extract_movies(dom):
    """
    Extract a list of highest rated movies from DOM (of IMDB page).
    Each movie entry should contain the following fields:
    - Title
    - Rating
    - Year of release (only a number!)
    - Actors/actresses (comma separated if more than one)
    - Runtime (only a number!)
    """

    # Create a list of individual movies by cutting at the start of each movie
    movie_list = dom.find_all('div', class_= "lister-item-content")
    titles = []
    ratings = []
    years = []
    actors = []
    runtimes = []

    # loop through the movie lit ot repeat tasks for each movie
    for i in range(len(movie_list)):

        # Isolate title by searching for returning text within anchor tag
        title = movie_list[i].a.text
        titles.append(title)

        # Isolate rating in file and use rstrip and lstrip to get clean result
        rating = movie_list[i].find('div', class_ = 'inline-block ratings-imdb-rating').text
        rating = rating.rstrip()
        rating = float(rating.lstrip())
        ratings.append(rating)

        # Isolate year of release by its name and strip braces
        year = movie_list[i].find('span', class_ = 'lister-item-year text-muted unbold').text
        year = int(year [-5:-1])
        years.append(year)

        # Isolate actors by searching all names and split after stars
        actor = movie_list[i].find_all('p', class_='')
        actor = str(actor[1].text)
        actor = actor.split("Stars:")[-1]
        actor = actor.replace('\n', '')
        if actor == '':
            actor = "No actors mentioned"
        actors.append(actor)

        # Isolate Runtime
        runtime = movie_list[i].find('span', class_ = 'runtime').text
        runtime = int(runtime.replace(' min', ''))
        runtimes.append(runtime)

    # Create pandas dataframe containing all the resuls and check output
    movies = pd.DataFrame({'Title': titles, 'Rating': ratings, 'Year': years, 'Actors': actors, 'Runtime': runtimes})
    print(movies.info())
    print(movies.head)
    return movies   # REPLACE THIS LINE AS WELL IF APPROPRIATE


def save_csv(outfile, movies):
    """
    Output a CSV file containing highest rated movies.
    """
    # writer = csv.writer(outfile)
    # writer.writerow(['Title', 'Rating', 'Year', 'Actors', 'Runtime'])
    movies.to_csv(outfile, index = False)

    # ADD SOME CODE OF YOURSELF HERE TO WRITE THE MOVIES TO DISK


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        print('The following error occurred during HTTP GET request to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


if __name__ == "__main__":

    # get HTML content at target URL
    html = simple_get(TARGET_URL)

    # save a copy to disk in the current directory, this serves as an backup
    # of the original HTML, will be used in grading.
    with open(BACKUP_HTML, 'wb') as f:
        f.write(html)

    # parse the HTML file into a DOM representation
    dom = BeautifulSoup(html, 'html.parser')

    # extract the movies (using the function you implemented)
    movies = extract_movies(dom)

    # write the CSV file to disk (including a header)
    with open(OUTPUT_CSV, 'w', newline='') as output_file:
        save_csv(output_file, movies)
