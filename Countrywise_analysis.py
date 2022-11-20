import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns

class country_analysis:

    def __init__(self,df):
        self.df=df
    
    def year_wise_medal_taly(self,df,country):
        temp_df=df.dropna(subset=['Medal'])
        temp_df.drop_duplicates(subset=['Team','NOC','Games','Year', 'City', 'Sport', 'Event', 'Medal'],inplace=True)
        new_df=temp_df[temp_df['region']==country]
        final_df=new_df.groupby('Year').count()[['Medal']].reset_index()
        return final_df
    
    def medal_heat_map(self,df,country):
        temp_df=df.dropna(subset=['Medal'])
        temp_df.drop_duplicates(subset=['Team','NOC','Games','Year', 'City', 'Sport', 'Event', 'Medal'],inplace=True)
        temp=temp_df[temp_df['region']==country]
        ax=temp.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0).astype(int)
        return ax

    def most_successful(self,df,country):
        temp_df=df.dropna(subset=['Medal'])

        temp_df=temp_df[temp_df['region']==country]
            
        x=temp_df['Name'].value_counts().reset_index().merge(df,left_on="index",right_on="Name",how='left')[["index","Name_x","Sport"]].drop_duplicates(subset=['index'])
        x.rename(columns={'index':'Name',"Name_x":"Medals"},inplace=True)
        return x.head(20)
