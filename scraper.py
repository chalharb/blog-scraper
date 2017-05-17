###################
# Web Scraper
# v.0.0.1
# Logan Harber
##################

import os
import requests
import numpy as np

from bs4 import BeautifulSoup


#############
# FUNCTIONS
#############

# Goes to page and returns the data object
def get_data(url):
    response = requests.get(url)
    response.raise_for_status()
    data = response.text

    return data


# Creates a directory to store the output files
def create_directory(output_dir):
    desired_permission = 0o700  # r+w only

    if os.path.isdir(output_dir):
        raise Exception('An error has occurred')
    else:
        print(bcolors.WARNING + "Attempting to create output directory..." + bcolors.ENDC)
        try:
            original_umask = os.umask(0)
            os.makedirs(output_dir, desired_permission)
            print(bcolors.OKGREEN + "Output directory created successfully!" + bcolors.ENDC)
        finally:
            os.umask(original_umask)


def create_files(all_articles, all_articles_content, output_dir):
    all_articles = np.array(all_articles).ravel()
    all_articles_content = np.array(all_articles_content).ravel()

    if len(all_articles) == len(all_articles_content):
        # combines 2 arrarys into a dictionary
        combined_articles = dict(zip(all_articles, all_articles_content))

        for title, content in combined_articles.items():
            fd = os.open(output_dir + "/" + title, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
            os.write(fd, content.encode())
            os.close(fd)
    else:
        print('Was unable to scrape the blog correctly. Try again!')


# colors for console output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# main function
def main():
    url = "https://medicalcitychildrenshospitalurgentcareblog.wordpress.com/page/"
    page_start = 1
    output_dir = "output-files"
    all_articles = []
    all_articles_content = []

    # check if directory exists
    try:
        create_directory(output_dir)
    except Exception as e:
        print(bcolors.FAIL + "Directory Already Exists!" + bcolors.ENDC)

    while True:
        try:
            built_url = url + str(page_start)
            data = get_data(built_url)
            file_names = []
            file_contents = []

            soup = BeautifulSoup(data, 'html.parser')
            print(built_url)

            # builds file names and sanitizes for file name
            for article in soup.select('.entry-title'):
                file_names.append(article.text.replace(u'\xa0', u' ').replace(" ", "-").replace("’", ""))

            # builds content for files
            for content in soup.select('.entry-content'):
                file_contents.append(content)

            # Append to global vars
            all_articles.append(file_names)
            all_articles_content.append(file_contents)

        except Exception as e:
            print(bcolors.FAIL + "\nNo page found. We're probably done. Aborting." + bcolors.ENDC)
            break

        page_start += 1

    create_files(all_articles, all_articles_content, output_dir)
    # TODO: GET ALL IMAGES (.entry-content > img)

if __name__ == '__main__': main()
