import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("i like you ")

for token in doc:
    print(token.pos_)