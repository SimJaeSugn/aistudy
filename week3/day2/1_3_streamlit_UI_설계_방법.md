# Streamlit을 활용한 간단한 UI 설계 방법

## UI 설계 기본 원칙

### 1. 사용자 중심 설계
- 사용자의 목적과 워크플로우를 우선 고려
- 직관적이고 명확한 인터페이스 제공
- 최소한의 클릭으로 원하는 결과 도출

### 2. 정보 계층 구조
- 중요한 정보를 상단에 배치
- 관련된 기능들을 그룹화
- 시각적 계층을 통한 정보 우선순위 표현

### 3. 일관성 유지
- 동일한 기능에는 동일한 컴포넌트 사용
- 색상, 폰트, 간격의 일관성 유지
- 예측 가능한 사용자 경험 제공

## Streamlit UI 설계 패턴

### 1. 헤더-사이드바-메인 패턴
```
┌─────────────────────────────────┐
│           Header                │
├─────────┬───────────────────────┤
│         │                       │
│ Sidebar │    Main Content       │
│         │                       │
│         │                       │
└─────────┴───────────────────────┘
```

**특징:**
- 가장 일반적인 레이아웃
- 사이드바에 컨트롤, 메인에 결과 표시
- 네비게이션과 콘텐츠의 명확한 분리

**적용 사례:**
- 데이터 대시보드
- 분석 도구
- 설정이 많은 애플리케이션

### 2. 탭 기반 패턴
```
┌─────────────────────────────────┐
│           Header                │
├─────────────────────────────────┤
│ Tab1 │ Tab2 │ Tab3 │ Tab4       │
├─────────────────────────────────┤
│                                 │
│        Tab Content              │
│                                 │
└─────────────────────────────────┘
```

**특징:**
- 기능별로 탭으로 분리
- 복잡한 애플리케이션의 구조화
- 사용자가 필요한 기능에 집중 가능

**적용 사례:**
- 다기능 분석 도구
- 여러 단계의 워크플로우
- 서로 다른 데이터 뷰

### 3. 단계별 진행 패턴
```
┌─────────────────────────────────┐
│    Step 1 → Step 2 → Step 3     │
├─────────────────────────────────┤
│                                 │
│        Current Step             │
│                                 │
│         [Next Button]           │
└─────────────────────────────────┘
```

**특징:**
- 순차적 진행이 필요한 작업
- 각 단계별 명확한 안내
- 진행 상황 시각화

**적용 사례:**
- 데이터 전처리 파이프라인
- 모델 훈련 과정
- 설문조사 형태의 입력

### 4. 대시보드 패턴
```
┌─────────────────────────────────┐
│           KPI Cards             │
├─────────┬─────────┬─────────────┤
│ Chart 1 │ Chart 2 │   Chart 3   │
├─────────┴─────────┼─────────────┤
│    Data Table     │   Controls  │
└───────────────────┴─────────────┘
```

**특징:**
- 여러 정보를 한 화면에 표시
- 그리드 레이아웃 활용
- 실시간 모니터링에 적합

**적용 사례:**
- 비즈니스 대시보드
- 모니터링 시스템
- 성과 추적 도구

## UI 컴포넌트 선택 가이드

### 입력 컴포넌트 선택

#### 텍스트 입력
```python
# 짧은 텍스트
name = st.text_input("이름")

# 긴 텍스트
description = st.text_area("설명", height=100)

# 비밀번호
password = st.text_input("비밀번호", type="password")
```

#### 숫자 입력
```python
# 정확한 값
age = st.number_input("나이", min_value=0, max_value=120, value=25)

# 범위 선택
price_range = st.slider("가격 범위", 0, 1000, (200, 800))

# 단일 값 선택
rating = st.select_slider("평점", options=[1, 2, 3, 4, 5])
```

#### 선택 입력
```python
# 단일 선택
category = st.selectbox("카테고리", ["A", "B", "C"])
option = st.radio("옵션", ["Option 1", "Option 2"])

# 다중 선택
features = st.multiselect("기능 선택", ["기능1", "기능2", "기능3"])

# 체크박스
agree = st.checkbox("동의합니다")
```

### 출력 컴포넌트 선택

#### 텍스트 출력
```python
# 제목과 헤더
st.title("메인 제목")
st.header("섹션 헤더")
st.subheader("서브 헤더")

# 일반 텍스트
st.write("일반 텍스트")
st.markdown("**굵은 글씨**")

# 코드
st.code("print('Hello World')", language="python")
```

#### 데이터 출력
```python
# 테이블
st.dataframe(df)  # 인터랙티브
st.table(df)      # 정적

# 메트릭
st.metric("매출", "1,000,000원", "10%")

# JSON
st.json({"key": "value"})
```

#### 시각화
```python
# 간단한 차트
st.line_chart(data)
st.bar_chart(data)

# 고급 차트
st.plotly_chart(fig)
st.pyplot(fig)

# 지도
st.map(location_data)
```

## 레이아웃 설계 전략

### 1. 컬럼 레이아웃
```python
# 균등 분할
col1, col2, col3 = st.columns(3)

# 비율 분할
col1, col2 = st.columns([2, 1])  # 2:1 비율

# 사용 예시
with col1:
    st.header("메인 콘텐츠")
    st.write("주요 내용")

with col2:
    st.header("사이드 정보")
    st.write("부가 정보")
```

### 2. 컨테이너 활용
```python
# 일반 컨테이너
with st.container():
    st.write("그룹화된 콘텐츠")
    st.button("버튼")

# 확장 가능한 컨테이너
with st.expander("자세히 보기"):
    st.write("숨겨진 내용")
    st.dataframe(detailed_data)
```

### 3. 사이드바 활용
```python
# 사이드바에 컨트롤 배치
with st.sidebar:
    st.header("설정")
    filter_option = st.selectbox("필터", options)
    date_range = st.date_input("날짜 범위")
    
# 메인 영역은 결과 표시용
st.header("결과")
filtered_data = apply_filter(data, filter_option, date_range)
st.dataframe(filtered_data)
```

## 사용자 경험 개선 방법

### 1. 로딩 상태 표시
```python
with st.spinner("데이터를 처리하는 중..."):
    result = expensive_computation()
    
# 진행률 표시
progress_bar = st.progress(0)
for i in range(100):
    progress_bar.progress(i + 1)
    time.sleep(0.01)
```

### 2. 피드백 제공
```python
if st.button("데이터 저장"):
    try:
        save_data(data)
        st.success("데이터가 성공적으로 저장되었습니다!")
    except Exception as e:
        st.error(f"저장 중 오류가 발생했습니다: {e}")
```

### 3. 도움말 제공
```python
st.text_input(
    "이메일", 
    help="유효한 이메일 주소를 입력하세요"
)

with st.expander("사용법 안내"):
    st.write("""
    1. 데이터 파일을 업로드하세요
    2. 분석 옵션을 선택하세요
    3. 결과를 확인하세요
    """)
```

### 4. 반응형 디자인
```python
# 화면 크기에 따른 컬럼 조정
if st.sidebar.checkbox("모바일 뷰"):
    # 세로 레이아웃
    st.write("차트")
    st.line_chart(data)
    st.write("테이블")
    st.dataframe(data)
else:
    # 가로 레이아웃
    col1, col2 = st.columns(2)
    with col1:
        st.line_chart(data)
    with col2:
        st.dataframe(data)
```

## UI 설계 체크리스트

### 기능성
- [ ] 모든 필수 기능이 접근 가능한가?
- [ ] 사용자 입력 검증이 적절한가?
- [ ] 에러 처리가 되어 있는가?

### 사용성
- [ ] 직관적인 네비게이션인가?
- [ ] 로딩 시간이 적절한가?
- [ ] 도움말이 제공되는가?

### 시각적 디자인
- [ ] 정보 계층이 명확한가?
- [ ] 색상과 폰트가 일관적인가?
- [ ] 여백과 정렬이 적절한가?

### 반응성
- [ ] 다양한 화면 크기에서 작동하는가?
- [ ] 사용자 액션에 즉각적인 피드백이 있는가?
- [ ] 상태 변화가 명확하게 표시되는가?

## 실제 적용 예시

### 데이터 분석 대시보드
1. **사이드바**: 필터 옵션, 날짜 범위
2. **상단**: KPI 메트릭 카드
3. **중앙**: 주요 차트와 그래프
4. **하단**: 상세 데이터 테이블

### 머신러닝 모델 데모
1. **입력 섹션**: 모델 파라미터 조정
2. **처리 섹션**: 예측 실행 버튼
3. **결과 섹션**: 예측 결과와 시각화
4. **설명 섹션**: 모델 해석과 설명

이러한 설계 원칙과 패턴을 따르면 사용자 친화적이고 효과적인 Streamlit 애플리케이션을 만들 수 있습니다.
