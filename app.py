import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

@st.cache
def load_data():
    df=pd.read_csv("HistoricalEsportData.csv", encoding='mac_roman')
    return df

df = load_data()

@st.cache
def load_data_2():
    df_2=pd.read_csv("GeneralEsportData.csv", encoding='mac_roman')
    return df_2

df_2 = load_data_2()

def page1(title):
    st.title(title)
    rows = st.slider('Choose the number of rows data to display: ',min_value=10, max_value= df.shape[0],key="1")
    st.write(df.head(rows))


years = list(range(1995,2021))

def page2(title):
    st.title(title)
    #Tournamets held per game
    st.subheader("Tournaments Held Per Game")
    fig = px.bar(df_2, x=df_2['Game'] ,y= df_2['TotalTournaments'])
    fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig,use_container_width=True)

    years = list(range(1998,2022))
    df_3 = df.loc[years]

    #Tournaments per year
    st.subheader("Tournaments Held Per Year")
    fig,ax = plt.subplots(figsize=(20,8))
    df_3['Tournaments'].plot(kind='bar',ax=ax)
    st.pyplot(fig)

def page3(title):
    st.title(title)
#Total number of players participated per game  
    st.subheader("Players Paricipated Per Game")
    fig = px.pie(df, names= 'Game',values='Players')
    fig.update_traces(hoverinfo='label+percent', textinfo='none', textfont_size=20,
                    marker=dict( line=dict(color='#000000', width=1)))
    st.plotly_chart(fig,use_container_width=True)

    #total players participated per year
    st.subheader("Players participated Per Year")
    players = df_2.groupby('ReleaseDate')['TotalPlayers'].sum()
    data = pd.DataFrame(players)
    fig,ax = plt.subplots(figsize=(20,8))
    data.plot(kind='bar',ax=ax)
    st.pyplot(fig)

def page4(title):
    st.title(title)
    #Total Earnings per year
    st.subheader("Earnings Per Year")
    years = list(range(1998,2022))
    df_3 = df.loc[years]
    fig,ax = plt.subplots(figsize=(35,20))
    df_3['Earnings'].plot(kind='bar',ax=ax)
    st.pyplot(fig)

    #total Earnings per game
    st.subheader("Earnings Per Game")
    fig = px.pie(df_2, names= 'Game',values='TotalEarnings')
    fig.update_traces(hoverinfo='label+percent', textinfo='none', textfont_size=20,
                    marker=dict( line=dict(color='#000000', width=1)))
    st.plotly_chart(fig,use_container_width=True)


def page5(title):
    st.title(title)
    #popular genre of game
    st.subheader("Genre Popularity")
    fig = px.bar(df_2, x='Genre', y='Game')
    fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig,use_container_width=True)


    #Earnings by Genre
    st.subheader("Earnings By Genre")
    paisa = df_2.groupby('Genre').agg({'TotalEarnings':np.sum})
    paisa.reset_index(inplace=True)
    fig = px.bar(paisa,x='Genre',y='TotalEarnings')
    fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig,use_container_width=True)

def page6(title):
    st.title(title)
    #most famous game in figthing genre in terms of franchise

    esport_fight = df_2[df_2["Genre"] == "Fighting Game"]
    esport_fight = esport_fight[["Game", "TotalTournaments"]].groupby(by = "Game").sum()
    esport_fight["Share"] = esport_fight["TotalTournaments"] / esport_fight["TotalTournaments"].sum()

    esport_fight_NF = esport_fight.copy()
    esport_fight_NF.reset_index(inplace=True)
    # removing numbers, brackets, : and , signs
    esport_fight_NF.Game = esport_fight_NF.Game.str.split('\s[+0-9()\']').str[0]
    esport_fight_NF.Game = esport_fight_NF.Game.str.split('[:]').str[0]
    esport_fight_NF.Game = esport_fight_NF.Game.str.split('\sXX').str[0]
    # removing greek letters
    esport_fight_NF.replace("\sIII|\sII|\sIV|\sIX|\sVI|\sV|\sXIII|\sXII|\sXI|\sXX|\sXrd|\sX|\sI|",'',regex=True, inplace=True)
    #esport_fight_NF = esport_fight_NF.Game.str.findall("Street\sFighter|Soul\sCalibur|Super\sSmash\sBros|Guilty\sGear")
    expresion = r"Street\sFighter|Soul\sCalibur|Super\sSmash\sBros|Tekken|Dragon\sBall|Dead\sor\sAlive|Guilty\sGear"
    esport_fight_NF["Game"][esport_fight_NF.Game.str.contains(expresion)] = esport_fight_NF.Game.str.findall(expresion).str[0]
    esport_fight_NF = esport_fight_NF.groupby("Game").sum()

    fig = plt.figure(figsize=(20,5))
    # define cmap
    cmap = plt.get_cmap("Blues")
    cmap = iter(cmap([i/10 for i in range(10)]))
    # find biggest prized games - give them color
    cols = []
    labs = []
    mostvalue = esport_fight_NF.nlargest(10, 'TotalTournaments')
    for i, gamename in enumerate(esport_fight_NF.index):
        if gamename in mostvalue.index:
            cols.append(next(cmap))
            labs.append(gamename)
        else:
            cols.append("gray")
            labs.append("")
    patches, texts = plt.pie(esport_fight_NF.TotalTournaments, labels=labs, colors=cols, radius=2, textprops={'fontsize': 12})
    #plt.legend(patches, esport_fight_NF.index, loc="upper right", bbox_to_anchor=(1,1),bbox_transform=plt.gcf().transFigure)
    st.subheader("Popular Fighting Franchise")
    st.pyplot(fig)

    #total tournamet prize per game in fighting genre
    esport_fight = df_2[df_2["Genre"] == "Fighting Game"]
    esport_fight = esport_fight[["Game", "TotalEarnings"]].groupby(by = "Game").mean()
    esport_fight["Share"] = esport_fight["TotalEarnings"] / esport_fight["TotalEarnings"].sum()

    esport_fight_NF = esport_fight.copy()
    esport_fight_NF.reset_index(inplace=True)
    esport_fight_NF.Game = esport_fight_NF.Game.str.split('\s[+0-9()\']').str[0]
    esport_fight_NF.Game = esport_fight_NF.Game.str.split('[:]').str[0]
    esport_fight_NF.Game = esport_fight_NF.Game.str.split('\sXX').str[0]
    esport_fight_NF.replace("\sIII|\sII|\sIV|\sIX|\sVI|\sV|\sXIII|\sXII|\sXI|\sXX|\sXrd|\sX|\sI|",'',regex=True, inplace=True)
    expresion = r"Street\sFighter|Soul\sCalibur|Super\sSmash\sBros|Tekken|Dragon\sBall|Dead\sor\sAlive|Guilty\sGear"
    esport_fight_NF["Game"][esport_fight_NF.Game.str.contains(expresion)] = esport_fight_NF.Game.str.findall(expresion).str[0]
    esport_fight_NF = esport_fight_NF.groupby("Game").sum()
    plt.figure(figsize=(20,5))
    cmap = plt.get_cmap("Reds")
    cmap = iter(cmap([i/10 for i in range(10)]))
    cols = []
    labs = []
    mostvalue = esport_fight_NF.nlargest(10, 'TotalEarnings')
    for i, gamename in enumerate(esport_fight_NF.index):
        if gamename in mostvalue.index:
            cols.append(next(cmap))
            labs.append(gamename)
        else:
            cols.append("grey")
            labs.append("")
    patches, texts = plt.pie(esport_fight_NF.TotalEarnings, labels=labs, colors=cols, radius=2, textprops={'fontsize': 12})
    #plt.legend(patches, esport_fight_NF.index, loc="upper right", bbox_to_anchor=(1,1),bbox_transform=plt.gcf().transFigure)
    st.subheader("Earnings By Top Fighting Games Franchise")
    st.pyplot(fig)

pages = {
            # 'Introduction': home,
            'Raw Data': page1,
            'Total Tournament Analysis': page2,
            'Total Players Analysis': page3,
            'Earnings Analysis': page4,
            'Genre Analysis': page5,
            'Popular Genre Analysis': page6,
        }

page = st.sidebar.selectbox('Choose a page...',list(pages.keys()))
pages[page](page)