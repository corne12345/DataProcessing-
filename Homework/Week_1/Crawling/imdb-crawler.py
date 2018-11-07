#!/usr/bin/env python
# Name:
# Student number:
"""
This script crawls the IMDB top 250 movies.
"""

import os
import csv
import codecs
import errno

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

# global constants
TOP_250_URL = 'http://www.imdb.com/chart/top'
OUTPUT_CSV = 'top250movies.csv'
SCRIPT_DIR = os.path.split(os.path.realpath(__file__))[0]
BACKUP_DIR = os.path.join(SCRIPT_DIR, 'HTML_BACKUPS')

# --------------------------------------------------------------------------
# Utility functions (no need to edit):


def create_dir(directory):
    """
    Create directory if needed.
    Args:
        directory: string, path of directory to be made
    Note: the backup directory is used to save the HTML of the pages you
        crawl.
    """

    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno == errno.EEXIST:
            # Backup directory already exists, no problem for this script,
            # just ignore the exception and carry on.
            pass
        else:
            # All errors other than an already existing backup directory
            # are not handled, so the exception is re-raised and the
            # script will crash here.
            raise


def save_csv(filename, rows):
    """
    Save CSV file with the top 250 most popular movies on IMDB.
    Args:
        filename: string filename for the CSV file
        rows: list of rows to be saved (250 movies in this exercise)
    """
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'title', 'year', 'runtime', 'genre(s)', 'director(s)', 'writer(s)',
            'actor(s)', 'rating(s)', 'number of rating(s)'
        ])

        writer.writerows(rows)


def make_backup(filename, html):
    """
    Save HTML to file.
    Args:
        filename: absolute path of file to save
        html: (unicode) string of the html file
    """

    with open(filename, 'wb') as f:
        f.write(html)


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


def main():
    """
    Crawl the IMDB top 250 movies, save CSV with their information.
    Note:
        This function also makes backups of the HTML files in a sub-directory
        called HTML_BACKUPS (those will be used in grading).
    """

    # Create a directory to store copies of all the relevant HTML files (those
    # will be used in testing).
    print('Setting up backup dir if needed ...')
    create_dir(BACKUP_DIR)

    # Make backup of the IMDB top 250 movies page
    print('Access top 250 page, making backup ...')
    top_250_html = simple_get(TOP_250_URL)
    top_250_dom = BeautifulSoup(top_250_html, 'lxml')

    make_backup(os.path.join(BACKUP_DIR, 'index.html'), top_250_html)

    # extract the top 250 movies
    print('Scraping top 250 page ...')
    url_strings = scrape_top_250(top_250_dom)

    # grab all relevant information from the 250 movie web pages
    rows = []
    for i, url in enumerate(url_strings):  # Enumerate, a great Python trick!
    # url = url_strings[0]
    # for i in range(1):
        print('Scraping movie %d ...' % i)

        # Grab web page
        movie_html = simple_get(url)

        # Extract relevant information for each movie
        movie_dom = BeautifulSoup(movie_html, "lxml")
        rows.append(scrape_movie_page(movie_dom))

        # Save one of the IMDB's movie pages (for testing)
        if i == 83:
            html_file = os.path.join(BACKUP_DIR, 'movie-%03d.html' % i)
            make_backup(html_file, movie_html)

    # Save a CSV file with the relevant information for the top 250 movies.
    print('Saving CSV ...')
    save_csv(os.path.join(SCRIPT_DIR, 'top250movies.csv'), rows)


def scrape_top_250(soup):
    """
    Scrape the IMDB top 250 movies index page.
    Args:
        soup: parsed DOM element of the top 250 index page
    Returns:
        A list of strings, where each string is the URL to a movie's page on
        IMDB, note that these URLS must be absolute (i.e. include the http
        part, the domain part and the path part).
    """

    # Create a list of length 250 by splitting on specific moviie seperator
    movie_list = soup.find_all('td', class_='titleColumn')
    movie_urls = []

    # loop over  list and find URL; next, use prefix to create total URL and add
    for i in range(len(movie_list)):
        movie_list[i] = movie_list[i].find('a')
        movie_list[i] = 'https://www.imdb.com' + movie_list[i].get('href')
        movie_urls.append(movie_list[i])

    return movie_urls


def scrape_movie_page(dom):
    """
    Scrape the IMDB page for a single movie
    Args:
        dom: BeautifulSoup DOM instance representing the page of 1 single
            movie.
    Returns:
        A list of strings representing the following (in order): title, year,
        duration, genre(s) (semicolon separated if several), director(s)
        (semicolon separated if several), writer(s) (semicolon separated if
        several), actor(s) (semicolon separated if several), rating, number
        of ratings.
    """
    # Scrape the tile and split it between braces to extract title and year
    strip = dom.find('h1').text
    strip = strip.split('(')
    title = strip[0]
    title = title[:-1]
    year = strip[-1].rstrip()
    year = year[:-1]

    # Scrape time classes to find runtime; second hit is runtime in minutes. Only append time
    runtime = dom.find_all('time')
    if len(runtime) > 1:
        runtime = runtime[1].text
        runtime = runtime[:-4]
    else:
        runtime = runtime[0].text
        duration = []
        for c in runtime:
            if c.isnumeric():
                duration.append(c)
        runtime = int(duration[0]) * 60 + int(duration[1]) * 10 + int(duration[2])

        # runtime = int(runtime[0]) * 60 + 10 * int(runtime [3]) + int(runtime[4])

    # Save all genres in a set to prevent double genres from occurring
    genres = set()
    raw = dom.find_all('a')
    for i in range(len(raw)):
        if 'genres' in str(raw[i]):
            genre_raw = raw[i].text
            genre = ''
            for c in genre_raw:
                if c.isalpha() == True:
                    genre += c
            genres.add(genre)

    genres_string = ''
    genres = list(genres)
    if len(genres) == 1:
        genres_string = str(genres[0])
    else:
        for i in range(len(genres)-1):
            genres_string += genres[i] + '; '
        genres_string += genres[-1]

    # Scraping for people and redirect this to directors, writers and actors
    people = dom.find('div', class_= 'plot_summary')
    people = people.find_all('div', class_= 'credit_summary_item')
    directors = people[0]
    writers = people[1]
    actors = people[2]

    directors = directors.find_all('a')
    for i in range(len(directors)):
        directors[i] = directors[i].text
    directors_string = ''
    if len(directors) > 2:
        directors = directors[0:2]
    if len(directors) == 1:
        directors_string = str(directors[0])
    else:
        for i in range(len(directors)-1):
            directors_string += directors[i] + '; '
        directors_string += directors [-1]


    writers = writers.find_all('a')
    for i in range(len(writers)):
        writers[i] = writers[i].text
    writers_string = ''
    if len(writers) > 2:
        writers = writers[0:2]
    if len(writers) == 1:
        writers_string = str(writers[0])
    else:
        for i in range(len(writers)-1):
            writers_string += writers[i] + '; '
        writers_string += writers [-1]

    actors = actors.find_all('a')
    for i in range(len(actors)):
        actors[i] = actors[i].text
    actors_string = ''
    if len(actors) > 3:
        actors = actors[0:3]
    if len(actors) == 1:
        actors_string = str(actors[0])
    else:
        for i in range(len(actors)-1):
            actors_string += actors[i] + '; '
        actors_string += actors [-1]

    # Scrape ratings and amount of votes
    scores = dom.find('div', class_ = 'ratingValue')
    scores = scores.find('strong')
    rating = scores.text

    votes = str(scores)
    votes = votes.split()
    votes = votes[4]
    votes_string = ''
    for c in votes:
        if c.isnumeric():
            votes_string += c

    output = [title, year, runtime, genres_string, directors_string, writers_string, actors_string, rating, votes_string]
    print(output)
    # YOUR SCRAPING CODE GOES HERE:
    # Return everything of interest for this movie (all strings as specified
    # in the docstring of this function).
    return output


if __name__ == '__main__':
    main()  # call into the progam

    # If you want to test the functions you wrote, you can do that here:
    # ...
