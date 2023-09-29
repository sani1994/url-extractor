import os
import sys
import time
from datetime import datetime
from googlesearch import search
from itertools import product
import requests
from bs4 import BeautifulSoup
import pandas as pd


def google_search(query: str, num_results: int = 20) -> str:
    """
    :param query: string or text to search in google
    :param num_results:The number of results you are looking for
    :return: google sea
    """
    base_url = "https://www.google.com/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    }

    params = {
        "q": query,
        "num": num_results,
    }

    # Set the number of retries and retry delay
    max_retries = 5
    retry_delay = 5  # in seconds

    for retry in range(max_retries):
        try:
            response = requests.get(base_url, params=params, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.text
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print(f"Received 429 error. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print(f"HTTP error: {e}")
                break
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            break

    return None


def get_url(query, num):
    html = google_search(query, num)
    soup = BeautifulSoup(html, 'html.parser')
    search_results = []
    for result in soup.find_all('div', class_='tF2Cxc'):
        link = result.find('a')
        if link:
            url = link.get('href')
            search_results.append(url)

    return search_results[:num]


def perform_google_search(query, num_results=20, stop=20, sleep_time=2):
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    try:
        results = list(search(query, num=num_results, user_agent=user_agent, stop=stop))
        return results
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("No arguments passed.Please pass an xls file as an argument. ex: python url_extractor path//test.xls")
        exit()

    dir_path = os.path.dirname(__file__)
    urls = []
    combination_dir_path = f"{dir_path}/combination_output"
    if not os.path.exists(combination_dir_path):
        os.mkdir(combination_dir_path)
    file_path = f"{dir_path}/{sys.argv[1]}"
    combination_list = []
    df = pd.read_excel(file_path, header=None)
    columns = (df[column_name] for column_name in df.columns)
    combinations = product(*columns)
    combinations_df = pd.DataFrame(combinations, columns=df.columns).dropna()
    max_attempts = 5
    url_file = open(dir_path + '/google_urls.txt', 'w')
    with open(combination_dir_path + "/combinations_" + datetime.now().strftime("%H_%M_%S") + ".txt", "w") as file:
        for values in combinations_df.itertuples():
            text = " ".join(values[1:])
            file.write(f"{text}\n")
            print(f"Looking search result for keyword: {text}")
            urls = get_url(text, 20)
            for item in urls:
                url_file.write(item + "\n")
    url_file.close()
    print(f"Google search url file path: {dir_path}/google_urls.txt")
