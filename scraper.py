###################
# Web Scraper
# v.1.0
# Logan Harber
##################

import requests
import os
import numpy as np
from bs4 import BeautifulSoup
import urllib.request
import ssl


# Returns generated URL with page number
def generate_url(url, page_number):
    return url + str(page_number)


# Return response text of URL
def get_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


# Converts title to URL Title
def convert_to_url_title(article):
    return article.text.replace(u'\xa0', u' ').replace(" ", "-").replace("’", "")


# Creates a directory to store the output files
def create_directory(output_dir):
    desired_permission = 0o700  # r+w only

    if os.path.isdir(output_dir):
        raise Exception('An error has occurred')
    else:
        print("Attempting to create output directory...")
        try:
            original_umask = os.umask(0)
            os.makedirs(output_dir, desired_permission)
            print("Output directory created successfully!")
        finally:
            os.umask(original_umask)


# Creates files with html content in the output directory
def create_files(article_titles, article_contents, output_path):
    article_titles = np.array(article_titles).ravel()
    article_contents = np.array(article_contents).ravel()

    if len(article_titles) == len(article_contents):
        # combines 2 arrarys into a dictionary
        combined_articles = dict(zip(article_titles, article_contents))

        for [title, content] in combined_articles.items():
            fd = os.open(output_path + "/" + title, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
            os.write(fd, content.encode())
            os.close(fd)
    else:
        print('Was unable to scrape the blog correctly. Try again!')


def get_all_images(all_images, output_path):
    ctx = fake_ssl()

    for image in all_images:
        resource = urllib.request.urlopen(image, context=ctx)

        filename = os.path.basename(image)
        sep = '?'  # Removes evertying after file extension that wordpress adds
        filename = filename.split(sep, 1)[0]

        print("Downloading {}".format(filename))
        output = open(output_path + "/" + filename, "wb")
        output.write(resource.read())
        output.close()


# Fakes ssl cert to be able to get images
def fake_ssl():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


# main function
def main():
    url = "https://medicalcitychildrenshospitalurgentcareblog.wordpress.com/page/"
    page_start = 1
    output_dir = "files"
    images_dir = "images"
    image_extension = ''
    all_articles_titles = []
    all_articles_content = []
    all_images = []
    # check if directory exists if not creates it
    try:
        create_directory(output_dir)
    except Exception as e:
        print("CONSOLE: File Directory Already Exists!")

    try:
        create_directory(images_dir)
    except Exception as e:
        print("CONSOLE: Images Directory Already Exists!")

    # Crawls pages and stores data
    while True:
        try:
            page_url = generate_url(url, page_start)
            data = get_data(page_url)
            soup = BeautifulSoup(data, 'html.parser')
            print(page_url)

            # Stores all Titles
            for title in soup.select('.entry-title'):
                all_articles_titles.append(convert_to_url_title(title))

            # Stores all Content
            for content in soup.select('.entry-content'):
                all_articles_content.append(content)

            # Stores all images
            for image in soup.select('.entry-content img'):
                all_images.append(image['src'])

        except Exception as e:
            print("\nNo more pages found...")
            break

        page_start += 1

    create_files(all_articles_titles, all_articles_content, output_dir)
    get_all_images(all_images, images_dir)

    print("\nTotal Articles Scraped: {}".format(len(all_articles_titles)))


if __name__ == '__main__': main()