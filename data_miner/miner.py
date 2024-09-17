import requests 
from bs4 import BeautifulSoup 
from translate import Translator

translator = Translator(from_lang='russian', to_lang='english')

def get_first_data(url):
    try:
        html_source = requests.get(url).text
        html_source = BeautifulSoup(html_source)

        return [[el for el in html_source.find_all('h3') if len(el.get_text()) <= 20],html_source.find_all(class_='img_left')[0].find('a')['href']]
    except: return None

def get_subtext(url, theme):
    html_source = requests.get(url).text
    html_source = BeautifulSoup(html_source)
    return [el.get_text() for el in html_source.find_all('p') if sum([e.lower() in el.get_text().lower() for e in theme.split()]) > len(theme.split())*(2/3)]

def translator_translate(word):
    return translator.translate(word).replace(' ', '_').replace('-','_').lower()

