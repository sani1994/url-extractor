import sys
import os
import requests
import tldextract
import functions
from datetime import datetime
import pandas as pd


def extract_Data(url, filename='output.xlsx', top_level=False):
    try:
        htmlResponse = functions.get_htmlFromUrl(url)
        all_tables = []
        all_lines_df = []
        links_for_all_archs = []
        all_iframe_src = []
        if (htmlResponse):
            browser = functions.get_soupFromHtml(htmlResponse)
            all_iframe_src = functions.get_iframeSrc(browser)
            index = 1
            if top_level:
                links_for_all_archs += functions.get_allLinks(browser)
                for url_to_check in links_for_all_archs:
                    ++index
                    if ("https://" in url_to_check):
                        print("Got A Perfect Url")
                    else:
                        SAM_domain = tldextract.extract(url)
                        url_to_check = SAM_domain.domain + "." + SAM_domain.suffix + "/" + url_to_check[1:]

                        url_to_check = "https://" + url_to_check
                        print(url_to_check)

                    if (('.pdf' in url_to_check) | ('.PDF' in url_to_check)):

                        print("Downloading PDF file: ", url_to_check)

                        response = requests.get(url_to_check)
                        new_filename = url_to_check.replace("/", "-").replace(":", "-")
                        pdf = open(output_folder + "/pdf-" + new_filename + str(index) + ".pdf", 'wb')
                        pdf.write(response.content)
                        pdf.close()
                        print("File ", index, " downloaded")

                    else:
                        all_iframe_src += links_for_all_archs

            all_lines = functions.get_text(browser)
            all_lines_df = pd.DataFrame(all_lines)
            all_tables = functions.get_tableFromSoup(browser)
        save_output(all_lines_df, all_tables, filename)
        return all_iframe_src
    except:
        print("An exception occurred extract_Data")
        return []


def save_output(all_lines_df, all_tables, filename='output.xlsx'):
    try:
        with pd.ExcelWriter(filename
                            ) as writer:
            all_lines_df.to_excel(writer, sheet_name='Paragraphs')
            index = 0
            for table in all_tables:
                index += 1
                for df in table:
                    df.to_excel(writer, sheet_name='Tables' + str(index))
    except:
        print("An exception Save Output")


def run_extraction(url, output_folder):
    name = url.replace("https://", "").replace("http://", "").replace("/", "-").replace(":", "-")
    all_iframe_src = extract_Data(url, output_folder + "/" + name + ".xlsx", True)
    domain = tldextract.extract(url).domain
    try:
        index = 0
        for iframe_src in all_iframe_src:
            index = index + 1
            if "googletagmanager" in iframe_src:
                print("googletagmanager")
            elif "youtube" in iframe_src:
                print("youtube")
            elif "vimeo" in iframe_src:
                print("vimeo")
            else:
                if domain in iframe_src:
                    extract_Data(iframe_src, output_folder + '/output-' + str(name) + str(index) + '.xlsx', False)
    except:
        print("An exception Extration")


# run main function
if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("No arguments passed; URL is required, eg. python main.py https://www.google.com")
        exit()

    urls = [""]

    output_folder = "output" + datetime.today().strftime("%d%m%Y") + datetime.now().strftime("%H%M%S")
    os.mkdir(output_folder)

    with open(sys.argv[1]) as file:
        lines = [line.rstrip() for line in file]
        urls += lines
        for line in lines:
            run_extraction(line, output_folder)

    file = open(output_folder + '/input.txt', 'w')
    for item in urls:
        file.write(item + "\n")
    file.close()
