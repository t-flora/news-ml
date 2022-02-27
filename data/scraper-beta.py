import requests
from random import randint
from time import sleep
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd
from newspaper import Article
from newspaper import ArticleException
from newspaper import Config
from tqdm import tqdm

config = Config()
config.request_timeout = 10

url = 'https://www.beta.team/developments/page/'
scraped_data = []

for page in tqdm(range(1,6)):
  
    req = requests.get(url + str(page) + '/')
    soup = BeautifulSoup(req.text, parse_only=SoupStrainer('a'))
  
    links = soup.find_all('a', class_="beta-development-card", attrs={"href"})
    print("Number of URLs found: ", len(links))
    for l in links:
      if l.has_attr("href"):
        link = l['href']
        article = Article(link)
        try:
          article.download()
          article.parse()
          scraped_data.append([link, article.text, article.title, article.publish_date, article.summary])
        except ArticleException:
          print("ArticleException raised. Article.download() did not work for this article.")
    
    # Stretch goal: download MySQL to store full-text indexed tables and query from them

    sleep(randint(2, 10))

df = pd.DataFrame(scraped_data, columns = ['URL', 'text', 'title', 'published_date', 'summary'])
df.to_csv("beta_announcements.csv")