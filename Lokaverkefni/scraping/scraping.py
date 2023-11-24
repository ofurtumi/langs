import re
from bs4 import BeautifulSoup
import urllib3
import json

def simple_cleaner (sent):
    sent = re.sub(r"[^ \w.]", "",sent)
    if sent == "": return
    sent = re.sub(r"[\n\t\r]*", "", sent)
    sent = re.sub(r"\s+", " ", sent)
    sent = sent.strip()
    if sent == "": return
    return sent

def snerpa():
    with open ('./snerpa_links.json') as f:
        snerpa_links = json.load(f)

    page_data = {}
    num = len(snerpa_links)

    for (i, link) in enumerate(snerpa_links, 1):
        page = urllib3.request("GET", link)
        html_data = page.data
        soup = BeautifulSoup(html_data, 'html.parser')

        all_text = soup.find('article')
        if all_text == None: return
        author = all_text.find('em')
        if author != None:
            author.extract()
        
        for br in soup.find_all("br"):
            br.replace_with("\n")

        text = [t for t in re.split(r"(\n)", all_text.text) if t != ""]
        text = [t for t in list(map(simple_cleaner, text)) if t != None]

        as_string = text[1:]
        page_data[text[0]] = as_string
        print(f"{i}/{num}", end='\r')

    return page_data

def heimsnet():
    page_data = {}
    
    with open('./solnet.txt') as f:
        log = f.read().split('\n')

    current_title = simple_cleaner( log[0] )
    current_lyrics = []
    for line in log:
        if line == "---":
            page_data[current_title] = current_lyrics
            current_title = ""
            current_lyrics = []
            continue
        if current_title == "":
            current_title = simple_cleaner(line)
            continue
        if line != "":
            current_lyrics.append(simple_cleaner(line))
    
    return page_data


page_data = {**heimsnet(), **snerpa()}
with open('./scraped_data.json', 'w', encoding="utf-8") as f:
    json.dump(page_data, f, ensure_ascii=False, indent=2)
