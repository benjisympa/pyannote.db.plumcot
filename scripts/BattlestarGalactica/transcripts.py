import urllib.request as urllib
from bs4 import BeautifulSoup
import re
from requests import get  # to make GET request
from urllib.request import Request, urlopen

#Useful to get the list of all the seasons and transcripts urls
quote_page = "https://bsg.hypnoweb.net/battlestar-galactica/les-episodes.124.2/"
#page = urllib.urlopen(quote_page)
req = Request(quote_page, headers={'User-Agent': 'Mozilla/5.0'})
page = urlopen(req).read()
soup = BeautifulSoup(page, 'html.parser')

seasons_id = ["f298s1", "f298s2", "f298s3", "f298s4"]
base_url = "https://bsg.hypnoweb.net"

divs = []
for id_ in seasons_id:
    divs.append(soup.find("div", attrs={'id': id_}))

def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = get(url)
        # write to file
        file.write(response.content)

def cas_particulier(sentence):
    if "Starbuck. Yes, sir." in sentence:
        sentence = "Starbuck: Yes, sir."
    if "– " in sentence:
        sentence = re.sub('–','-',sentence)
    if "The Cylon bomber. Do you think that he was trying to blow up your project," in sentence:
        sentence = "The Cylon bomber - Do you think that he was trying to blow up your project ?"
    if "#6 (in his head) You're a hero. You're even more popular and powerful than ever before. You've had your trial by fire, so now they truly believe in you. Hard for anyone to accuse you of treason again." in sentence:
        sentence = "#6 - You're a hero. You're even more popular and powerful than ever before. You've had your trial by fire, so now they truly believe in you. Hard for anyone to accuse you of treason again."
    if sentence == 'Credits':
        sentence = ''
    if 'Gaeta: (on P.A.) Attention, Colonial one will arrive in 30 minutes. Repeat: Colonial one will arrive in 30 minutes.' in sentence:
        sentence : 'Gaeta: (on P.A.) Attention, Colonial one will arrive in 30 minutes. Colonial one will arrive in 30 minutes.'
    if 'Kelly: Colonel, the toasters have knocked out our CO. This has gotta be part of a bigger plan. I recommend we execute jump' in sentence:
        sentence = 'Kelly: Colonel, the toasters have knocked out our CO. This has gotta be part of a bigger plan. I recommend we execute jump to urgency standby coordinates.'
    if "Roslin: We have got to jump back. We can't stay here. Lieutenant thrace won't be able to find us o­nce she retrieves the arrow" in sentence:
        sentence = "Roslin: We have got to jump back. We can't stay here. Lieutenant thrace won't be able to find us o­nce she retrieves the arrow from caprica."
    if "Strabuck: What do you want from me, Helo? She's a Cylon. You've been had. We've been had. So what, I'm just supposed to be" in sentence:
        sentence = "Strabuck: What do you want from me, Helo? She's a Cylon. You've been had. We've been had. So what, I'm just supposed to be nice to her? Because she says she's pregnant? Get out of the way."
    if "Tyrol: Cally, there. There.  I know you're hit, buddy. It's okay, I'm gonna check you right now. I'm gonna put him here, Cal" in sentence:
        sentence = "Tyrol: Cally, there. There.  I know you're hit, buddy. It's okay, I'm gonna check you right now. I'm gonna put him here, Cally. Here, stay down. Be with me right here.  Okay, I'm gonna check you right now. It's not that bad, it's not that bad. It's not that bad. Cally, check the ridge."
    if "Apollo: All right? You have my parole. When I'm on duty, I'll make no attempt to free her or sow insurrection among the crew." in sentence:
        sentence = "Apollo: All right? You have my parole. When I'm on duty, I'll make no attempt to free her or sow insurrection among the crew. And when I'm not o­n duty, I'll report directly back to this cell."
    if "Guard: (to Roslin)  Will you pray with me? Help us, lords of kobol. Help your prophet Laura guide us to the path of righteousness. That we might--   that we might destroy our enemies. Let us walk the path of righteousness and lift our faces unto your goodness. Help us turn away from the calls of the wicked and show us the knowledge of your certain salvation. We offer this" in sentence :
        sentence = "Guard: (to Roslin)  Will you pray with me? Help us, lords of kobol. Help your prophet Laura guide us to the path of righteousness. That we might--   that we might destroy our enemies. Let us walk the path of righteousness and lift our faces unto your goodness. Help us turn away from the calls of the wicked and show us the knowledge of your certain salvation. We offer this prayer."
    if "Apollo: You're in charge of getting her down to sickbay. Take Bonnington as escort. Remember, just head away from the sound" in sentence:
        sentence = "Apollo: You're in charge of getting her down to sickbay. Take Bonnington as escort. Remember, just head away from the sound of gunfire."
    if "Starbuck and Helo are standing outside her apartment, She doesn't have her keys so she shoots the lock and kick the door" in sentence:
        sentence = "Starbuck and Helo are standing outside her apartment, She doesn't have her keys so she shoots the lock and kick the door open."
    if "Starbuck; My gods what are they doing?" in sentence:
        sentence = "Starbuck: My gods what are they doing?"
    if 'Tyrol" Nice to be small, huh? Ship\'s got more than one engine. Get to it.' in sentence:
        sentence = "Tyrol: Nice to be small, huh? Ship's got more than one engine. Get to it."
    if "TighWhat?" in sentence:
        sentence = "Tigh: What?"
    if "Tigh; I think there's part of you that looks into that thing's eyes and still sees that young girl that reported aboard two years ago as a rook pilot. Well, it's not. It never was. Bill, it's a machine." in sentence:
        sentence = "Tigh: I think there's part of you that looks into that thing's eyes and still sees that young girl that reported aboard two years ago as a rook pilot. Well, it's not. It never was. Bill, it's a machine."
    #S2E17
    #Base ship's turning away. He's--he's frakkin' running, Major!
    #I'm at the manifold. I'm gonna see if I can turn them. Yes! There's definitely air escaping. Through a crack, over. SVC relay. The breach is behind that.
    if "Kat: Can the chatter, Snowbirds! This is the CAG. Abort maneuver. I say again, decoy squadron," in sentence:
        sentence = "Kat: Can the chatter, Snowbirds! This is the CAG. Abort maneuver. I say again, decoy squadron, abort maneuver."
    if "Chief: I think we should call off the strike. There's no reason to go forward with it if the Galactica's" in sentence:
        sentence = "Chief: I think we should call off the strike. There's no reason to go forward with it if the Galactica's gonna come back."
    #S3E2
    #Come o n.
    #Let's go.
    #S3E3
    #It's on.
    if "Adama: Yeah... it's me. (" in sentence:
        sentence = "Adama: Yeah... it's me. Welcome home, Bulldog."
    if "Adama: The attacks on the Colonies. By crossing the line, I showed them that we were the warmongers they figured us to be. [" in sentence:
        sentence = "Adama: The attacks on the Colonies. By crossing the line, I showed them that we were the warmongers they figured us to be. And I left them but one choice. To attack us before we attacked them."
    #S4E1
    #Twelve Cylon models. Seven are known.
    #Four live in secret.
    #One will be revealed.
    return sentence

def sub_(sentence_):
    sentence_ = re.sub("\(.*?\) ", "", sentence_)
    sentence_ = re.sub(" \(.*?\)", "", sentence_)
    sentence_ = re.sub("\(.*?\)", "", sentence_)
    sentence_ = re.sub("\[.*?\] ", "", sentence_)
    sentence_ = re.sub(" \[.*?\]", "", sentence_)
    sentence_ = re.sub("\[.*?\]", "", sentence_)
    sentence_ = sentence_.strip()
    return sentence_

def split_(sentence_, carac=':'):
    all_ = sentence_.split(carac)
    speaker = ''
    sentence = ''
    if len(all_) >= 2:#>=
        res = sentence_.split(carac, 1)
        #print(res)
        speaker = res[0].strip()
        sentence = res[1].strip()
    #else:#bad sentence (location, ...)
    #    print(sentence_)
    return speaker, sentence

def parse_sentence(sentence, season, epi, speaker_old=''):
    speaker = ''
    sentence_ = ''
    if season == 1 and epi == 8:
        if sentence.name and sentence.name == 'strong':
            speaker = sentence.string
            speaker = speaker.strip()
            #print(speaker)
            return speaker
        if not sentence.name:
            sentence_ = cas_particulier(sentence)
            if '---' in sentence_:
                sentence_ = ''
            speaker = speaker_old
            sentence_ = sub_(sentence_)
            #if sentence_:
            #    print(sentence_)
    elif (isinstance(sentence, str) or not sentence.name) and sentence and sentence[0] != '(':
        sentence_ = cas_particulier(sentence)
        sentence_ = sub_(sentence_)
        if season == 1 and epi in [1,2,3,4,5,10,11,12,13]:
            speaker, sentence_ = split_(sentence_)
        if season == 1 and epi in [6,7,9]:
            speaker, sentence_ = split_(sentence_, carac='-')
        if season == 2 and epi in [1,2,3]:
            speaker, sentence_ = split_(sentence_)
        if season == 2 and epi in [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,20]: #=
            speaker, sentence_ = split_(sentence_)
        if season == 2 and epi in [19]: #=
            speaker, sentence_ = split_(sentence_)
        if season == 3 and epi in [1,2,3,8]:
            speaker, sentence_ = split_(sentence_)
        if season == 3 and epi in [4,5,6,7,9,10,11,12,13,14,15,16,17,18,19,20]: #.string, if not .name
            speaker, sentence_ = split_(sentence_)
        if season == 4 and epi in [1,2,3,4,5,6,7,8,9]: #=
            speaker, sentence_ = split_(sentence_)
        #if print_:
        #    print(sentence_)
        #    if res[1] == '':
        #        continue
        #    print(res[0].strip(), res[1].strip())
    if speaker and sentence_:
        speaker = speaker.translate(str.maketrans('', '', '!"\'()*+,-./:;<=>?[\\]^_`{|}~­'))
        sentence_ = sentence_.translate(str.maketrans('', '', '­='))
        sentence_ = sentence_.replace('\xad', '')
        sentence_ = sentence_.replace('\u00ad', '')
        sentence_ = sentence_.replace('\"', '')
        sentence_ = sentence_.replace('\'', '')
        speaker = speaker.replace(' ','_')
        speaker = speaker.strip()
        sentence_ = sentence_.strip()
        if speaker.isupper() and sentence_.isupper():
            return
        #print(speaker, sentence_)
        print(speaker+' '+sentence_, file=text_file)
        if season == 3 and epi == 5 and speaker == 'Three' and sentence == 'Evacuate the entire facility. ...You should go as well, Gaius. There\'s a place for you too.':
            print('Man Walk!', file=text_file)
    return

def parse_sentences(brs, season, epi):
    #Particular cases
    if season == 2:
        if epi == 19:
            for br in brs:
                if br.contents:
                    for txt in br.contents:
                        if '===' not in txt.text:
                            parse_sentence(txt.text, season, epi)
            return
        elif epi >= 4: #4
            if epi == 6:
                print('Dualla 18,000 souls aboard the 24 ships that joined President roslin\'s rebellion, sir.', file=text_file)
                print('Tigh That\'s over a third of the people in the fleet.', file=text_file)
                print('Adama Give me a breakdown. What have we lost?', file=text_file)
                print('Dualla Uh, 9,500 souls from Gemenon. 6,250 from Caprica.', file=text_file)
            for br in brs:
                if br.contents:
                    if epi == 6 and br.contents[0].name != 'br' and br.contents[0].name != 'strong':
                        parse_sentence(br.text, season, epi)
                    elif br.contents[0].name == 'strong':
                        #print(br.contents[0].string.strip(), br.contents[1].strip())
                        parse_sentence(br.text, season, epi)
                    #children = br.findChildren("strong" , recursive=False)
                    #for child in children:
                    #    print(child)
            return
    if season == 3:
        if epi ==4 and epi != 8:
            for br in brs:
                if br.contents:
                    if br.contents[0].name == 'strong':
                        parse_sentence(br.text, season, epi)
            return
        elif epi >= 5 and epi != 8:
            for br in brs:
                if br.contents:
                    sentence = next(br.next_siblings, None)
                    if sentence and sentence.name != 'em' and sentence.name != 'br':
                        if not sentence or sentence == ' ':
                            continue
                        sentence_ = br.text + sentence
                        if br.text == 'Gaeta' and sentence == ': Previously o­n ':
                            continue
                        if br.text == 'Jammer' and sentence == ', to ':
                            continue
                        if br.text == 'Cally' and sentence == ': Run! Don\'t look back. Go! ':
                            sentence_ = 'Jammer: Run! Don\'t look back. Go!'
                        parse_sentence(sentence_, season, epi)
                        #print(sentence_)
            return
    if season == 4:
        if epi == 8:
            for br in brs:
                if br.contents:
                    sentence = next(br.next_siblings, None)
                    if sentence and sentence.name != 'em' and sentence.name != 'br':
                        sentence_ = br.text + sentence
                        if br.text == 'Lee' and sentence == ': Previously, on Battlestar Galactica. ':
                            continue
                        if br.text == 'Athena' and sentence == ', ':
                            continue
                        if br.text == 'to Natalie' and sentence == ': Get away from my child! You are never gonna take her. ':
                            sentence_ = 'Athena: Get away from my child! You are never gonna take her.'
                        parse_sentence(sentence_, season, epi)
            return
        else:
            for br in brs:
                if br.contents:
                    if br.contents[0].name == 'strong':
                        parse_sentence(br.text, season, epi)
            return
    #General cases
    speaker_old = ''
    for sentence in brs.previous_siblings:
        speaker = parse_sentence(sentence, season, epi, speaker_old)
        if speaker:
            speaker_old = speaker
    for sentence in brs.next_siblings:
        speaker = parse_sentence(sentence, season, epi, speaker_old)
        if speaker:
            speaker_old = speaker

#Print get all transcripts for the 6 seasons
num_season = 0
for div in divs: #for each season
    tds = div.find_all('td')
    num_season += 1
    epi = 0
    for td in tds: #for each episode
        url = base_url + td.find('a')['href']
        if 'S01E00' in url:
            continue
        print(url)
        epi += 1
        download(url, '../../data/BattlestarGalactica/html_pages/transcripts/season'+str(num_season).zfill(2)+'episode'+str(epi).zfill(2)+'.html')
        with open("../../data/BattlestarGalactica/transcripts/BattlestarGalactica.Season"+str(num_season).zfill(2)+".Episode"+str(epi).zfill(2)+".temp", "w") as text_file:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page, 'html.parser')
            div = soup.find("div", attrs={'id': "script_vo"})
            if not div:
                continue
            script_p = div.find_all('p')
            #script_p = [p for p in script_p]
            #Particular cases
            if num_season == 2:
                if epi == 19:
                    script = div.find('div')
                    brs = script.find_all('strong')
                    if not brs:
                        continue
                    parse_sentences(brs, num_season, epi)
                    continue
                elif epi == 6:
                    script = div.find('div')
                    brs = script.find_all('p')
                    if not brs:
                        continue
                    parse_sentences(brs, num_season, epi)
                    continue
                elif epi >= 4:
                    script = div.find('div')
                    brs = script.find_all('div')
                    if not brs:
                        continue
                    parse_sentences(brs, num_season, epi)
                    continue
            if num_season == 3:
                if epi == 4 and epi != 8:
                    script = div.find('div')
                    brs = script.find_all('p')
                    if not brs:
                        continue
                    parse_sentences(brs, num_season, epi)
                    continue
                elif epi >= 5 and epi != 8:
                    script = div.find('div')
                    brs = script.find_all('strong')
                    if not brs:
                        continue
                    parse_sentences(brs, num_season, epi)
                    continue
            if num_season == 4:
                if epi == 8:
                    script = div.find('div')
                    brs = script.find_all('strong')
                    if not brs:
                        continue
                    parse_sentences(brs, num_season, epi)
                    continue
                else:
                    script = div.find('div')
                    brs = script.find_all('p')
                    if not brs:
                        continue
                    parse_sentences(brs, num_season, epi)
                    continue
            #General cases
            if len(script_p) > 0:# and script_p[0] != ' ':
                script = script_p#[0]
                for paragraph in script:
                    brs = paragraph.find('br')
                    if not brs:
                        continue
                    parse_sentences(brs, num_season, epi)
            else:
                script = div
                brs = script.find('br')
                if not brs:
                    continue
                parse_sentences(brs, num_season, epi)
            #print()
        #print()
