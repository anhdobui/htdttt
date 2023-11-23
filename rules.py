import spacy
import pandas as pd
nlp = spacy.load("en_core_web_sm")

df = pd.read_csv("struct_english.csv")

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
  if(similar_row > result['similar_result']):
   result['similar_result'] = similar_row
   result['struct_result'] = row
 return result['similar_result']

