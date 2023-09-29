import requests
import unicodedata
from bs4 import BeautifulSoup
import pandas as pd

def get_htmlFromUrl(url):

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.46'
        }

        r = requests.get(url, headers=headers)

        print("Url : " + r.url + " > " + str(r.status_code))
        return r.content

    except:
        print("An exception occurred")
        return None    


def get_soupFromHtml(html):

    soup = BeautifulSoup(html, 'html.parser')

    return soup


def clean_response(response):
    if type(response) == list:
        return response
    response = unicodedata.normalize("NFKD", response)
    response = response.replace('\t', ' ')
    response = response.replace('\r', ' ')
    response = response.replace('\n', ' ')
    response = response.replace('  ', ' ')

    return response

def get_text(soup):
    lines = []

    for line in soup.find_all('p'):
        lines.append(line.get_text())

    # loop over all h1-h6 tags
    for position in range(1, 7):
        for line in soup.find_all('h' + str(position)):
            lines.append(line.get_text())

    return lines

def get_iframeSrc(soup):
    iframe_src = []

    for iframe in soup.find_all('iframe'):
        iframe_src.append(iframe.get('src'))

    return iframe_src

def get_allLinks(soup):
    links = []

    for link in soup.find_all('a'):
        links.append(link.get('href'))

    return links

def get_tableFromSoup(soup):
    tables = soup.find_all('table')

    pd_tables = []
    for table in tables:
        pd_tables.append(pd.read_html(str(table)))

    return pd_tables