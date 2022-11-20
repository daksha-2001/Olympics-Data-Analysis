import pandas as pd
import numpy as np

class preprocess:

    def __init__(self,df,region_df):
        self.df=df
        self.region_df=region_df

    def extract_summer_rows(self,df):
        df=df[df['Season']=='Summer']
        return df
    
    def merge_region_df(self,df):
        df=df.merge(self.region_df,on="NOC",how='left')
        df.drop_duplicates(inplace=True)
        return df

    def dummies(self,df):
        df=pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)
        return df

    
    