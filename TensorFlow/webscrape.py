from bs4 import BeautifulSoup as bs
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
    # TODO add command line arguments
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
