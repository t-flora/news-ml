from newspaper import Article
from newspaper import Config

config = Config()

url = "https://evtol.com/news/vertical-flight-society-continues-record-growth/"

article = Article(url)
article.download()
article.parse()
print(article.text)