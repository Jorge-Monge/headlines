from flask import Flask
from flask import render_template
from flask import request
import requests
import feedparser
import json
import urllib2
import urllib

app = Flask(__name__)

RSS_FEEDS = {'bbc': "http://feeds.bbci.co.uk/news/rss.xml",
             'cnn': "http://rss.cnn.com/rss/edition.rss",
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'elpais_espana': 'http://ep00.epimg.net/rss/elpais/portada.xml'}

DEFAULTS = {'news_provider': 'bbc',
            'city': 'Calgary, CA'}


WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=9f3175069568b53bc97e04575bb8cdcb"

last_city = None
last_news_provider = None


@app.route("/")
def home():
    global last_news_provider
    global last_city
    # Get customized headlines, based on user input or default
    news_provider = request.args.get("news_provider")
    if not news_provider:
        if last_news_provider:
            news_provider = last_news_provider
        else:
            news_provider = DEFAULTS['news_provider']
    articles = get_news(news_provider)
    last_news_provider = news_provider
    # Get customized weather based on user input or default
    city = request.args.get('city')
    if not city:
        if last_city:
            city = last_city
        else:
            city = DEFAULTS['city']
    weather = get_weather(city)
    last_city = city

    return render_template("home.html", articles = articles, weather = weather)

def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        news_provider = DEFAULTS['news_provider']
    else:
        news_provider = query.lower()
    feed = feedparser.parse(RSS_FEEDS.get(news_provider))
    return feed['entries']

def get_weather(query):
    query = urllib.quote(query)
    url = WEATHER_URL.format(query)
    #data = urllib2.urlopen(url).read()
    try:
        data = requests.get(url).text
        parsed = json.loads(data)
        if parsed.get('weather'):
            weather = {'description': parsed['weather'][0]['description'],
                       'temperature': parsed['main']['temp'],
                       'city': parsed['name']}
        else:
            weather = {'description': 'Not Available',
                       'temperature': 'Not Available',
                       'city': 'Not Available'}
    except:
        weather = None

    return weather
    
          

if __name__ == '__main__':
    app.run(port = 5000, debug = True)
