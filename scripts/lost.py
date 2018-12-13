import urllib.request as urllib
from bs4 import BeautifulSoup
import re

#Useful to get the list of all the seasons and transcripts urls
quote_page = "https://lostpedia.fandom.com/wiki/Lost:_Destiny_Calls_transcript"
page = urllib.urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')

seasons = ["Season_1", "Season_2", "Season_3", "Season_4", "Season_5", "Season_6"]
base_url = "https://lostpedia.fandom.com"

#Print get all transcripts for the 6 seasons
num_season = 0
with open("Lost_raw.txt", "w") as text_file:
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
                        page = urllib.urlopen(quote_page)
                        soup = BeautifulSoup(page, 'html.parser')
                        start = soup.find("nav", attrs={'id': 'toc'})#.parent
                        #print(start)
                        for tr in start.find_next_siblings("p"):
                            #print(tr.get_text().strip())
                            print("Lost."+"Season"+str(num_season).zfill(2)+".Episode"+str(epi+1).zfill(2)+' '+tr.get_text().strip(), file=text_file)
            #print()

num_season = 0
with open("Lost.txt", "w") as text_file:
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