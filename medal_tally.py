import pandas as pd
import numpy as np

class medal_tally:

    def __init__(self,df):
        self.df=df
    
    def medal(self,df,flag):
        medal_tally=df.drop_duplicates(subset=['Team','NOC','Games','Year', 'City', 'Sport', 'Event', 'Medal'])
        
        if flag==1:
            medal=medal_tally.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year',ascending=True).reset_index()
        else:
            medal=medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()

        medal['Gold']=medal['Gold'].astype('int')
        medal['Silver']=medal['Silver'].astype('int')
        medal['Bronze']=medal['Bronze'].astype('int')

        medal['Total']=medal['Gold']+medal['Silver']+medal['Bronze']

        return medal

    def country_year(self,df):
        year=df['Year'].unique().tolist()
        country=df['region'].dropna().unique().tolist()

        country.sort()
        year.sort()

        country.insert(0,'Overall')
        year.insert(0,'Overall')

        return year,country

    def fetch_medal_tally(self,medal,year,country):

        flag=0

        if year=='Overall' and country=='Overall':
            df=medal
        
        if year=='Overall' and country!='Overall':
            flag=1
            df=medal[medal['region']==country]
        
        if year!='Overall' and country=='Overall':
            df=medal[medal['Year']==year]
        
        if year!='Overall' and country!='Overall':
            df=medal[(medal['Year']==year) & (medal['region']==country)]

        df=self.medal(df,flag)

        return df


