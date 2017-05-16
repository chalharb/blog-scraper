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


def create_files(all_articles, output_dir):
    article_titles = np.array(all_articles).ravel()  # Converts 2d to 1d array
    print(len(article_titles))

    for file_name in article_titles:
        # Open a file
        fd = os.open(output_dir + "/" + file_name, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
        # Write one string
        os.write(fd, file_name.encode())
        # Close opened file
        os.close(fd)


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

    # check if directory exists
    try:
        create_directory(output_dir)
    except Exception as e:
        print(bcolors.FAIL + "Directory Already Exists!" + bcolors.ENDC)

    while True:
        try:
            built_url = url + str(page_start)
            data = get_data(built_url)
            url_title = []

            soup = BeautifulSoup(data, 'html.parser')
            print(built_url)
            entry_count = len(soup.select('.entry-title'))

            print(bcolors.OKBLUE + 'Number of entries on this page {}...'.format(entry_count) + bcolors.ENDC)

            for article in soup.select('.entry-title'):
                # Sanitizes for filename creation
                url_title.append(article.text.replace(u'\xa0', u' ').replace(" ", "-").replace("’", ""))

            all_articles.append(url_title)

        except Exception as e:
            print(bcolors.FAIL + "\nNo page found. We're probably done. Aborting." + bcolors.ENDC)
            break

        page_start += 1

    create_files(all_articles, output_dir)
    # all_articles_count = len(all_articles)
    # print("\nTotal number of articles gathered: %d" % all_articles_count)
    # print(all_articles)

if __name__ == '__main__': main()
