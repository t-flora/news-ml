import spacy
from spacy.training.example import Example
from spacy.tokens import DocBin
import random
from spacy.util import minibatch, compounding
from pathlib import Path
from annotated_data import TRAIN_DATA
from valid_data import VALID_DATA

nlp = spacy.load('en_core_web_trf')

db = DocBin()
for text, annotations in TRAIN_DATA:
    doc = nlp(text)
    ents = []
    for start, end, label in annotations.get("entities"):
        span = doc.char_span(start, end, label=label)
        ents.append(span)
    doc.ents = ents
    db.add(doc)
db.to_disk("./train.spacy")

db = DocBin()
for text, annotations in VALID_DATA:
    doc = nlp(text)
    ents = []
    for start, end, label in annotations.get("entities"):
        span = doc.char_span(start, end, label=label)
        ents.append(span)
    doc.ents = ents
    db.add(doc)
db.to_disk("./valid.spacy")