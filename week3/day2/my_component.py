import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, date, time

st.title("Streamlit 핵심 컴포넌트 데모")

st.divider()

tab1,tab2,tab3,tab4 = st.tabs(["입력 위젯","데이터 표시","시각화","미디어"])
with tab1:
    st.header("입력 위젯 모음")
    
    col1, col2  = st.columns(2)
    with col1:
        st.subheader("텍스트 입력")
        text_input = st.text_input("단일 텍스트 입력")
        text_area = st.text_area("여러 줄 텍스트 입력",height=150)
        password = st.text_input("비밀번호",type="password")

        
        st.subheader("숫자입력")
        slider =st.slider("슬라이더",0,100,25)
    with col2:        
        st.subheader("선택 위젯")
        selectbox = st.selectbox("단일선택",["A","B","C"])
        radio = st.radio("라디오버튼",["D","E","F"])

        st.subheader("날짜/시간")
        date_input = st.date_input("날짜 선택",value=date.today())
        time_input = st.time_input("시간 선택",value=time(12,0))

with tab2:
    st.header("데이터 표시 컴포넌트")
    
    df = pd.DataFrame({
        '이름': ['김철수', '이영희', '박민수', '정수진', '최영수'],
        '나이': [25, 30, 35, 28, 32],
        '점수': [85, 92, 78, 95, 88],
        '등급': ['B', 'A', 'C', 'A', 'B']
    })
    st.dataframe(df,use_container_width=True)    
    st.metric("평균 점수",df["점수"].mean(),"숫자")
    st.metric("학생 수",len(df),"글자")

with tab3:
    st.title("시각화 컴포넌트")

    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['A', 'B', 'C']
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("선 그래프")
        st.line_chart(chart_data)

        st.subheader("막대 차트")
        st.bar_chart(chart_data)
    with col2:
        st.subheader("영역 차트")
        st.area_chart(chart_data)

        st.subheader("Matplotlib 차트")
        fig, ax = plt.subplots()
        ax.hist(np.random.randn(100),bins=20)
        ax.set_title("히스토그램")
        st.pyplot(fig)
    
    st.subheader("지도")
    map_data = pd.DataFrame(
        np.random.randn(100,2) / [50,50] + [37.76, -122.4],
        columns=['lat', 'lon']
    )
    st.map(map_data)

with tab4:
    st.subheader("이미지")
    col1, col2 = st.columns(2)
    with col1:
        image_array = np.random.rand(100,100,3)
        filename = "aaa.png"
        st.image("./"+filename,caption="랜덤 이미지" , width=200)

        st.subheader("파일 업로드")
        uploaded_file = st.file_uploader(
            "파일을 선택하세요",
            type=['txt', 'csv', 'png', 'jpg']
        )
        if uploaded_file is not None:
            st.write(f"업로드된 파일: {uploaded_file.name}")
            st.write(f"파일 크기: {uploaded_file.size} bytes")            
            with open("./"+uploaded_file.name,'wb') as file:
                imgDatga = uploaded_file.read()
                file.write(imgDatga)
                filename = uploaded_file.name
    with col2:
        st.subheader("다운로드 버튼")
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="CSV 다운로드",
            data=csv_data,
            file_name="sample_data.csv",
            mime="text/csv"
        )