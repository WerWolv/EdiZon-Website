from bs4 import BeautifulSoup
import requests
from flask import Flask
import json

app = Flask(__name__)

def process(link):
    html = requests.get('https://www.switchcheatsdb.com' + link).content.decode()
    soap = BeautifulSoup(html, 'html.parser')
    js = {
        'tittle': soap.h1.string,
        'img': soap.img['src']
        }
    return js

@app.route('/tops')
def get_top_cheats():
    html = requests.get('https://www.switchcheatsdb.com/hof').content.decode()
    soap = BeautifulSoup(html, 'html.parser')
    divs = soap.find_all('div',"container")
    tops = divs[1]
    tops = tops.contents[7].find_all('a')
    links = [{'rank': i.next_sibling.next_sibling.div.string, 'link':i.get('href')} for i in tops]
    for i in links:
        i.update(process(i['link']))
    return json.dumps(links)

@app.route('/recents')
def get_recent_cheats():
    html = requests.get('https://www.switchcheatsdb.com/').content.decode()
    soap = BeautifulSoup(html, 'html.parser')
    divs = soap.find_all('div',"container")
    tops = divs[1]
    tops = tops.contents[7].find_all('a')
    links = [{'link': x.get('href')} for x in tops]
    for i in links:
        i.update(process(i['link']))
    return json.dumps(links)

if __name__ == '__main__':
    app.env = 'development'
    app.run('0.0.0.0',port=8080)