import pandas as pd
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
    return clean_df