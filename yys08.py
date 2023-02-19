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
    st.dataframe(bb, 300, 400)  


st.set_page_config(layout="wide")      

with st.form(key ='Form1'):
    with st.sidebar:
        
        select_language =  st.sidebar.radio('고객이 원하는 데이터를 분석하기 편하도록', ('한국 야구 데이터 분석', '긍정 부정 분석'))
        

#2. 워드 클라우드


def  emotion():
        
     uploaded_file = st.file_uploader("Choose a file")
    
     if uploaded_file:
        # 파일이 업로드된 경우에만 실행될 코드들
        origin_text = open(uploaded_file.name, encoding="utf8")
        positive     = open("pos_pol_word.txt", encoding="utf8")
        negative    = open("neg_pol_word.txt", encoding="utf8" )
        st.write("파일 업로드 완료")
        
        # 이하 생략
     else:
        # 파일이 업로드되지 않은 경우에 대한 처리
        st.write("파일을 선택해주세요.")

    #2. 위의 텍스트 파일 3개를 엔터로 구분해서 변수에 담습니다.
    origin = origin_text.read()    # origin_text 를 문자형 변수 origin 에 담는다
    pos =  positive.read().split('\n')  # 긍정단어를 엔터로 구분해서 리스트로 구성
    neg =  negative.read().split('\n') # 부정단어를 엔터로 구분해서 리스트로 구성

    #3. pos 와 neg 리스트에서 결측치를 제거합니다.
    pos = list( filter( lambda  x : x, pos ) )
    neg = list( filter( lambda x : x, neg ) )

    #4. 단어 한자리는 삭제
    pos1 = list( filter( lambda  x : True  if len(x) > 1  else  False, pos ) )
    neg1 = list( filter( lambda  x : True  if len(x) > 1  else  False, neg ) )

    #5. 분석하고자 하는 텍스트에 나오는 긍정단어와 부정단어 딕셔너리
    pos_dict = {}
    neg_dict = {}
    pos_dict['긍정단어'] = []
    pos_dict['긍정건수'] =[]
    neg_dict['부정단어'] = []
    neg_dict['부정건수'] =[]

    #6. 긍정단어에서 제외시키고 싶은 단어들을 제외시킵니다.
    pos1.remove('ㅎㅎ')
    pos1.remove('^^')
    pos1.remove('이벤트')
    pos1.remove('어진')
    pos1.append('맛있다')
    pos1.append('언니')

    #7. 원본 데이터에서 긍정단어가 얼마나 포함되었는지 확인하고 내리는 코드

    for i in pos1:
        if i in origin:
            pos_dict['긍정단어'].append(i)
            pos_dict['긍정건수'].append(origin.count(i))

    #8. 위에서 생성한 csv 파일을 판다스 데이터 프레임으로 만들어서 출력하는 코드
    import  pandas  as  pd

    origin_pos_df = pd.DataFrame(pos_dict)
    #origin_pos_df.columns=['긍정단어', '긍정건수'] 
    origin_pos_df['긍정순위']=origin_pos_df['긍정건수'].rank(method='dense', ascending=False).astype(int)
    a_pos = origin_pos_df[:].sort_values(by=['긍정순위']).head(20)   # 상위 20개만 출력

    #9. 부정단어에서 제외시키고 싶은 단어들을 제외시킵니다.
    neg1.remove(':D')
    neg1.remove(':)')
    neg1.remove('저는')
    neg1.append('맵다')

    #10. 원본 데이터에서 부정단어가 얼마나 포함되었는지 확인하고 내리는 코드

    for i in neg1:
        if i in origin:
            neg_dict['부정단어'].append(i)
            neg_dict['부정건수'].append(origin.count(i))


    #11. 위에서 생성한 csv 파일을 판다스 데이터 프레임으로 만들어서 출력하는 코드
    import  pandas  as  pd

    origin_nag_df = pd.DataFrame(neg_dict)
    origin_nag_df['부정순위']=origin_nag_df['부정건수'].rank(method='dense', ascending=False).astype(int)
    a_nag = origin_nag_df[:].sort_values(by=['부정순위']).head(20)   # 상위 20개만 출력

    #12. 긍정 데이터 프레임과 부정 데이터 프레임을 옆으로 붙이는 코드

    a_pos.reset_index(drop=True, inplace=True)   # a_pos 데이터 프레임의 인덱스 없앰
    a_nag.reset_index(drop=True, inplace=True)  # a_nag 데이터 프레임의 인덱스 없앰
    df_posneg=pd.concat([a_pos,a_nag],axis=1)   # 인덱스 없는 상태에서 그냥 그대로
                                                # 양옆으로 붙인다.

    uploaded_file = None
    origin_text.close()
    positive.close()
    negative.close()
    return origin_pos_df, origin_nag_df, df_posneg.style.hide_index()


def pos_word_chart(p_df):
    ##1. 워드 클라우드 생성을 위한 패키지
    # wordcoloud.py 안에 있는 WordCloud 함수를 불러와라
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
       
    ## 4. 생성된 데이터 프레임을 딕셔너리로 변환
    ##  wordcolud 함수에 데이터를 제공할 때는 데이터 프레임으로 줄 수 는 없고
    # 딕셔너리 형태로 제공 해야 합니다. 
    wc = p_df.set_index("긍정단어").to_dict()["긍정건수"]

    wordCloud = WordCloud(
    font_path = "malgunsl.ttf", # 폰트 지정
    width = 1000, # 워드 클라우드의 너비 지정
    height = 800, # 워드클라우드의 높이 지정
    max_font_size=100, # 가장 빈도수가 높은 단어의 폰트 사이즈 지정
    background_color = 'white' # 배경색 지정
    ).generate_from_frequencies(wc) # 워드 클라우드 빈도수 지정

    fig, ax = plt.subplots(figsize = (12, 8))
    ax.imshow(wordCloud)
    plt.axis('off')
    st.pyplot(fig)

def neg_word_chart(n_df):
    ##1. 워드 클라우드 생성을 위한 패키지
    # wordcoloud.py 안에 있는 WordCloud 함수를 불러와라
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

    ## 4. 생성된 데이터 프레임을 딕셔너리로 변환
    ##  wordcolud 함수에 데이터를 제공할 때는 데이터 프레임으로 줄 수 는 없고
    # 딕셔너리 형태로 제공 해야 합니다. 
    wc = n_df.set_index("부정단어").to_dict()["부정건수"]

    wordCloud = WordCloud(
    font_path = "malgunsl.ttf", # 폰트 지정
    width = 1000, # 워드 클라우드의 너비 지정
    height = 800, # 워드클라우드의 높이 지정
    max_font_size=100, # 가장 빈도수가 높은 단어의 폰트 사이즈 지정
    background_color = 'white' # 배경색 지정
    ).generate_from_frequencies(wc) # 워드 클라우드 빈도수 지정

    fig, ax = plt.subplots(figsize = (12, 8))
    ax.imshow(wordCloud)
    plt.axis('off')
    st.pyplot(fig)
 
        
if select_language =='한국 야구 데이터 분석':
    tab1, tab2 = st.tabs(["📈 Bar Chart", "🗃 Data"])
    
    with tab1:
        tab1.subheader("한국 야구 데이터 분석에 필요한 고객 맞춤 데이터 시각화")
        bar_chart()
        
    with tab2:
        tab2.subheader("A tab with the data")
        st.dataframe(bb, 300, 400)        
        
elif select_language=='긍정 부정 분석':
    tab1, tab2, tab3, tab4 = st.tabs(["🗃 Data", "📈 긍정 Chart", "📈 부정 Chart" ,"긍정부정 단어순위"])
    
    with tab1:
        tab1.subheader("긍정 부정 감성 분석")
        try:
            p_df,n_df,all_df = emotion()   
            st.dataframe(all_df, 300, 400)   
        except:
            pass
              
    with tab2:
        tab2.subheader("긍정 단어 워드 클라우드")
        try:      
            pos_word_chart(p_df)
        except:
            pass
       
    with tab3:
        tab3.subheader("부정 단어 워드 클라우드")
        try:
            neg_word_chart(n_df)
        except:
            pass
   
    with tab4:
        tab4.subheader("긍정단어와 부정단어 건수와 순위")
        try:
            st.dataframe(all_df, 300, 400)   
        except:
            pass
       
