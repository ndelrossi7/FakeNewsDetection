import pyforest
import pandas as pd


def clean_data(df):
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
    return clean_df
