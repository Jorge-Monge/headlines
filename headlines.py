from flask import Flask
import feedparser

app = Flask(__name__)

RSS_FEEDS = {'bbc': "http://feeds.bbci.co.uk/news/rss.xml",
             'cnn': "http://rss.cnn.com/rss/edition.rss",
             'fox': 'http://feeds.foxnews.com/foxnews/latest'}

@app.route("/")
@app.route("/bbc")
def bbc():
    return get_news('bbc')

@app.route("/cnn")
def cnn():
    return get_news('cnn')

@app.route("/fox")
def fox():
    return get_news('fox')

def get_news(news_provider):
    feed = feedparser.parse(RSS_FEEDS.get(news_provider))
    first_article = feed['entries'][0]
    return """
    <html>
      <body>
        <h1>{0} Headlines</h1>
          <b>{1}</b> <br/>
          <i>{2}</i> <br/>
          <p>{3}</p> <br/>
      </body>
    </html>""".format(news_provider.upper(),\
                      first_article.get("title"),\
                      first_article.get("published"),\
                      first_article.get("summary"))
          

if __name__ == '__main__':
    app.run(port = 5000, debug = True)
