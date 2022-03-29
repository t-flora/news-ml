import spacy
import pandas as pd

filename = "beta_announcements.csv"
df = pd.read_csv(f"../data/csvfiles/scraped_web/{filename}")

bodies = list(df['text'])
titles = list(df['title'])

nlp = spacy.load("en_core_web_lg")
def show_ents(doc):
    if doc.ents:
        for ent in doc.ents:
            print(ent.text + ent.start_char + ent.end_char + ent.label_ + spacy.explain(ent.label_))
    else:
        print("No entities in doc")

# Process texts as a stream, much faster than calling
# nlp() on each text
t_docs = list(nlp.pipe(titles))
b_docs = list(nlp.pipe(bodies))

show_ents(t_docs[0])