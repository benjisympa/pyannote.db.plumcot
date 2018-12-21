import urllib.request as urllib
from bs4 import BeautifulSoup
import re
from requests import get # to make GET request

def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = get(url)
        # write to file
        file.write(response.content)

#Useful to get the list of all the seasons and transcripts urls
quote_page = "https://lostpedia.fandom.com/wiki/Lost:_Destiny_Calls_transcript"
page = urllib.urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')

seasons = ["Season_1", "Season_2", "Season_3", "Season_4", "Season_5", "Season_6"]
base_url = "https://lostpedia.fandom.com"

#Print get all transcripts for the 6 seasons
num_season = 0
with open("data/Lost/transcripts.txt", "w") as text_file:
    div = soup.find("div", attrs={'id': 'mw-content-text'})
    start = div.find_all("td")
    for s in start:
        season = s.find("a")
        if season and season["href"].split('/')[-1] in seasons:
            #print(season["href"])
            num_season += 1
            for s_ in s.find_next_siblings("td"):
                for s_d in s_.find_all("div"):
                    urls = s_d.find_all("a")
                    for epi, url in enumerate(urls):
                        #print(url['href'])

                        quote_page = base_url+url['href']
                        download(quote_page, "data/Lost/html_pages/transcripts/season"+str(num_season).zfill(2)+".episode"+str(epi+1).zfill(2)+".html")
                        page = urllib.urlopen(quote_page)
                        soup = BeautifulSoup(page, 'html.parser')
                        start = soup.find("nav", attrs={'id': 'toc'})#.parent
                        #print(start)
                        for tr in start.find_next_siblings("p"):
                            #print(tr.get_text().strip())
                            text = tr.get_text().strip()
                            text = re.sub('\[.*?\]', '', text)
                            if text == '':
                                continue
                            #print(text)
                            print("Lost."+"Season"+str(num_season).zfill(2)+".Episode"+str(epi+1).zfill(2)+' '+text, file=text_file)
            #print()
