###################
# Web Scraper
# v.0.0.1
# Logan Harber
##################

import os
import requests
from bs4 import BeautifulSoup

# Pings url duh.
def pingPage(url):
    # Requires http or https
    response = requests.get(url)
    response.raise_for_status()

    data = response.text

    return data


def build_url(url, pageCount):
    new_url = url + str(pageCount)
    return new_url


def createDirectory(output_dir):
    desired_permission = 0o777
    try:
        original_umask = os.umask(0)
        os.makedirs(output_dir, desired_permission)
    finally:
        os.umask(original_umask)


def main():
    url = "https://medicalcitychildrenshospitalurgentcareblog.wordpress.com/page/"
    page_start = 1
    output_dir = "output-files"

    # check if directory exists
    if os.path.isdir(output_dir):
        print("Output directory already exists!")
    else:
        print("Creating Output Directory...")
        createDirectory(output_dir)

    while True:
        try:
            built_url = build_url(url, page_start)  # new url for each page
            print(built_url)
            data = pingPage(built_url)

            soup = BeautifulSoup(data, 'html.parser')
            print(soup.find_all("article"))
        except Exception as e:
            print("No page found. We're probably done. Aborting.")
            break

        page_start += 1

if  __name__ =='__main__':main()