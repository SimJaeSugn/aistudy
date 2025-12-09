import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="My App", page_icon="🚀")

# 2. 사이드바
st.sidebar.title("Navigation")

# 3. 메인 콘텐츠
st.title("Main Content")

# 4. 사용자 입력
user_input = st.text_input("Enter something:")

# 5. 처리 및 출력
if user_input:
    st.write(f"You entered: {user_input}")