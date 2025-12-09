"""
Streamlit 기본 앱 실습
- 기본적인 Streamlit 앱 구조 이해
- 텍스트 출력과 간단한 사용자 입력 처리
"""

import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="기본 Streamlit 앱",
    page_icon="🚀",
    layout="centered"
)

# 제목과 설명
st.title("첫 번째 Streamlit 앱")
st.write("Streamlit을 사용한 간단한 웹 애플리케이션입니다.")

# 구분선
st.divider()

# 기본 텍스트 출력
st.header("텍스트 출력 예제")
st.write("일반 텍스트입니다.")
st.markdown("**굵은 글씨**와 *기울임 글씨*를 사용할 수 있습니다.")
st.text("고정폭 폰트로 표시되는 텍스트입니다.")

# 코드 표시
st.subheader("코드 표시")
st.code("""
def hello_world():
    print("Hello, Streamlit!")
    return "안녕하세요!"
""", language="python")

# 구분선
st.divider()

# 간단한 사용자 입력
st.header("사용자 입력 예제")

# 텍스트 입력
user_name = st.text_input("이름을 입력하세요:")

# 입력이 있을 때만 출력
if user_name:
    st.write(f"안녕하세요, {user_name}님!")
    st.success(f"{user_name}님, 환영합니다!")

# 숫자 입력
age = st.number_input("나이를 입력하세요:", min_value=0, max_value=120, value=25)
st.write(f"입력하신 나이: {age}세")
 
# 선택 박스
favorite_color = st.selectbox(
    "좋아하는 색깔을 선택하세요:",
    ["빨강", "파랑", "초록", "노랑", "보라"]
)
st.write(f"선택하신 색깔: {favorite_color}")

# 체크박스
agree = st.checkbox("개인정보 처리에 동의합니다.")
if agree:
    st.write("동의해 주셔서 감사합니다.")

# 구분선
st.divider()

# 버튼 예제
st.header("버튼 예제")

if st.button("인사하기"):
    st.balloons()  # 축하 애니메이션
    st.write("안녕하세요! 버튼을 클릭해주셔서 감사합니다.")

# 정보 메시지
st.info("이것은 정보 메시지입니다.")
st.warning("이것은 경고 메시지입니다.")

# 사이드바
st.sidebar.title("사이드바")
st.sidebar.write("여기는 사이드바입니다.")
sidebar_option = st.sidebar.radio(
    "옵션을 선택하세요:",
    ["옵션 1", "옵션 2", "옵션 3"]
)
st.sidebar.write(f"선택된 옵션: {sidebar_option}")

# 메인 영역에 사이드바 선택 결과 표시
st.write(f"사이드바에서 선택한 옵션: {sidebar_option}")
