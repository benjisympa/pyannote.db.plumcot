from requests import get  # to make GET request

import urllib.request as urllib
from bs4 import BeautifulSoup
import re

#Useful to get the list of all the seasons and transcripts urls
episode_urls = ["https://transcripts.fandom.com/wiki/Harry_Potter_and_the_Philosopher%27s_Stone",
               "https://transcripts.fandom.com/wiki/Harry_Potter_and_the_Chamber_of_Secrets"]

def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = get(url)
        # write to file
        file.write(response.content)

def sub_(sentence, epi):
    if epi == 1:
        sentence = re.sub(":", "", sentence)
    sentence = re.sub("\(.*?\) ", "", sentence)
    sentence = re.sub(" \(.*?\)", "", sentence)
    sentence = re.sub("\(.*?\)", "", sentence)
    sentence = re.sub("\[.*?\] ", "", sentence)
    sentence = re.sub(" \[.*?\]", "", sentence)
    sentence = re.sub("\[.*?\]", "", sentence)
    sentence = re.sub('\{.*?\} ', '', sentence)
    sentence = re.sub(' \{.*?\}', '', sentence)
    sentence = re.sub('\{.*?\}', '', sentence)
    sentence = sentence.strip()
    return sentence

def parse_sentence(to_iterate):
    epi = 1
    speaker = ''
    sentence = ''
    for sentence_ in to_iterate:
        #print(sentence_)
        if sentence_.name == 'u':
            continue
        elif sentence_.name == 'br':
            if speaker and sentence and 'scene' not in speaker.lower() and 'location' not in speaker.lower():
                sentence = sub_(sentence, epi)
                speaker = re.sub(" ", "_", speaker)
                #print('a', speaker, '999', sentence)
                print(speaker+' '+sentence, file=text_file)
            elif not speaker and sentence:
                ss = sentence.split(':')
                if ss[0].isupper() and 'scene' not in ss[0].lower() and 'location' not in ss[0].lower():
                    speaker = ss[0]
                    sentence = ':'.join(ss[1:])
                    sentence = sub_(sentence, epi)
                    speaker = re.sub(" ", "_", speaker)
                    #print('b', speaker, '999', sentence)
                    print(speaker+' '+sentence, file=text_file)
            speaker = ''
            sentence = ''
        elif sentence_.name == 'b':
            speaker = sentence_.text.strip()
            #print('speaker', speaker)
        elif not sentence_.name: #to avoid italic
            sentence += sentence_.strip()
            #print('sentence', sentence_)
    if speaker and sentence and 'scene' not in speaker.lower() and 'location' not in speaker.lower():
        sentence = sub_(sentence, epi)
        speaker = re.sub(" ", "_", speaker)
        #print('c', speaker, '999', sentence)
        print(speaker+' '+sentence, file=text_file)
    elif not speaker and sentence:
        ss = sentence.split(':')
        if ss[0].isupper() and 'scene' not in ss[0].lower() and 'location' not in ss[0].lower():
            speaker = ss[0]
            sentence = ':'.join(ss[1:])
            sentence = sub_(sentence, epi)
            speaker = re.sub(" ", "_", speaker)
            #print('d', speaker, '999', sentence)
            print(speaker+' '+sentence, file=text_file)

print('début')
deb = 0
num_season = 1
for epi, url in enumerate(episode_urls):
    if epi < deb:
        continue
    download(url, "../../Plumcot/data/HarryPotter/html_pages/transcripts/season.01.episode"+str(epi+1).zfill(2)+".html")
    page = urllib.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    start = soup.find("div", attrs={'id': 'mw-content-text'})#.parent
    #print(start)
    if epi == 0:
        with open("../../Plumcot/data/HarryPotter/transcripts/HarryPotter.Season"+str(num_season).zfill(2)+".Episode"+str(epi+1).zfill(2)+".temp", "w") as text_file:
            for tr in start.find_all('p'):
                #print(tr.get_text().strip())
                text = tr.get_text().strip()
                text = sub_(text, 0)
                if text == '':
                    continue
                if text[0] == '(':
                    continue
                #print(text)
                if text == 'Welcome, Harry, to Diagon Alley.':
                    text = 'Hagrid: Welcome, Harry, to Diagon Alley.'
                if text == "Ain't no one gonna get past Fluffy. Hehe, not a soul knows how. Except for me and Dumbledore. I shouldn't have told you that. I shouldn't have told you that. Oh! Ooh! Ooh! Ooh! Ooh!":
                    text = "Hagrid: Ain't no one gonna get past Fluffy. Hehe, not a soul knows how. Except for me and Dumbledore. I shouldn't have told you that. I shouldn't have told you that. Oh! Ooh! Ooh! Ooh! Ooh!"
                if text == "Dumbledore! As long as Dumbledore's around, you're safe. As long as Dumbledore's around, you can't be touched.":
                    text = "Hermione: Dumbledore! As long as Dumbledore's around, you're safe. As long as Dumbledore's around, you can't be touched."
                ss = text.split(':')
                if len(ss) < 2:
                    #print(num_season, epi+1, ss)
                    continue
                #print(ss)
                #print('&&&&&&&')
                speaker = ss[0].strip()
                sentence = ss[1].strip()
                speaker = re.sub(" ", "_", speaker)
                #speaker = speaker.translate(str.maketrans('', '', '!"\'()*+,-./:;<=>?[\\]^_`{|}~'))
                print(speaker+' '+sentence, file=text_file)
    if epi == 1:
        with open("../../Plumcot/data/HarryPotter/transcripts/HarryPotter.Season"+str(num_season).zfill(2)+".Episode"+str(epi+1).zfill(2)+".temp", "w") as text_file:
            for paragraph in start.find_all('p'):
                #print(paragraph.name, paragraph.text.strip())
                br = paragraph.find('br')
                if not br:
                    parse_sentence(paragraph)
                else:
                    parse_sentence(br.previous_siblings)
                    #print(br.previous_siblings, br.next_siblings)
                    #print('*********')
                    parse_sentence(br.next_siblings)
                #print('88888888888')
