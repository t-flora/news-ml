import pandas as pd
import glob
import os
from newspaper import Article
from datetime import datetime

# dt_extension = '10-Dec-2021-17:27'
# print(list(glob.iglob("*.csv")))
cwd = os.getcwd()

filename = max(glob.iglob(f"{cwd}/csvfiles/*.csv"), key = os.path.getmtime)
timestamp = datetime.now().strftime("%d-%b-%H-%M")

# df = pd.read_csv(f"extracted_news_articles_{dt_extension}.csv", encoding = 'utf-8')
df = pd.read_csv(filename, encoding = 'utf-8')

def add_text(df, drop_na = False):
    df['text'] = None
    for i, url in enumerate(df['link']):
        try:
            article = Article(url)
            article.download()
            article.parse()
            df.at[i, 'text'] = article.text
        except:
            pass
    if drop_na:
        df.dropna(inplace = True)
    return df

df = add_text(df)

try:
    assert(len(df)>4)
except:
    print("Dataframe contains less than 5 elements")

df.to_csv(f"{cwd}/csvfiles/text-added-{timestamp}.csv", encoding = 'utf-8')