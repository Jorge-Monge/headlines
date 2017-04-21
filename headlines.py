from flask import Flask
from flask import render_template
from flask import request
import feedparser

app = Flask(__name__)

RSS_FEEDS = {'bbc': "http://feeds.bbci.co.uk/news/rss.xml",
             'cnn': "http://rss.cnn.com/rss/edition.rss",
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'elpais_espana': 'http://ep00.epimg.net/rss/elpais/portada.xml'}

@app.route("/", methods=['GET', 'POST'])
def get_news():
    query = request.form.get("news_provider")
    if not query or query.lower() not in RSS_FEEDS:
        news_provider = "bbc"
    else:
        news_provider = query.lower()
    feed = feedparser.parse(RSS_FEEDS.get(news_provider))
    return render_template("home.html", articles = feed['entries'])
          

if __name__ == '__main__':
    app.run(port = 5000, debug = True)
