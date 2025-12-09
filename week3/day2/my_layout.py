import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, date, time

st.sidebar.title("레이아웃 설정")
layout_type = st.sidebar.selectbox(
    "레이아웃 유형 선택:",["기본컬럼","비율컬럼","중첩컬럼"]
)
st.set_page_config(
    page_title="내 첫번째 streamlit 앱",
    layout = "wide"
)
if layout_type == "기본컬럼":
    st.header("기본 컬럼 레이아웃")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("첫번째 컬럼")
        st.write("여기는 첫번째 컬럼입니다.")

    with col2:
        st.subheader("두번째 컬럼")     

if layout_type == "비율컬럼":
    st.header("비율컬럼 레이아웃")
    col1, col2, col3 = st.columns([2,1,1])

    with col1:
        st.subheader("첫번째 컬럼")
    with col2:
        st.subheader("두번째 컬럼")   
    with col3:
        st.subheader("세번째 컬럼")    

if layout_type == "중첩컬럼":
    col1, col2 = st.columns([1,2],border=True)
    with col1:
        col1_1, col1_2 = st.columns([1,1],border=True)
        with col1_1:
            st.write("col1_1 컬럼")
        with col1_2:
            st.subheader("col1_2 컬럼")
        st.subheader("첫번째 컬럼")
    with col2:
        st.subheader("두번째 컬럼")