import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns

class olympics_analysis:

    def __init__(self,df):
        self.df=df
    
    def plot_data_vs_year(self,df,col):
        data_over_time=df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('index')

        if col=='Name':
            data_over_time.rename(columns={'index':'Edition','Year':'Athletes'},inplace=True)
            fig=px.line(data_over_time,x='Edition',y='Athletes')
        else:
            data_over_time.rename(columns={'index':'Edition','Year':col},inplace=True)
            fig=px.line(data_over_time,x='Edition',y=col)

        return fig
    
    def plot_heatmap(self,df):
        x=df.drop_duplicates(['Year','Sport','Event'])

        ax=x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype(int)

        return ax

    def most_successful(self,df,sport):
        temp_df=df.dropna(subset=['Medal'])
        
        if sport!='Overall':
            temp_df=temp_df[temp_df['Sport']==sport]
            
        x=temp_df['Name'].value_counts().reset_index().merge(df,left_on="index",right_on="Name",how='left')[["index","Name_x","Sport","region"]].drop_duplicates(subset=['index'])
        x.rename(columns={'index':'Name',"Name_x":"Medals"},inplace=True)
        return x.head(20)





