# Streamlit의 구조와 핵심 컴포넌트

## Streamlit 앱의 기본 구조

### 실행 모델
Streamlit은 위에서 아래로 순차적으로 실행되는 스크립트 기반 모델을 사용합니다.

```python
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
```

### 상태 관리
- Streamlit은 기본적으로 상태를 유지하지 않음 (Stateless)
- 사용자 상호작용 시마다 전체 스크립트가 다시 실행됨
- `st.session_state`를 통해 상태 관리 가능

## 핵심 컴포넌트 분류

### 1. 텍스트 및 데이터 표시 컴포넌트

#### 텍스트 표시
- `st.title()`: 제목
- `st.header()`: 헤더
- `st.subheader()`: 서브헤더
- `st.text()`: 일반 텍스트
- `st.markdown()`: 마크다운 텍스트
- `st.write()`: 범용 출력 함수
- `st.code()`: 코드 블록
- `st.latex()`: LaTeX 수식

#### 데이터 표시
- `st.dataframe()`: 인터랙티브 데이터프레임
- `st.table()`: 정적 테이블
- `st.metric()`: 메트릭 카드
- `st.json()`: JSON 데이터

### 2. 입력 위젯 (Input Widgets)

#### 기본 입력
- `st.text_input()`: 텍스트 입력
- `st.text_area()`: 여러 줄 텍스트
- `st.number_input()`: 숫자 입력
- `st.date_input()`: 날짜 선택
- `st.time_input()`: 시간 선택

#### 선택 위젯
- `st.selectbox()`: 드롭다운 선택
- `st.multiselect()`: 다중 선택
- `st.radio()`: 라디오 버튼
- `st.checkbox()`: 체크박스
- `st.slider()`: 슬라이더
- `st.select_slider()`: 선택 슬라이더

#### 버튼
- `st.button()`: 일반 버튼
- `st.download_button()`: 다운로드 버튼
- `st.file_uploader()`: 파일 업로드

### 3. 미디어 및 시각화 컴포넌트

#### 차트 및 그래프
- `st.line_chart()`: 선 그래프
- `st.area_chart()`: 영역 그래프
- `st.bar_chart()`: 막대 그래프
- `st.pyplot()`: Matplotlib 그래프
- `st.plotly_chart()`: Plotly 차트
- `st.altair_chart()`: Altair 차트
- `st.map()`: 지도

#### 미디어
- `st.image()`: 이미지 표시
- `st.audio()`: 오디오 재생
- `st.video()`: 비디오 재생

### 4. 레이아웃 컴포넌트

#### 컨테이너
- `st.container()`: 일반 컨테이너
- `st.empty()`: 빈 컨테이너 (나중에 채울 수 있음)
- `st.expander()`: 접을 수 있는 컨테이너

#### 열 레이아웃
- `st.columns()`: 열 분할
- `st.sidebar`: 사이드바

#### 탭
- `st.tabs()`: 탭 인터페이스

### 5. 상태 및 제어 컴포넌트

#### 상태 관리
- `st.session_state`: 세션 상태 저장소
- `st.cache_data()`: 데이터 캐싱
- `st.cache_resource()`: 리소스 캐싱

#### 제어 흐름
- `st.stop()`: 실행 중단
- `st.rerun()`: 앱 재실행

#### 알림
- `st.success()`: 성공 메시지
- `st.info()`: 정보 메시지
- `st.warning()`: 경고 메시지
- `st.error()`: 에러 메시지
- `st.exception()`: 예외 표시

#### 진행 상황
- `st.progress()`: 진행률 바
- `st.spinner()`: 로딩 스피너
- `st.balloons()`: 축하 애니메이션
- `st.snow()`: 눈 애니메이션

## 컴포넌트 사용 패턴

### 1. 기본 패턴
```python
# 입력 받기
user_name = st.text_input("이름을 입력하세요:")

# 조건부 처리
if user_name:
    st.write(f"안녕하세요, {user_name}님!")
```

### 2. 폼 패턴
```python
with st.form("my_form"):
    name = st.text_input("이름")
    age = st.number_input("나이", min_value=0, max_value=120)
    submitted = st.form_submit_button("제출")
    
    if submitted:
        st.write(f"{name}님의 나이는 {age}세입니다.")
```

### 3. 컬럼 레이아웃 패턴
```python
col1, col2, col3 = st.columns(3)

with col1:
    st.header("Column 1")
    st.write("첫 번째 열")

with col2:
    st.header("Column 2")
    st.write("두 번째 열")

with col3:
    st.header("Column 3")
    st.write("세 번째 열")
```

### 4. 사이드바 패턴
```python
# 사이드바에 컨트롤 배치
st.sidebar.title("설정")
option = st.sidebar.selectbox("옵션 선택", ["A", "B", "C"])
value = st.sidebar.slider("값 선택", 0, 100, 50)

# 메인 영역에 결과 표시
st.title("메인 콘텐츠")
st.write(f"선택된 옵션: {option}")
st.write(f"선택된 값: {value}")
```

## 컴포넌트 조합 전략

### 1. 계층적 구조
```
App
├── Header (title, description)
├── Sidebar (controls, navigation)
├── Main Content
│   ├── Input Section
│   ├── Processing Section
│   └── Output Section
└── Footer (additional info)
```

### 2. 모듈화
- 관련 기능을 함수로 분리
- 재사용 가능한 컴포넌트 생성
- 코드 가독성 향상

### 3. 반응형 디자인
- 다양한 화면 크기 고려
- 컬럼 레이아웃 활용
- 모바일 친화적 인터페이스

## 성능 최적화 팁

### 1. 캐싱 활용
```python
@st.cache_data
def load_data():
    # 데이터 로딩 로직
    return data
```

### 2. 조건부 렌더링
```python
if st.checkbox("고급 옵션 표시"):
    # 필요할 때만 렌더링
    advanced_options()
```

### 3. 세션 상태 최적화
```python
# 필요한 데이터만 세션 상태에 저장
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = process_data()
```

## 컴포넌트 선택 가이드

### 데이터 입력이 필요한 경우
- 단일 값: `text_input`, `number_input`, `selectbox`
- 다중 값: `multiselect`, `checkbox` 조합
- 범위 값: `slider`, `date_input` 범위

### 데이터 표시가 필요한 경우
- 테이블 형태: `dataframe`, `table`
- 차트 형태: `line_chart`, `bar_chart`, `plotly_chart`
- 텍스트 형태: `write`, `markdown`, `text`

### 레이아웃 구성이 필요한 경우
- 수평 분할: `columns`
- 수직 그룹핑: `container`, `expander`
- 네비게이션: `sidebar`, `tabs`

이러한 컴포넌트들을 적절히 조합하면 사용자 친화적이고 기능적인 Streamlit 애플리케이션을 만들 수 있습니다.
