import random
import spacy
from spacy.training import Example
nlp = spacy.load("en_core_web_lg")

ner = nlp.get_pipe("ner")

COMPANIES = ["Vertical Aerospace", "Archer Aviation", "Joby Aviation", \
    "Lilium"]

#the training data with named entity NE needs to be of this format 
# ( "training example",[(strat position of NE,end position of NE,"type of NE")] )

# Possible entity labels in spacy:
# PERSON, NORP (nationalities, religious or political groups)
# FAC (Buildings, airports, highways, bridges, infrastructure)
# ORG (Companies, agencies, institutions, etc.)
# GPE (Countries, cities, states)
# LOC (Non-GPE locations, natural features)
# PRODUCT, EVENT, WORK_OF_ART, LAW, LANGUAGE, DATE, TIME (smaller than a day)
# PERCENT, MONEY, QUANTITY, ORDINAL, CARDINAL

# train_strs = {
#     "Uber blew through $1 million a week" : {"Uber" : "ORG"},
#     "Android Pay expands to Canada" : {"Android": "PRODUCT", "Canada" : "GPE"},
#     "Spotify steps up Asia expansion" : {"Spotify" : "ORG", "Asia" : "GPE"},
#     "Google Maps launches location sharing" : {"Google Maps" : "PRODUCT"},
#     "Google rebrands its business apps" : {"Google" : "ORG"},
#     "look what i found on google! 😂" : {"google" : "PRODUCT"}
# }

def patt_finder(substr, string):
    start_idx = string.index(substr)
    end_idx = start_idx + len(substr)
    return start_idx, end_idx

train_data = []
for i, sentence in enumerate(train_strs.keys()):
    assert(len(train_data)==i)
    num_ents = len(train_strs[sentence].keys())
    train_data.append([sentence, [None]*num_ents])
    for j in range(num_ents):
        sent_dict = train_strs[sentence]
        start_idx, end_idx = patt_finder(list(sent_dict.keys())[j], sentence)
        ent_str = list(sent_dict.values())[j]
        train_data[i][1][j] = (start_idx, end_idx, ent_str)

# format for TRAIN_DATA
# TRAIN_DATA = [
# (sentence, [(substr_start_idx, substr_end_idx, 'ORG')]),
#  ... 
# ]

#An optimizer is set to update the model’s weights.
# optimizer = nlp.create_optimizer()
# for itn in range(100):
#     random.shuffle(train_data)
#     for raw_text, entity_offsets in train_data:
#         doc = nlp.make_doc(raw_text)
#         example = Example(doc, entity_offsets)
#         nlp.update([doc], [example], drop=0.25, sgd=optimizer)
# #setting drop makes it harder for the model to just memorize the data.
# nlp.to_disk("/model")