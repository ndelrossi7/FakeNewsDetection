from spacy.lang.en.stop_words import STOP_WORDS
import operator
import pandas as pd
import re
from itertools import chain
from collections import Counter
import operator
import string
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.manifold import TSNE
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
import numpy as np
from sklearn.model_selection import train_test_split
import warnings
from nltk.tokenize import RegexpTokenizer
import seaborn as sns 

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


def barplot(df, name):
    name = str(name)
    fig = plt.figure(figsize=(18,6))
    sns.barplot(x=df.word[:10], y=df.number[:10], palette=sns.cubehelix_palette(reverse = True))
    plt.title(f'Top 10 Most Common Words used in {name} Articles')
    plt.show()


def lemma(df):
    tokenizer = RegexpTokenizer(r'[a-zA-Z0-9]+')
    lemmatizer = WordNetLemmatizer()
    nltk.download('wordnet')
    stop_words = set(stopwords.words('english')) 
    df['token_body'] = df['Body'].apply(lambda x: tokenizer.tokenize(x))
    df['token_body'] = df['token_body'].apply(lambda x: [word for word in x if word not in stop_words])
    df['lemma'] = df['token_body'].apply(lambda x: [lemmatizer.lemmatize(w.lower()) for w in x])
    df['lemma'] = df['lemma'].apply(lambda x: (" ").join(x))
    return df


def topic_analysis(df):
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    tf = tf_vectorizer.fit_transform(df['lemma'])
    tf_feature_names = tf_vectorizer.get_feature_names()

    no_topics = 20
    lda = LatentDirichletAllocation(n_topics=no_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)
    return lda


def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print ("Topic %d:" % (topic_idx))
        print (" ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]]))








