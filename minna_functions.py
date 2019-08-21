import pyforest
import pandas as pd
import re
from itertools import chain
from collections import Counter
import operator
import string


def clean_data(df):
    '''cleans data from the kaggle dataset: removes duplicate entries and null rows'''
    df.dropna(subset=['Body'], inplace = True)
    duplicates = df[df.URLs.duplicated(keep = False)].sort_values(by='URLs')
    duplicates.reset_index(inplace = True)
    duplicates.drop(['index'], axis = 1, inplace= True)
    df.drop_duplicates(subset = 'Body', keep = False, inplace = True)
    
    for i in range(len(duplicates.index)-1):
        if duplicates.URLs[i] == duplicates.URLs[i + 1] and duplicates.Body[i][:30] == duplicates.Body[i+1][:30]:
            duplicates.drop(i, axis = 0, inplace = True)
            
    clean_df = pd.concat([df, duplicates])
    clean_df.reset_index(inplace = True)
    clean_df.drop(['index'], axis = 1, inplace = True)
    clean_df['Body'] = [ re.sub(r"[\n\t\s]+",' ', clean_df['Body'][i]) for i in range(len(clean_df))]
    
    return clean_df

def token_words(df):
    vector_words_all = []
    for i in range(len(df)):
        vector_words_all.append(df['token_body'][i])

    list_words = list(chain.from_iterable(vector_words_all))

    counts = Counter()
    for token in list_words:
        if token.is_stop == False and token.is_punct == False:
            counts[token.lemma_] += 1

    counts = dict(counts)
    counts = dict(sorted(counts.items(), key=operator.itemgetter(1),reverse=True))
    return counts

def token_dataframe_from_dict(_dict):
    counts_df = pd.DataFrame.from_dict(_dict, orient='index')
    counts_df.reset_index(inplace = True)
    counts_df.columns = ['word','number']
    
    return counts_df



def get_article_type(df, _type):
    articles = df.loc[df['Label'] == _type]
    articles.reset_index(inplace = True)
    articles.drop('index', axis = 1, inplace = True)
    return articles









