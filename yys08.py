import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def  plotting_demo():
    
    #uploaded_file = st.file_uploader("Choose a file")

    #money=pd.read_csv(uploaded_file)
    money = pd.read_csv("money_data7.csv")

    option = st.selectbox(
        'How would you like to choice year ?',
        ('2020', '2021', '2022'))

    option2 = int(option)

    st.write('You selected:', option)

    money = money[:] [money['A_YEAR']== option2]
    
    global  aa
    
    aa = money

    fig, ax = plt.subplots(2,2, figsize=(12,8))

    plt.subplot(221)
    plt.plot(  list( money['A_MONTH'] ), list( money['A_RATE'] ), color='red' , marker='o'     ) 
    plt.xticks(tuple(money['A_MONTH']) )
    plt.title('America rate')


    plt.subplot(222)
    plt.plot(  list( money['A_MONTH'] ), list( money['K_RATE'] ), color='blue' , marker='o'     ) 
    plt.xticks(tuple(money['A_MONTH']) )
    plt.title('Korea rate')

    plt.subplot(223)
    plt.plot(  list( money['A_MONTH'] ), list( money['KOSPI'] ), color='green' , marker='o'     ) 
    plt.xticks(tuple(money['A_MONTH']) )
    plt.title('Kospi Rate')

    plt.subplot(224)
    plt.plot(  list( money['A_MONTH'] ), list( money['HOUSE_PRICE'] ), color='yellow' , marker='o'     ) 
    plt.xticks(tuple(money['A_MONTH']) )
    plt.title('House Price')

    st.pyplot(fig)
    #st.dataframe(money)
       
url = "https://sports.news.naver.com/kbaseball/record/index?category=kbo&year="

years = ['2015', '2016','2017', '2018', '2019', '2020', '2021', '2022' ]

df = pd.DataFrame([]) 

for    i    in     years: 
    df1 = pd.read_html( url + i  )[0]
    df1['년도'] =  i 
    df = pd.concat([df, df1], axis=0)

baseball = df    

baseball.팀.replace({'두산':'Dusan','삼성':'SS','키움':'KU','한화': 'HH','롯데':'Lotte','넥센':'NecSen'}, inplace=True)

        
def bar_chart():
    
    option = st.selectbox(
        'How would you like to choice year ?',
        ('2015', '2016','2017', '2018', '2019', '2020', '2021', '2022'))

    option2 = option

    st.write('You selected:', option)

    df7  =  baseball[:] [ baseball.년도==option2 ]
    
    global bb
    bb = df7    
    
    fig, ax = plt.subplots(figsize=(12,8))
  

    import plotly.express as px

    fig = px.bar(df7, x='팀', y='승률' , color='승률', hover_data= ['승률','출루율'], labels={'승률':'한국 야구 승률 데이터'} , height=400)

    plt.title( "year korea baseball winrate data", position=(0.5,1.1))
    st.plotly_chart(fig, use_container_width=True)
    #st.dataframe(df7)

st.set_page_config(layout="wide")      

with st.form(key ='Form1'):
    with st.sidebar:
        
        select_language =  st.sidebar.radio('데이터 분석 결과', ('금리가 집값에 영향을 미치는지 빠르게 파악하기', '야구의 승률과 순위의 관계 빠르게 파악하기', '다른 데이터 분석'))
        
        
if select_language =='금리가 집값에 영향을 미치는지 빠르게 파악하기':  
    tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
   
    with tab1:
        tab1.subheader("금리가 집값에 영향을 미치는지 빠르게 파악하기")
        plotting_demo()
        
    with tab2:
        tab2.subheader("A tab with the data")
        st.dataframe(aa, 1000, 400)
  

        
elif select_language =='야구의 승률과 순위의 관계 빠르게 파악하기':
    tab1, tab2 = st.tabs(["📈 Bar Chart", "🗃 Data"])
    
    with tab1:
        tab1.subheader("야구의 승률과 순위의 관계 빠르게 파악하기")
        bar_chart()
        
    with tab2:
        tab2.subheader("A tab with the data")
        st.dataframe(bb)        
        
 
  

 
