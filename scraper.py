###################
# Web Scraper
# v.0.0.1
# Logan Harber
##################

import requests
from bs4 import BeautifulSoup

url = "https://medicalcitychildrenshospitalurgentcareblog.wordpress.com/page/"
pageCount = 10
full_html = []

# Pings url duh.
def pingPage(url):
    # Requires http or https
    response = requests.get(url)

    data = response.text

    return data


def build_url(url, pageCount):
    pageCountToString = str(pageCount)
    new_url = url + pageCountToString
    return new_url


for i in range(pageCount):
    i += 1

    builtURL = build_url(url, i)  # new url for each page
    print builtURL
    data = pingPage(builtURL)

    soup = BeautifulSoup(data, 'html.parser')
    print(soup.find_all("article"))


print full_html
print len(full_html)
