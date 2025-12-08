"""
Streamlit 핵심 컴포넌트 데모
- 다양한 입력 위젯 사용법
- 데이터 표시 컴포넌트 활용
- 미디어 및 시각화 컴포넌트 실습
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, date, time

# 페이지 설정
st.set_page_config(
    page_title="핵심 컴포넌트 데모",
    page_icon="🎛️",
    layout="wide"
)

st.title("Streamlit 핵심 컴포넌트 데모")
st.write("다양한 Streamlit 컴포넌트들을 실습해보세요.")

# 탭으로 섹션 구분
tab1, tab2, tab3, tab4 = st.tabs(["입력 위젯", "데이터 표시", "시각화", "미디어"])

# 탭 1: 입력 위젯
with tab1:
    st.header("입력 위젯 모음")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("텍스트 입력")
        text_input = st.text_input("단일 텍스트 입력", placeholder="여기에 입력하세요")
        text_area = st.text_area("여러 줄 텍스트", height=100)
        password = st.text_input("비밀번호", type="password")
        
        st.subheader("숫자 입력")
        number = st.number_input("숫자 입력", min_value=0, max_value=100, value=50)
        slider = st.slider("슬라이더", 0, 100, 25)
        range_slider = st.slider("범위 슬라이더", 0, 100, (20, 80))
        
    with col2:
        st.subheader("선택 위젯")
        selectbox = st.selectbox("단일 선택", ["옵션 1", "옵션 2", "옵션 3"])
        multiselect = st.multiselect("다중 선택", ["A", "B", "C", "D"])
        radio = st.radio("라디오 버튼", ["선택 1", "선택 2", "선택 3"])
        
        st.subheader("날짜/시간")
        date_input = st.date_input("날짜 선택", value=date.today())
        time_input = st.time_input("시간 선택", value=time(12, 0))
        
        st.subheader("기타")
        checkbox = st.checkbox("체크박스")
        color = st.color_picker("색상 선택", "#FF0000")
    
    # 입력 결과 표시
    if st.button("입력 결과 확인"):
        st.json({
            "텍스트": text_input,
            "숫자": number,
            "슬라이더": slider,
            "선택박스": selectbox,
            "다중선택": multiselect,
            "라디오": radio,
            "체크박스": checkbox,
            "날짜": str(date_input),
            "시간": str(time_input),
            "색상": color
        })

# 탭 2: 데이터 표시
with tab2:
    st.header("데이터 표시 컴포넌트")
    
    # 샘플 데이터 생성
    df = pd.DataFrame({
        '이름': ['김철수', '이영희', '박민수', '정수진', '최영수'],
        '나이': [25, 30, 35, 28, 32],
        '점수': [85, 92, 78, 95, 88],
        '등급': ['B', 'A', 'C', 'A', 'B']
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("데이터프레임 (인터랙티브)")
        st.dataframe(df, use_container_width=True)
        
        st.subheader("메트릭 카드")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("평균 점수", f"{df['점수'].mean():.1f}", "2.1")
        with col_b:
            st.metric("최고 점수", df['점수'].max(), "5")
        with col_c:
            st.metric("학생 수", len(df), "1")
    
    with col2:
        st.subheader("정적 테이블")
        st.table(df)
        
        st.subheader("JSON 데이터")
        st.json({
            "총 학생 수": len(df),
            "평균 나이": df['나이'].mean(),
            "등급 분포": df['등급'].value_counts().to_dict()
        })

# 탭 3: 시각화
with tab3:
    st.header("시각화 컴포넌트")
    
    # 차트용 데이터 생성
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['A', 'B', 'C']
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("선 차트")
        st.line_chart(chart_data)
        
        st.subheader("막대 차트")
        st.bar_chart(chart_data)
    
    with col2:
        st.subheader("영역 차트")
        st.area_chart(chart_data)
        
        st.subheader("Matplotlib 차트")
        fig, ax = plt.subplots()
        ax.hist(np.random.randn(100), bins=20)
        ax.set_title("히스토그램")
        st.pyplot(fig)
    
    # 지도 데이터
    st.subheader("지도")
    map_data = pd.DataFrame(
        np.random.randn(100, 2) / [50, 50] + [37.76, -122.4],
        columns=['lat', 'lon']
    )
    st.map(map_data)

# 탭 4: 미디어
with tab4:
    st.header("미디어 컴포넌트")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("이미지")
        # 간단한 이미지 생성 (numpy 배열)
        image_array = np.random.rand(100, 100, 3)
        st.image(image_array, caption="랜덤 이미지", width=200)
        
        st.subheader("파일 업로드")
        uploaded_file = st.file_uploader(
            "파일을 선택하세요",
            type=['txt', 'csv', 'png', 'jpg']
        )
        if uploaded_file is not None:
            st.write(f"업로드된 파일: {uploaded_file.name}")
            st.write(f"파일 크기: {uploaded_file.size} bytes")
    
    with col2:
        st.subheader("다운로드 버튼")
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="CSV 다운로드",
            data=csv_data,
            file_name="sample_data.csv",
            mime="text/csv"
        )
        
        st.subheader("진행률 표시")
        if st.button("진행률 시뮬레이션"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(100):
                progress_bar.progress(i + 1)
                status_text.text(f'진행률: {i+1}%')
                # 실제로는 time.sleep() 사용하지만 데모용으로 생략
            
            status_text.text('완료!')
            st.success('작업이 완료되었습니다!')

# 사이드바에 컨트롤 추가
st.sidebar.header("컨트롤 패널")
show_code = st.sidebar.checkbox("코드 예제 보기")

if show_code:
    st.sidebar.code("""
# 기본 사용법
import streamlit as st

# 텍스트 출력
st.write("Hello World")

# 입력 위젯
name = st.text_input("이름")
age = st.slider("나이", 0, 100)

# 조건부 출력
if name:
    st.write(f"안녕하세요, {name}님!")
    """, language="python")

# 알림 메시지
st.sidebar.info("각 탭을 클릭하여 다양한 컴포넌트를 확인해보세요!")
st.sidebar.warning("일부 기능은 실제 파일이나 데이터가 필요할 수 있습니다.")
