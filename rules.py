import spacy
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import jaccard_score
nlp = spacy.load("en_core_web_sm")

df = pd.read_csv("struct_english.csv")

tfidf_vectorizer = TfidfVectorizer()
tfidf_vectorizer.fit_transform(df['struct'])

def compare_struct(text_input):
 doc_nlp_input = nlp(text_input)
 struct_input = []
 for token in doc_nlp_input:
  struct_input.append(token.pos_)
 struct_input = ' '.join(struct_input)
 
 doc_nlp_struct_input = nlp(struct_input)
 result = {'similar_result':-2}
 for row in df[df['Quantity'] == len(doc_nlp_input)]['struct']:
  doc_nlp_compare = nlp(row)
  similar_row = doc_nlp_struct_input.similarity(doc_nlp_compare)
  tfidf_row,tfidf_struct_input = tfidf_vectorizer.transform([row,struct_input])
  tfidf_row = (tfidf_row > 0).astype(float)
  tfidf_struct_input = (tfidf_struct_input > 0).astype(float)
  jaccard_similarity = jaccard_score(tfidf_row, tfidf_struct_input, average='samples')
  similar_result = (jaccard_similarity+similar_row)/2
  if(similar_row > result['similar_result']):
   result['similar_result'] = similar_result
   result['struct_result'] = row
 return result['similar_result']



