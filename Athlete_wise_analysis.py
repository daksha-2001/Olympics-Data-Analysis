import pandas as pd
import numpy as np
import plotly.figure_factory as ff


class Athlete:

    def __init__(self,df):
        self.df=df
    
    def age_vs_medal(self,df):
        athlete_df=df.drop_duplicates(subset=['Name','region'])

        x1=athlete_df['Age'].dropna()
        x2=athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
        x3=athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
        x4=athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()

        fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
        fig.update_layout(autosize=False,width=1000,height=600)
        return fig

    def age_vs_sports(self,athlete_df):
        x = []
        name = []
        famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
        for sport in famous_sports:
            temp_df = athlete_df[athlete_df['Sport'] == sport]
            x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
            name.append(sport)

        fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)

        return fig

    def weight_v_height(self,df,sport):
        athlete_df = df.drop_duplicates(subset=['Name', 'region'])
        athlete_df['Medal'].fillna('No Medal', inplace=True)
        if sport != 'Overall':
            temp_df = athlete_df[athlete_df['Sport'] == sport]
            return temp_df
        else:
            return athlete_df

    def men_vs_women(self,df):
        athlete_df = df.drop_duplicates(subset=['Name', 'region'])

        men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
        women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

        final = men.merge(women, on='Year', how='left')
        final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

        final.fillna(0, inplace=True)

        return final