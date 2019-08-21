import pandas as pd
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from itertools import chain
import operator
import re
from collections import Counter
import matplotlib.pyplot as plt

from spacy.lang.en.stop_words import STOP_WORDS
import operator
import pandas as pd
import re
from itertools import chain
from collections import Counter
import operator
import string
from spacy.lang.en.stop_words import STOP_WORDS
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import re
from itertools import chain
from collections import Counter
import operator
import string


# clean
def cleandf(df):
    df.dropna(subset=['Body'], inplace = True)
    dup1 = df[df['URLs'].duplicated(keep = False)].sort_values(by = 'URLs')
    df.drop_duplicates(subset='Body', keep=False, inplace=True)
    dup1.reset_index(inplace = True)
    dup1.drop(['index'], axis = 1, inplace = True)
    for i in range(len(dup1.index)-1):
        if dup1.URLs[i] == dup1.URLs[i + 1] and dup1.Body[i][:30] == dup1.Body[i+1][:30]:
            dup1.drop(i, axis = 0, inplace = True)
    clean_df = pd.concat([df, dup1])
    clean_df.reset_index(inplace = True)
    clean_df.drop(['index'], axis = 1, inplace = True)
    clean_df.Body = [re.sub(r"[\n\t\s]+",' ', i) for i in clean_df.Body]
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