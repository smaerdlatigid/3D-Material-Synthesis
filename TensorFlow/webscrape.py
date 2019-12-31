from bs4 import BeautifulSoup as bs
import argparse
import requests

def ignore(string):
    ignored = [".png", ".jpg", ".jpeg", ".js", ".css", ".zip", "xml", "json"]
    for i in ignored:
        if i in string:
            return True
    return False

def find_links(URL, PATTERN="https://drive"):
    # TODO optimize for minimal querying
    r = requests.get(URL)
    soup = bs(r.content, 'lxml')
    urls = []
    for item in soup.select('[href^="{}"], [src^="{}"]'.format(PATTERN, PATTERN)):
        if item.get('href') is not None:  
            if not ignore(item['href']):
                urls.append(item['href'])
        else:
            if not ignore(item['src']):
                urls.append(item['src'])
    return list(set(urls))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    help_ = "Load h5 model trained weights"
    parser.add_argument("-d", "--weights", help=help_, default="encoder.h5")
    help_ = "Number of training epochs"
    parser.add_argument("-bu", "--epochs", help=help_, default=10 ,type=int)
    help_ = "Pickle file of training samples"
    parser.add_argument("-p", "--train", help=help_)
    help_ = "Pickle file of test samples"
    parser.add_argument("-f", "--test", help=help_)
    args = parser.parse_args()

    BASE_URL = "https://3dtextures.me/"
    DEPTH_LIMIT = 3
    PATTERN = "https://drive"
    # OUTPUT FILE

    # DEPTH = 0
    all_links = []
    download_links = []

    links = find_links(BASE_URL, BASE_URL)
    all_links.extend(links)
    for d in range(DEPTH_LIMIT):

        newlinks = []
        for l in range(len(links)):
            print(links[l])

            # search links for downloads
            drive_links = find_links(links[l], PATTERN="https://drive")
            download_links.extend(drive_links) # take unique values later

            # search for new links
            depth_links = find_links(links[l], PATTERN=BASE_URL)
            for j in range(len(depth_links)): 
                if depth_links[j] not in all_links:
                    newlinks.append(depth_links[j])
                    all_links.append(depth_links[j])
            # print("new links: {}".format(len(newlinks)))

        links = list(set(newlinks))

    with open('download_links.txt', 'w') as fh:
        for link in set(download_links):
            fh.write("{}\n".format(link))
