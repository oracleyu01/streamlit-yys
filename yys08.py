import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#money = pd.read_csv("money_data7.csv")

#st.sidebar.success("Select a demo above.")

def  plotting_demo():
    money = pd.read_csv("money_data7.csv")
    option = st.selectbox(
        'How would you like to choice year ?',
        ('2020', '2021', '2022'))

    option2 = int(option)

    st.write('You selected:', option)

    money = money[:] [money['A_YEAR']== option2]

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
    st.dataframe(money)

with st.form(key ='Form1'):
    with st.sidebar:
        #user_word = st.sidebar.text_input("Enter a keyword", "habs")    
        select_language = st.sidebar.radio('What do you want treand?', ('Money', 'baseball', 'text mining'))
        #include_retweets = st.sidebar.checkbox('Include retweets in data')
        #num_of_tweets = st.sidebar.number_input('Maximum number of tweets', 100)
        #submitted1 = st.form_submit_button(label = 'Search Twitter 🔎')
         
        
if select_language =='All':        
    plotting_demo()      
