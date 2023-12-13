import spacy
import pandas as pd

df_struct_old  = pd.read_csv("struct_english.csv")
nlp = spacy.load("en_core_web_sm")
text = "I go to school by bike"

def text_struct_nlp(text):
 doc = nlp(text)
 text_struct = []
 for token in doc:
  text_struct.append(token.pos_)
 return ' '.join(text_struct)

def get_data_struct(struct:[]):
 data = {'struct': [],'Quantity':[]}
 sett = set()
 for i in struct:
  text_struct = text_struct_nlp(i)
  sett.add(text_struct)
 data['struct'] = list(sett)
 print(data)
 for i in data['struct']:
    data['Quantity'].append(len(nlp(i)))
 return data
data_struct = get_data_struct([text])
print(data_struct)

df_struct_new = pd.DataFrame(data_struct)
df_struct_new = pd.concat([df_struct_old, df_struct_new], axis=0)
df_struct_new = df_struct_new.drop_duplicates()
df_struct_new.to_csv('struct_english.csv', index=False)
print(df_struct_new)
