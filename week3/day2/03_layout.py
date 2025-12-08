"""
Streamlit UI 레이아웃 실습
- 컬럼 레이아웃 활용
- 컨테이너와 확장 가능한 섹션
- 사이드바와 메인 영역 구성
- 탭을 이용한 콘텐츠 구성
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(
    page_title="UI 레이아웃 실습",
    page_icon="🎨",
    layout="wide"
)

# 제목
st.title("Streamlit UI 레이아웃 실습")
st.markdown("다양한 레이아웃 패턴을 실습해보세요.")

# 사이드바 설정
st.sidebar.title("레이아웃 설정")
layout_type = st.sidebar.selectbox(
    "레이아웃 유형 선택:",
    # ["기본 컬럼", "비율 컬럼", "중첩 컬럼", "컨테이너", "확장 섹션", "대시보드"]
    ["기본 컬럼", "비율 컬럼", "중첩 컬럼"]
)

# 샘플 데이터 생성
@st.cache_data
def generate_sample_data():
    dates = pd.date_range('2024-01-01', periods=30, freq='D')
    data = {
        'date': dates,
        'sales': np.random.randint(100, 1000, 30),
        'profit': np.random.randint(10, 100, 30),
        'customers': np.random.randint(50, 200, 30)
    }
    return pd.DataFrame(data)

df = generate_sample_data()

# 레이아웃 유형별 구현
if layout_type == "기본 컬럼":
    st.header("기본 컬럼 레이아웃")
    st.write("균등하게 분할된 컬럼 레이아웃입니다.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("첫 번째 컬럼")
        st.write("여기는 첫 번째 컬럼입니다.")
        st.metric("총 매출", f"${df['sales'].sum():,}", "12%")
        
    with col2:
        st.subheader("두 번째 컬럼")
        st.write("여기는 두 번째 컬럼입니다.")
        st.metric("평균 이익", f"${df['profit'].mean():.0f}", "5%")
        
    with col3:
        st.subheader("세 번째 컬럼")
        st.write("여기는 세 번째 컬럼입니다.")
        st.metric("총 고객", f"{df['customers'].sum():,}", "8%")

elif layout_type == "비율 컬럼":
    st.header("비율 컬럼 레이아웃")
    st.write("2:1:1 비율로 분할된 컬럼 레이아웃입니다.")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.subheader("메인 콘텐츠 (넓은 영역)")
        fig = px.line(df, x='date', y='sales', title='일별 매출 추이')
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader("사이드 정보 1")
        st.write("부가 정보를 표시합니다.")
        st.bar_chart(df.set_index('date')['profit'])
        
    with col3:
        st.subheader("사이드 정보 2")
        st.write("추가 정보를 표시합니다.")
        st.line_chart(df.set_index('date')['customers'])

elif layout_type == "중첩 컬럼":
    st.header("중첩 컬럼 레이아웃")
    st.write("컬럼 안에 또 다른 컬럼을 만든 레이아웃입니다.")
    
    # 첫 번째 레벨 컬럼
    left_col, right_col = st.columns([3, 2])
    
    with left_col:
        st.subheader("메인 영역")
        
        # 중첩된 컬럼
        sub_col1, sub_col2 = st.columns(2)
        with sub_col1:
            st.write("서브 컬럼 1")
            st.area_chart(df.set_index('date')['sales'])
        with sub_col2:
            st.write("서브 컬럼 2")
            st.bar_chart(df.set_index('date')['profit'])
    
    with right_col:
        st.subheader("사이드 영역")
        st.write("오른쪽 사이드 영역입니다.")
        
        # 메트릭 표시
        st.metric("최고 매출", f"${df['sales'].max():,}")
        st.metric("최저 매출", f"${df['sales'].min():,}")
        st.metric("매출 편차", f"${df['sales'].std():.0f}")

# elif layout_type == "컨테이너":
#     st.header("컨테이너 레이아웃")
#     st.write("컨테이너를 사용하여 콘텐츠를 그룹화합니다.")
    
#     # 첫 번째 컨테이너
#     with st.container():
#         st.subheader("데이터 개요")
#         col1, col2, col3, col4 = st.columns(4)
#         with col1:
#             st.metric("데이터 포인트", len(df))
#         with col2:
#             st.metric("평균 매출", f"${df['sales'].mean():.0f}")
#         with col3:
#             st.metric("총 이익", f"${df['profit'].sum():,}")
#         with col4:
#             st.metric("평균 고객", f"{df['customers'].mean():.0f}")
    
#     st.divider()
    
#     # 두 번째 컨테이너
#     with st.container():
#         st.subheader("상세 분석")
#         tab1, tab2 = st.tabs(["매출 분석", "고객 분석"])
        
#         with tab1:
#             fig = px.scatter(df, x='date', y='sales', size='profit', 
#                            title='매출과 이익의 상관관계')
#             st.plotly_chart(fig, use_container_width=True)
        
#         with tab2:
#             fig = px.histogram(df, x='customers', nbins=10, title='고객 수 분포')
#             st.plotly_chart(fig, use_container_width=True)

# elif layout_type == "확장 섹션":
#     st.header("확장 가능한 섹션")
#     st.write("필요에 따라 펼치거나 접을 수 있는 섹션입니다.")
    
#     # 기본 정보는 항상 표시
#     st.subheader("기본 정보")
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.metric("총 매출", f"${df['sales'].sum():,}")
#     with col2:
#         st.metric("총 이익", f"${df['profit'].sum():,}")
#     with col3:
#         st.metric("총 고객", f"{df['customers'].sum():,}")
    
#     # 확장 가능한 섹션들
#     with st.expander("상세 통계 보기"):
#         st.write("데이터의 상세 통계 정보입니다.")
#         st.dataframe(df.describe())
    
#     with st.expander("차트 보기"):
#         st.write("다양한 차트로 데이터를 시각화합니다.")
#         chart_col1, chart_col2 = st.columns(2)
#         with chart_col1:
#             st.line_chart(df.set_index('date')['sales'])
#         with chart_col2:
#             st.bar_chart(df.set_index('date')['profit'])
    
#     with st.expander("원본 데이터 보기"):
#         st.write("전체 원본 데이터를 확인할 수 있습니다.")
#         st.dataframe(df)

# elif layout_type == "대시보드":
#     st.header("대시보드 레이아웃")
#     st.write("실제 대시보드와 같은 복합적인 레이아웃입니다.")
    
#     # KPI 카드 섹션
#     st.subheader("핵심 지표")
#     kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
#     with kpi_col1:
#         st.metric(
#             "총 매출", 
#             f"${df['sales'].sum():,}", 
#             f"{((df['sales'].sum() - 15000) / 15000 * 100):+.1f}%"
#         )
#     with kpi_col2:
#         st.metric(
#             "평균 일매출", 
#             f"${df['sales'].mean():.0f}", 
#             f"{((df['sales'].mean() - 500) / 500 * 100):+.1f}%"
#         )
#     with kpi_col3:
#         st.metric(
#             "총 이익", 
#             f"${df['profit'].sum():,}", 
#             f"{((df['profit'].sum() - 1500) / 1500 * 100):+.1f}%"
#         )
#     with kpi_col4:
#         st.metric(
#             "평균 고객수", 
#             f"{df['customers'].mean():.0f}", 
#             f"{((df['customers'].mean() - 120) / 120 * 100):+.1f}%"
#         )
    
#     st.divider()
    
#     # 차트 섹션
#     chart_col1, chart_col2 = st.columns([2, 1])
    
#     with chart_col1:
#         st.subheader("매출 추이")
#         fig = px.line(df, x='date', y='sales', title='일별 매출 추이')
#         fig.add_scatter(x=df['date'], y=df['profit']*10, 
#                        mode='lines', name='이익 (x10)', yaxis='y2')
#         fig.update_layout(yaxis2=dict(overlaying='y', side='right'))
#         st.plotly_chart(fig, use_container_width=True)
    
#     with chart_col2:
#         st.subheader("매출 분포")
#         fig = px.pie(values=[df['sales'].sum(), df['profit'].sum()], 
#                     names=['매출', '이익'], title='매출 vs 이익')
#         st.plotly_chart(fig, use_container_width=True)
        
#         st.subheader("고객 통계")
#         st.write(f"최대 고객수: {df['customers'].max()}")
#         st.write(f"최소 고객수: {df['customers'].min()}")
#         st.write(f"표준편차: {df['customers'].std():.1f}")
    
#     # 데이터 테이블 섹션
#     with st.expander("상세 데이터 테이블"):
#         st.dataframe(
#             df.style.highlight_max(axis=0),
#             use_container_width=True
#         )

# 사이드바에 추가 정보
st.sidebar.markdown("---")
st.sidebar.subheader("레이아웃 팁")
st.sidebar.info("""
- 컬럼은 최대 10개까지 생성 가능
- 비율은 리스트로 지정 가능
- 컨테이너는 중첩 가능
- 확장 섹션으로 공간 절약
""")

st.sidebar.subheader("코드 예제")
if st.sidebar.button("코드 보기"):
    st.sidebar.code("""
# 기본 컬럼
col1, col2 = st.columns(2)

# 비율 컬럼
col1, col2 = st.columns([3, 1])

# 컨테이너
with st.container():
    st.write("그룹화된 콘텐츠")

# 확장 섹션
with st.expander("제목"):
    st.write("숨겨진 콘텐츠")
    """, language="python")

# 하단 정보
st.markdown("---")
st.caption("이 예제는 다양한 Streamlit 레이아웃 패턴을 보여줍니다. 실제 프로젝트에서 적절한 패턴을 선택하여 사용하세요.")
