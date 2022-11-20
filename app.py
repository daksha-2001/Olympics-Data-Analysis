import streamlit as st
import pandas as pd
from preprocesss import preprocess
from medal_tally import medal_tally
from olympics_analysis import olympics_analysis
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from Countrywise_analysis import country_analysis
from Athlete_wise_analysis import Athlete

df=pd.read_csv('athlete_events.csv')
region_df=pd.read_csv('noc_regions.csv')


st.sidebar.title("Olympics Analysis")
radio=st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise analysis','Athlete-wise analysis')
)



preprocesss=preprocess(df,region_df)
medal_tally =medal_tally(df)
olympics_analysis=olympics_analysis(df)
country_analysis=country_analysis(df)
Athlete_analysis=Athlete(df)

df=preprocesss.extract_summer_rows(df)
merged_df=preprocesss.merge_region_df(df)
main_df=preprocesss.dummies(merged_df)


if radio=='Medal Tally':
    st.sidebar.header('Medal Tally')

    year,country=medal_tally.country_year(main_df)
    
    selected_country=st.sidebar.selectbox("Select Country",country)
    selected_year=st.sidebar.selectbox("Select Year",year)

    medals=medal_tally.fetch_medal_tally(main_df,selected_year,selected_country)

    if selected_year=='Overall' and selected_country=='Overall':
        st.title('Overall Tally')
    
    elif selected_year=='Overall' and selected_country!='Overall':
        st.title(selected_country+" Olympics Performance")

    elif selected_year!='Overall' and selected_country=='Overall':
        st.title('Medal Tally in '+ str(selected_year)+" Olympics")

    elif selected_year!='Overall' and selected_country!='Overall':
        st.title(selected_country+" Performance in "+ str(selected_year) + " Olympics")
        
    st.table(medals)

if radio=="Overall Analysis":
    Edition=main_df['Year'].unique().shape[0]-1
    Sport=main_df['Sport'].unique().shape[0]
    Event=main_df['Event'].unique().shape[0]
    Athlete=main_df['Name'].unique().shape[0]
    City=main_df['City'].unique().shape[0]
    nations=main_df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Editions")
        st.title(Edition)
    with col2:
        st.header("Hosts")
        st.title(City)
    with col3:
        st.header("Sports")
        st.title(Sport)

    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Events")
        st.title(Event)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(Athlete)

    fig=olympics_analysis.plot_data_vs_year(main_df,'region')
    st.title("Participating Nations over the Years")
    st.plotly_chart(fig)

    fig=olympics_analysis.plot_data_vs_year(main_df,'Event')
    st.title("Participating Events over the Years")
    st.plotly_chart(fig)

    fig=olympics_analysis.plot_data_vs_year(main_df,'Name')
    st.title("No. of Athletes over the Years")
    st.plotly_chart(fig)

    st.title("No. of Events over the Years for every Sport")
    fig,ax=plt.subplots(figsize=(20,20))
    pivot=olympics_analysis.plot_heatmap(main_df)
    sns.heatmap(pivot, ax=ax,annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sports_list=main_df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0,'Overall')
    sports=st.selectbox("Select Sports",sports_list)
    X=olympics_analysis.most_successful(main_df,sports)
    st.table(X)

if radio=="Country-wise analysis":

    st.sidebar.title('Country-Wise Analysis')
    country_list=main_df['region'].dropna().unique().tolist()
    country_list.sort()
    country=st.sidebar.selectbox("Select Country",country_list) 

    st.title(country+" Medal Tally over the Years")
    data=country_analysis.year_wise_medal_taly(main_df,country)

    fig=px.line(data,'Year','Medal')
    st.plotly_chart(fig)

    st.title(country+" excels in Following Sports")
    pivot_1=country_analysis.medal_heat_map(main_df,country)
    fig,ax=plt.subplots(figsize=(20,20))
    sns.heatmap(pivot_1, ax=ax,annot=True)
    st.pyplot(fig)

    st.title("Top 15 Athletes of "+country)
    athletes=country_analysis.most_successful(main_df,country)
    st.table(athletes)

if radio=='Athlete-wise analysis':

    fig=Athlete_analysis.age_vs_medal(main_df)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age wrt Medals")
    st.plotly_chart(fig)

    fig=Athlete_analysis.age_vs_sports(main_df)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight For a Specific Sport')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = Athlete_analysis.weight_v_height(main_df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = Athlete_analysis.men_vs_women(main_df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)


     



