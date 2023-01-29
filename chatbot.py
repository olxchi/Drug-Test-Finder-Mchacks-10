from urllib.request import urlopen
import re
from nltk.corpus import wordnet
import requests
from bs4 import BeautifulSoup
import chardet

# build list of keywords by webscraping
# use wordnet to get synonyms for those keywords
# build a dictionary of intents
# define a dictionary of responses
# matching intents and generating responses
# need to install: bs4, nltk, wordnet from nltk, requests, chardet

# this is the website we're getting main information from, pulling html of it to integrate into chatbot
url = "https://erowid.org/general/big_chart.shtml"
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")
bs = BeautifulSoup(html, features = "html.parser")



def get_drugs_from_table():
    drug_list = []
    # divide the different tables
    chem_table = bs.find('table', id="section-CHEMICALS")
    plants_table = bs.find('table', id="section-PLANTS")
    herbs_table = bs.find('table', id="section-HERBS")
  #  pharms_table = bs.find('table', id="sections-PHARMS")

    # add the title of the drugs into our keywords

    for row in chem_table.select('tr:has(a)'):
        drug_list.append(row.find('a').text)

    for row in herbs_table.select('tr:has(a)'):
        drug_list.append(row.find('a').text)


    for row in chem_table.select('tr:has(a)'):
        drug_list.append(row.find('a').text)
    
   # print(len(plants_table.find_all('tr')))

    for r in plants_table.select('tr:has(a)'):
        drug_list.append(r.find('a').text)


    # return a dictionary with drugs as keys
    # return dict.fromkeys(drug_list)
    return drug_list

def get_synonyms(lst):
    list_syn = {}
    
    for word in list(set(lst)):
        synonyms = []
        synonym_list = wordnet.synsets(word)
        
        if(len(synonym_list) != 0):
            for syn in wordnet.synsets(word):
                for lem in syn.lemmas():
                    # remove special characters
                    lem_name = re.sub('[^a-zA-Z0-9 \n\.]', ' ', lem.name())
                    synonyms.append(lem_name)
            
        list_syn[word]=set(synonyms)
    return list_syn



# build a dictionary that matches our keyword to intents
def build_intents_dict(synonyms_dict):
    keywords = {}
    keywords_dict = {}

    # adds 
    for key, syn_list in synonyms_dict.items():
        keywords[key] = ['.*\\b'+key+'\\b.*']
        for synonym in syn_list:
            keywords[key].append('.*\\b'+synonym+'\\b.*')
    
    for intent, keys in keywords.items():
        # join values in the keywords dictionary with OR 
        keywords_dict[intent]=re.compile('|'.join(keys))
    
    return keywords_dict

# using our keywords, define a response
def fill_responses_dict():
    my_string = "erowid.org"
    chem_table = bs.find('table', id="section-CHEMICALS")
    plants_table = bs.find('table', id="section-PLANTS")
    herbs_table = bs.find('table', id="section-HERBS")

    responses = {}

    for row in chem_table.select('tr:has(a)'):
        my_drug = row.find('a').text
        
        if(row.find('a').has_attr('href')):
            drug_url = 'https://' + my_string + row.find('a').attrs['href']
            if(drug_url[-1] == '/'):
                continue

            # create a beautiful soup obj
            my_page = urlopen(drug_url)
            bytes = my_page.read()

            try:
                encoding = chardet.detect(bytes)['encoding']
            except:
                encoding = 'utf-8'

            my_html = bytes.decode(encoding)
            soup = BeautifulSoup(my_html, features = "html.parser")
       #     print(soup.get_text)py -
#            drug_name = soup.findAll('div', {'class':'ts-substance-name'})[0].text

            # find children
            summary_card = soup.findAll('div', {'class':'summary-card-text-surround'})
            if(len(summary_card) >= 1):
                kids = summary_card[0].findChildren()
            else:
                continue
  #          kids = soup.findAll('div', {'class':'summary-card-text-surround'})[0].findChildren()
            for child in kids:
                responses[my_drug] = str(child.text)
            #    print(responses[my_drug])
#                print(child.text)

    for row in plants_table.select('tr:has(a)'):
        my_drug = row.find('a').text
        
        if(row.find('a').has_attr('href')):
            drug_url = 'https://' + my_string + row.find('a').attrs['href']
            if(drug_url[-1] == '/'):
                continue

            # create a beautiful soup obj
            my_page = urlopen(drug_url)
            bytes = my_page.read()

            try:
                encoding = chardet.detect(bytes)['encoding']
            except:
                encoding = 'utf-8'

            my_html = bytes.decode(encoding)
            soup = BeautifulSoup(my_html, features = "html.parser")
       #     print(soup.get_text)py -
#            drug_name = soup.findAll('div', {'class':'ts-substance-name'})[0].text

            # find children
            summary_card = soup.findAll('div', {'class':'summary-card-text-surround'})
            if(len(summary_card) >= 1):
                kids = summary_card[0].findChildren()
            else:
                continue
  #          kids = soup.findAll('div', {'class':'summary-card-text-surround'})[0].findChildren()
            for child in kids:
                responses[my_drug] = str(child.text)
            #    print(responses[my_drug])
#                print(child.text)


    for row in herbs_table.select('tr:has(a)'):
        my_drug = row.find('a').text
        
        if(row.find('a').has_attr('href')):
            drug_url = 'https://' + my_string + row.find('a').attrs['href']
            if(drug_url[-1] == '/'):
                continue

            # create a beautiful soup obj
            my_page = urlopen(drug_url)
            bytes = my_page.read()

            try:
                encoding = chardet.detect(bytes)['encoding']
            except:
                encoding = 'utf-8'

            my_html = bytes.decode(encoding)
            soup = BeautifulSoup(my_html, features = "html.parser")
       #     print(soup.get_text)py -
#            drug_name = soup.findAll('div', {'class':'ts-substance-name'})[0].text

            # find children
            summary_card = soup.findAll('div', {'class':'summary-card-text-surround'})
            if(len(summary_card) >= 1):
                kids = summary_card[0].findChildren()
            else:
                continue
  #          kids = soup.findAll('div', {'class':'summary-card-text-surround'})[0].findChildren()
            for child in kids:
                responses[my_drug] = str(child.text)
            #    print(responses[my_drug])
#                print(child.text)


    return responses

kw_dict = build_intents_dict(get_synonyms(get_drugs_from_table()))
resp = fill_responses_dict()

def get_response(msg):
    matched_intent = None
    for intent, pattern in kw_dict.items():
        if re.search(pattern, msg):
            matched_intent = intent

    key='fallback'

    if matched_intent in resp:
        key = matched_intent  

    return resp[key]

if __name__ == "__main__":
#    print(hardcoded_list())
#    poop = get_drugs_from_table()
#    print(get_synonyms(poop))
 #   print(poop)
 #   build_intents_dict(get_synonyms(poop))
 #   print(fill_responses_dict())

 # initialize our chatbot with responses

    resp['fallback'] = "Our database doesn't know that one yet! Try again later."
    resp['i love you'] = "I don't love you, but I love drug safety!"

    print("What drug are you curious about?[type 'quit' to exit]")
    while(True):
        user_input = input().lower()
        if user_input == 'quit':
            print("thanks for chatting! practice safe drug use :)")
            break
 #       matched_intent = None
 #       for intent, pattern in kw_dict.items():
  #          if re.search(pattern, user_input):
  #              matched_intent = intent
  #      key='fallback'
  #      if matched_intent in resp:
   #         key = matched_intent
        print(get_response(user_input))
