import spacy
import pandas as pd
from IPython.display import display

def tokens_to_df(doc, properties=None, is_display=True):
                
    texts = [token.text for token in doc] 
    index = [token.i for token in doc] 
    if properties is None:
        properties = ['text', 'i', 'idx', 'text_with_ws', 'is_sent_start', 'is_sent_end', 
                   'head', 'dep_', 'ent_type_', 'tag_', 'lemma_', 
                   'norm_', 'is_stop', 'is_oov', ('tag_explain', token_explain('tag_'))]
    columns = [property_ if isinstance(property_, str) else property_[0] 
               for property_ in properties]        
    df_token = pd.DataFrame(columns = columns,
                            index = index)    
    for token in doc: 
        for property_ in properties:
            if isinstance(property_, str): 
                df_token.loc[token.i, property_] = getattr(token, property_)
            else:
                df_token.loc[token.i, property_[0]] = property_[1](token)
                   
    if is_display:
        df_token = df_token.style.set_properties(**{'text-align': 'left'})          
        display(df_token)
    return df_token

def tokens_to_sheet(doc, properties=None):
    if properties is None:
        properties = [('text', 15), ('tag_', 15), ('head', 15), ('dep_', 15), 
                      (('tag_explain', token_explain('tag_')), 30)]
        
    headers = [property_ if isinstance(property_, str) else property_[0] 
               for property_, width in properties]
    widths = [width for _, width in properties]
    header_text = ''.join([f'{header:<{width}}'  for header, width in zip(headers, widths)])    
    
    row_texts =[]
    for token in doc: 
        column_values = []
        for property_, width  in properties:
            if isinstance(property_, str): 
                column_values.append(str(getattr(token, property_)))
            else:
                column_values.append(str(property_[1](token)))
        row_text = ''.join([f'{value:<{width}}'  for value, width in zip(column_values, widths)])
        row_texts.append(row_text)
        
    print(header_text)
    max_len = max([len(row_text) for row_text in row_texts]) + 2
    print('-'*max_len)
    for row_text in row_texts:
        print(row_text)    
    

def token_explain(property_):
    def explain(token):
        return spacy.explain(getattr(token, property_)) 
    return explain


