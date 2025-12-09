import streamlit as st

st.set_page_config(
    page_title="내 첫번째 streamlit 앱",
    layout = "wide"
)

st.title("내 첫번재 streamlit 앱")
st.write("이것은 첫 번째 streamlit 앱입니다.")

st.divider()


st.header("해더 텍스트")
st.write("일반 텍스트")
st.markdown("""#대제목
## 하위 제목
**굵은 글씨**            
""")
st.text("고정폭 폰트로 표시되는 텍스트입니다.")
st.write("고정폭 폰트로 표시되는 텍스트입니다.")
st.divider()

# 코드표시
st.subheader("코드표시")
st.code("""
class my_class(BaseModel):    
    def __init__(self):
        pass
        
    def hello_world(self):
        print("Hello, Streamlit!")
        return "안녕하세요!"

""",language="python")

st.divider()
st.header("사용자 입력 예제")

user_name = st.text_input("이름을 입력하세요:")

if user_name:
    st.write(f"안녕하세요, {user_name}님!")
    st.success(f"{user_name}님, 환영합니다.!")

age = st.number_input("나이를 입력하세요:",min_value=0,max_value=120,value=25)
st.write(f"입력하신 나이는 {age}세 입니다.")

favorite_color = st.selectbox("좋아하는 색깔을 선택하세요",["빨강","파랑","초록","노랑","보라"])
st.write(f"선택하신 색깔: {favorite_color}")

agree = st.checkbox("개인정보 처리에 동의합니다.")
if agree:
    st.write(f"동의해 주셔서 감사합니다.")

st.divider()

st.header("버튼 예제")
col1, col2, col3 = st.columns([1,1,8])


with col1:
    a = st.button("예약",use_container_width=True)

with col2:
    b = st.button("취소",use_container_width=True)

if a:
    st.balloons()
    st.write("안녕하세요! 버튼을 클릭해주셔서 감사합니다.")
if b:
    a = False

st.info("이것은 정보 메시지입니다.")
st.success("이것은 정보 메시지입니다.")
st.warning("이것은 경고 메시지입니다.")

st.sidebar.title("사이드바")
st.sidebar.write("여기는 사이드바입니다.")
sidebar_option = st.sidebar.radio("옵션을 선택하세요",["옵션1","옵션2","옵션3","옵션4"])


st.sidebar.write(f"선택한 옵션:{sidebar_option}")
if sidebar_option=="옵션2":
    st.balloons()

st.write(f"사이드바에서 선택한 옵션: {sidebar_option}")