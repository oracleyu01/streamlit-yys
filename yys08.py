import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



       
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

    df  =  baseball[:] [ baseball.년도==option2 ]
    
    global bb
    bb = df    
    
    fig, ax = plt.subplots(figsize=(12,8))
  
    import plotly.express as px
    
    df['category'] = [str(i) for i in df.index]

    color_discrete_sequence = ['dodgerblue']*len(df)
    color_discrete_sequence[0] = 'gold'
    color_discrete_sequence[2] = 'gold'


    fig = px.bar(df, y='승률', x='팀', 
                 text='승률',
                 hover_data= ['출루율','장타율'], title='한국 야구팀 승률 분석',
                 color='category',
                 color_discrete_sequence=color_discrete_sequence )

    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    st.plotly_chart(fig, use_container_width=True)


st.set_page_config(layout="wide")      

with st.form(key ='Form1'):
    with st.sidebar:
        
        select_language =  st.sidebar.radio('고객이 원하는 데이터를 분석하기 편하도록', ('한국 야구 데이터 분석', '다른 데이터 분석'))
        
        
        
if select_language =='한국 야구 데이터 분석':
    tab1, tab2 = st.tabs(["📈 Bar Chart", "🗃 Data"])
    
    with tab1:
        tab1.subheader("한국 야구 데이터 분석에 필요한 고객 맞춤 데이터 시각화")
        bar_chart()
        
    with tab2:
        tab2.subheader("A tab with the data")
        st.dataframe(bb)        
        
