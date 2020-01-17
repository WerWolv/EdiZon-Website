from bs4 import BeautifulSoup
import requests
from flask import Flask
import json
import datetime

app = Flask(__name__)

debug = True

cache_top = None
cache_recent = None

def log(txt):
    if debug:
        print(txt)

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
    global cache_top
    time = datetime.datetime.now()
    if cache_top is None or (cache_top['time'] - time).total_seconds() > 60*24:
        html = requests.get('https://www.switchcheatsdb.com/hof').content.decode()
        soap = BeautifulSoup(html, 'html.parser')
        divs = soap.find_all('div',"container")
        tops = divs[1]
        tops = tops.contents[7].find_all('a')
        links = [{'rank': i.next_sibling.next_sibling.div.string, 'link':i.get('href')} for i in tops]
        for i in links:
            print(f'top\t ===> \t {i}')
            i.update(process(i['link']))
        cache_top = {'time':time, 'data':links}
        return json.dumps(links)
    return json.dumps(cache_top['data'])

@app.route('/recents')
def get_recent_cheats():
    global cache_recent
    time = datetime.datetime.now()
    if cache_recent is None or (cache_recent['time'] - time).total_seconds() > 60*24:
        html = requests.get('https://www.switchcheatsdb.com/').content.decode()
        soap = BeautifulSoup(html, 'html.parser')
        divs = soap.find_all('div',"container")
        tops = divs[1]
        tops = tops.contents[7].find_all('a')
        links = [{'link': x.get('href'), 'img': x.img.get('src'), 'tittle': x.next_sibling.next_sibling.div.string} for x in tops]
        # for i in links:
        #     print(f'recent\t ===> \t {i}')
        #     i.update(process(i['link']))
        cache_recent = {'time':time, 'data':links}
        return json.dumps(links)
    return json.dumps(cache_recent['data'])

@app.route('/')
def home():
    return 'api on progress:<br>\
        <a href="\\recents"> recents cheats </a><br>\
        <a href="\\tops"> top cheats </a>\
        '



if __name__ == '__main__':
    app.env = 'development'
    app.run('0.0.0.0',port=8080)