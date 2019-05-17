from requests import get  # to make GET request

import urllib.request as urllib
from bs4 import BeautifulSoup
import re

#Useful to get the list of all the seasons and transcripts urls
base_url = 'http://www.buffyworld.com/buffy/transcripts/'
episode_urls = []
for i in range(1,145): #Faire +1 pour avoir l'url du site pour vérifier sur interner On enlève l'épisode 0
    episode_urls.append(''+str(i).zfill(3)+'_tran.html')

def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = get(url)
        # write to file
        file.write(response.content)

def sub_(sentence):
    sentence = re.sub("\r", "", sentence)
    sentence = re.sub("\n", "", sentence)
    sentence = re.sub("     ", " ", sentence)
    sentence = re.sub("--", "", sentence)
    sentence = re.sub("\"", "", sentence)
    sentence = re.sub("\(\(", "{{", sentence)
    sentence = re.sub("\{\{", "", sentence)
    sentence = re.sub("\}\}", "", sentence)
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

def contents_parse(paragraph, sentences):
    is_old_br = False
    for p in paragraph.contents:
        if paragraph.name == 'p':
            contents_parse(paragraph, sentences)
        elif paragraph.name == 'br':
            is_old_br = True
        else:
            sentence = p.replace(u'\xa0', u' ')
            if is_old_br:
                sentences[-1] += sentence
            else:
                sentences.append(sentence)

def parse_sentences(sentences, epi):
    if sentences.name == 'p':
        parse_br(sentences, epi)
    else:
        if epi == 55:
            print(sentences)
            if sentences.name == 'font':
                print(sentences.text)
        else:
            if not sentences.name:
                sentence = sentences.strip()
                if sentence:
                    if epi == 51:
                        ss = sentence.split()
                        if ss[0].isupper():
                            speaker = ss[0]
                            sentence_ = sentence[len(ss[0]):].strip()
                            sentence_ = sub_(sentence_)
                            sentence_ = ' '.join(sentence_.split()).strip()
                            speaker = '_'.join(speaker.split()).strip()
                            print(speaker+' '+sentence_, file=text_file)
                    else:
                        parse_sentence_(sentence)

def parse_br(brs, epi):
    ul = brs.find('ul')
    if ul:
        br = ul.find('br')
    else:
        br = brs.find('br')
    for sentences in br.previous_siblings:
        parse_sentences(sentences, epi)
    for sentences in br.next_siblings:
        parse_sentences(sentences, epi)

def parse_sentence_(sentence, to_print=True):
    ss = sentence.split(':')
    if len(ss) < 2:
        return
    speaker = ss[0].strip()
    if len(ss) == 2:
        if len(speaker.split()) > 3:#1
            return
        sentence_ = ss[1].strip()
    if len(ss) > 2:
        sentence_ = ''
        for s in ss[1:]:
            sentence_ += s
            sentence_ += ':'
        sentence_ = sentence_[0:-1].strip()
    if sentence_:
        #re.sub('\(\(', '{{', sentence_)
        if "A demonstration, {{right/alright}}." in sentence_:
            sentence_ = "A demonstration, alright."
        sentence_ = sub_(sentence_)
        if 'Written by' in speaker or 'Directed by' in speaker or 'Transcribed by' in speaker or 'Note' in speaker:
            return
        if sentence_:
            speaker_ = sub_(speaker)
            if 'Episode begins' in speaker_ or 'Cut to' in speaker_ or 'Executive Producer' in speaker_:
                return
            if to_print:
                sentence_ = ' '.join(sentence_.split()).strip() #WE LET THE PUNCTUATION
                speaker_ = '_'.join(speaker_.split()).strip()
                print(speaker_+' '+sentence_, file=text_file)
            return [speaker_, sentence_]
    return

for epi, url_ in enumerate(episode_urls):
    url = base_url+url_
    print('epi ', epi+1)
    if epi+1 in range(1,13):
        season=1
    elif epi+1 in range(13,35):
        season=2
    elif epi+1 in range(35,57):
        season=3
    elif epi+1 in range(57,79):
        season=4
    elif epi+1 in range(79,101):
        season=5
    elif epi+1 in range(101,123):
        season=6
    elif epi+1 in range(123,145):
        season=7
    download(url, "../../Plumcot/data/BuffyTheVampireSlayer/html_pages/transcripts/season"+str(season).zfill(2)+".episode"+str(epi+1).zfill(2)+".html")
    with open("../../Plumcot/data/BuffyTheVampireSlayer/transcripts/BuffyTheVampireSlayer.Season"+str(season).zfill(2)+".Episode"+str(epi+1).zfill(2)+".temp", "w") as text_file:
        page = urllib.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        if epi < 50:
            start = soup.find("pre")#.parent
            txt = start.text
            txt = txt.split('~~~~~~~~~~ Prologue ~~~~~~~~~~')[1]
            sentences = txt.split('\n\n')
            for sentence in sentences:
                if sentence:
                    if '~~~~~~~~~~' in sentence:
                        continue
                    parse_sentence_(sentence)
        elif epi == 50:
            #.previous_siblings .next_siblings
            paragraphs = soup.find_all('p')
            for paragraph in paragraphs:
                sentence = ''
                for p in paragraph:
                    if not p.name:
                        sentence += ' '
                        sentence_s = p.split('\n')
                        #if sentence_s[1]:
                        #    print(sentence_s)
                        sentence += sentence_s[0].strip()
                    else:
                        continue
                sentence_ = sentence.strip()
                if sentence_:
                    if '---------' in sentence_:
                        continue
                    parse_sentence_(sentence_)
        elif epi in [51,52,64]:#, 55]:
            parse_br(soup, epi)
        elif epi == 55:
            print('PARSER MANUELLEMENT !')
        elif False:#epi in [60, 68, 69]:
            ul = soup.find('ul')
            sentences = ul.text
            sentences = sentences.split('\n')
            sentences = [s.strip() for s in sentences]
            sentence_old = ''
            sentences_ = []
            nb_none = 0
            for sentence in sentences:
                if sentence_old:
                    sentence_old += ' ' + sentence
                if not sentence:
                    if sentence_old:
                        sentences_.append(sentence_old)
                        nb_none = 0
                    else:
                        nb_none += 1
                    sentence_old = sentence
                if nb_none == 10:
                    break
                if not sentence_old:
                    sentence_old = sentence
            for sentence in sentences_:
                if "Girl (giggling) Noooo." in sentence:
                    sentence = "Girl: Noooo."
                parse_sentence_(sentence)
        elif epi in [60, 65, 68, 69, 72, 74, 76, 77]:
            print('PARSER MANUELLEMENT EPI 65!')
            ul = soup.find('ul')
            sentences = ul.text
            sentences = sentences.split('\n')
            sentences = [s.strip() for s in sentences]
            sentence_old = ''
            sentences_ = []
            nb_none = 0
            for sentence in sentences:
                ss = parse_sentence_(sentence, False)
                if sentence_old and not ss:
                    sentence_old += ' ' + sentence
                if not sentence or ss:
                    if sentence_old:
                        sentences_.append(sentence_old)
                        nb_none = 0
                    else:
                        nb_none += 1
                    sentence_old = sentence
                if nb_none == 10:
                    break
                if not sentence_old:
                    sentence_old = sentence
            for sentence in sentences_:
                if "Girl (giggling) Noooo." in sentence:
                    sentence = "Girl: Noooo."
                parse_sentence_(sentence)
        elif epi == 67:
            paragraphs = soup.find_all('p')
            for paragraph in paragraphs:
                sentence = paragraph.text
                if 'Disclaimer' in sentence:
                    continue
                parse_sentence_(sentence)
        elif epi in [70, 71, 82, 84]:
            print('PARSER A LA MAIN')
        elif epi in range(122,143):
            if epi == 143:
                print('PARSER A LA MAIN')
            bq = soup.find('blockquote')
            paragraphs = list(bq.find_all('p'))
            for paragraph in paragraphs[1:]:
                sentence = ''
                p_l = list(paragraph)
                if len(p_l) > 1 and p_l[0].name == 'b' and not p_l[0].text[0].isdigit():
                    for p in paragraph:
                        if p.name == 'b':
                            speaker = p.text.strip()
                            speaker = sub_(speaker)
                        if not p.name:
                            sentence = p.strip()
                            sentence = sub_(sentence)
                            if sentence and speaker:
                                if 'Cut' not in speaker and 'cut' not in speaker:
                                    sentence = ' '.join(sentence.split()).strip()
                                    speaker = '_'.join(speaker.split()).strip()
                                    print(speaker+' '+sentence, file=text_file)
        else:#if epi == 53:
            paragraphs = soup.find_all('p')
            for paragraph in paragraphs:
                for sentence in paragraph:
                    if sentence.name:
                        continue
                    sentence_ = sentence.strip()
                    if sentence_:
                        if '---------' in sentence_:
                            continue
                        parse_sentence_(sentence_)
