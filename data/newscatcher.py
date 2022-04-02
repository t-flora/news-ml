# import sys
# import configparser
import time, csv, os, json, requests
import pandas as pd
from datetime import datetime

query = 'Vertical Aerospace OR Joby Aviation'
lang = 'en'
category = ''
to_rank = 1000
all_news = False

# if __name__ == '__main__':
#     config = configparser.ConfigParser()
#     config.read(sys.argv[1])
#     cfg = config['settings']
#     query = cfg['query']
#     lang = cfg['lang']
#     category = cfg['category']
#     to_rank = cfg['to_rank']
#     all_news = cfg['all_news']

timestamp = datetime.now().strftime("%d-%b-%Y-%H-%M")
directory = "/mnt/c/Users/TFLORA/capstone-project/data"

# This code is heavily based on the documentation example below:
# https://docs.newscatcherapi.com/knowledge-base/guides-and-tutorials/export-news-into-a-csv-with-python

# URL of our News API
base_url = 'https://api.newscatcherapi.com/v2/search'

# Your API key
try:
    API_KEY = os.environ["NC_API_KEY"]
    assert(API_KEY is not None)
except:
    raise ValueError("API key not found")

# Put API key to headers to be authorized to perform a call
headers = {'x-api-key': API_KEY}

# Define your desired parameters
### Multiple parameters
if all_news:
    params = [
        {
            'q': 'Economia OR Politica OR Crime',
            'lang': 'pt',
            'to_rank': 10000,
            'topic': "news",
            'page_size': 100,
            'page': 1
        },
        {
            'q': 'Evento',
            'lang': 'pt',
            'to_rank': 10000,
            'topic': "entertainment",
            'page_size': 100,
            'page': 1
        },
        {
            'q': 'Esporte',
            'lang': 'pt',
            'to_rank': 10000,
            'topic': "sport",
            'page_size': 100,
            'page': 1
        },
        {
            'q': 'Internacional',
            'lang': 'pt',
            'to_rank': 10000,
            'topic': "world",
            'page_size': 100,
            'page': 1
        }#,
#     {
#         'q': 'Negocios',
#         'lang': 'pt',
#         'to_rank': 10000,
#         'topic': "business",
#         'page_size': 100,
#         'page': 1
#     }
    ]
else:
    params = {
        'q': query,
        'lang': lang,
        'to_rank': to_rank,
        'topic':category,
        'page_size': 100,
        'page': 1
        }

# Make a simple call with both headers and params
# response = requests.get(base_url, headers=headers, params=params)

# # Encode received results
# results = json.loads(response.text.encode())
# if response.status_code == 200:
#     print('Done')
# else:
#     print(results)
#     print('ERROR: API call failed.')

##########################################
###### Code for multiple parameters ######
##########################################

if all_news:
    # Variable to store all found news articles, mp stands for "multiple queries"
    all_news_articles = []

    # Infinite loop which ends when all articles are extracted
    for separated_param in params:

        print(f'Query in use => {str(separated_param)}')
        
        while True:
            # Wait for 1 second between each call
            time.sleep(1)

            # GET Call from previous section enriched with some logs
            response = requests.get(base_url, headers=headers, params=separated_param)
            results = json.loads(response.text.encode())
            if response.status_code == 200:
                print(f'Done for page number => {separated_param["page"]}')

                # print(json.dumps(response.json(), indent=4, sort_keys=True))
                # Adding your parameters to each result to be able to explore afterwards
                for i in results['articles']:
                    i['used_params'] = str(separated_param)

                # Storing all found articles
                all_news_articles.extend(results['articles'])

                # Ensuring to cover all pages by incrementing "page" value at each iteration
                separated_param['page'] += 1
                if separated_param['page'] > results['total_pages']:
                    print("All articles have been extracted")
                    break
                else:
                    print(f'Proceed extracting page number => {separated_param["page"]}')
            else:
                print(results)
                print(f'ERROR: API call failed for page number => {separated_param["page"]}')
                break

    print(f'Number of extracted articles => {str(len(all_news_articles))}')
else:
    # Variable to store all found news articles
    all_news_articles = []

    # Ensure that we start from page 1
    params['page'] = 1

    # Infinite loop which ends when all articles are extracted
    while True:

        # Wait for 1 second between each call
        time.sleep(1)

        # GET Call from previous section enriched with some logs
        response = requests.get(base_url, headers=headers, params=params)
        results = json.loads(response.text.encode())
        if response.status_code == 200:
            print(f'Done for page number => {params["page"]}')


            # Adding your parameters to each result to be able to explore afterwards
            for i in results['articles']:
                i['used_params'] = str(params)


            # Storing all found articles
            all_news_articles.extend(results['articles'])

            # Ensuring to cover all pages by incrementing "page" value at each iteration
            params['page'] += 1
            if params['page'] > results['total_pages']:
                print("All articles have been extracted")
                break
            else:
                print(f'Proceed extracting page number => {params["page"]}')
        else:
            print(results)
            print(f'ERROR: API call failed for page number => {params["page"]}')
            break

    print(f'Number of extracted articles => {str(len(all_news_articles))}')

    # Define variables
unique_ids = []
unique_excerpts = []
unique_urls = []
unique_articles = []

# excs = []
# summs = []
# links = []

# Each article has keys: '_id', '_score', 'author', 'authors', 'clean_url', 'country', 'is_opinion', 'language', 'link', 'media', 'published_date', 'published_date_precision', 'rank', 'rights', 'summary', 'title', 'topic', 'twitter_account']
# Iterate on each article and check whether we saw this _id before
for article in all_news_articles:
    eb = article['excerpt'] not in unique_excerpts
    lb = article['link'] not in unique_urls
    if article['_id'] not in unique_ids:
        unique_ids.append(article['_id'])
        if eb and lb:
            unique_excerpts.append(article['excerpt'])
            unique_urls.append(article['link'])
            unique_articles.append(article)

pandas_table = pd.DataFrame(results['articles'])

field_names = list(all_news_articles[0].keys())
# Generate CSV file from dict
with open('extracted_news_articles.csv', 'w', encoding="utf-8", newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names, delimiter=";")
    writer.writeheader()
    writer.writerows(all_news_articles)

# Generate CSV from Pandas table
# Create Pandas table
pandas_table = pd.DataFrame(all_news_articles)

# Generate CSV
pandas_table.to_csv(f'csvfiles/extracted_news_articles_{timestamp}.csv')