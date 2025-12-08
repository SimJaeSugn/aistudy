"""
Streamlit 인터랙티브 기능 실습
- 세션 상태 관리
- 폼과 사용자 입력 처리
- 실시간 데이터 업데이트
- 조건부 렌더링과 동적 콘텐츠
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="인터랙티브 기능 실습",
    page_icon="⚡",
    layout="wide"
)

st.title("Streamlit 인터랙티브 기능 실습")
st.write("사용자와 상호작용하는 다양한 기능들을 실습해보세요.")

# 세션 상태 초기화 함수
def initialize_session_state():
    """세션 상태를 안전하게 초기화합니다."""
    if 'counter' not in st.session_state:
        st.session_state.counter = 0
    
    if 'user_data' not in st.session_state:
        st.session_state.user_data = []
    
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ""
    
    if 'user_theme' not in st.session_state:
        st.session_state.user_theme = "밝은 테마"
    
    # 데이터 관리용 초기 데이터
    if 'items' not in st.session_state:
        st.session_state.items = [
            {"id": 1, "이름": "샘플 항목 1", "값": 150, "상태": "활성"},
            {"id": 2, "이름": "샘플 항목 2", "값": 250, "상태": "비활성"},
            {"id": 3, "이름": "샘플 항목 3", "값": 300, "상태": "활성"},
        ]
    
    if 'next_id' not in st.session_state:
        st.session_state.next_id = 4
    
    # items가 리스트인지 확인하고, 아니면 초기화
    if not isinstance(st.session_state.items, list):
        st.session_state.items = [
            {"id": 1, "이름": "샘플 항목 1", "값": 150, "상태": "활성"},
            {"id": 2, "이름": "샘플 항목 2", "값": 250, "상태": "비활성"},
            {"id": 3, "이름": "샘플 항목 3", "값": 300, "상태": "활성"},
        ]

# 세션 상태 초기화 실행
initialize_session_state()

# 탭으로 기능 구분
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "세션 상태", "폼 처리", "실시간 업데이트", "조건부 렌더링", "데이터 관리"
])

# 탭 1: 세션 상태 관리
with tab1:
    st.header("세션 상태 관리")
    st.write("세션 상태를 사용하여 앱의 상태를 유지합니다.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("카운터 예제")
        st.write(f"현재 카운터 값: {st.session_state.counter}")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if st.button("증가", key="inc"):
                st.session_state.counter += 1
                st.rerun()
        with col_b:
            if st.button("감소", key="dec"):
                st.session_state.counter -= 1
                st.rerun()
        with col_c:
            if st.button("초기화", key="reset"):
                st.session_state.counter = 0
                st.rerun()
    
    with col2:
        st.subheader("사용자 설정")
        
        name = st.text_input("이름", value=st.session_state.user_name, key="name_input")
        theme = st.selectbox("테마 선택", ["밝은 테마", "어두운 테마"], 
                           index=0 if st.session_state.user_theme == "밝은 테마" else 1)
        
        if st.button("설정 저장"):
            st.session_state.user_name = name
            st.session_state.user_theme = theme
            st.success(f"{name}님의 설정이 저장되었습니다! (테마: {theme})")
        
        if st.session_state.user_name:
            st.info(f"안녕하세요, {st.session_state.user_name}님! 현재 테마: {st.session_state.user_theme}")

# 탭 2: 폼 처리
with tab2:
    st.header("폼과 사용자 입력 처리")
    st.write("폼을 사용하여 여러 입력을 한 번에 처리합니다.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("사용자 정보 입력")
        with st.form("user_form"):
            name = st.text_input("이름")
            age = st.number_input("나이", min_value=0, max_value=120, value=25)
            email = st.text_input("이메일")
            interests = st.multiselect("관심사", 
                                     ["프로그래밍", "데이터 분석", "머신러닝", "웹 개발", "디자인"])
            agree = st.checkbox("개인정보 처리에 동의합니다")
            
            submitted = st.form_submit_button("제출")
            
            if submitted:
                if name and email and agree:
                    user_info = {
                        "이름": name,
                        "나이": age,
                        "이메일": email,
                        "관심사": interests,
                        "제출시간": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    st.session_state.user_data.append(user_info)
                    st.success("정보가 성공적으로 제출되었습니다!")
                else:
                    st.error("모든 필수 항목을 입력하고 동의해주세요.")
    
    with col2:
        st.subheader("제출된 데이터")
        if st.session_state.user_data and len(st.session_state.user_data) > 0:
            try:
                df = pd.DataFrame(st.session_state.user_data)
                st.dataframe(df, use_container_width=True)
                
                if st.button("데이터 초기화"):
                    st.session_state.user_data = []
                    st.rerun()
            except Exception as e:
                st.error(f"데이터 표시 중 오류가 발생했습니다: {str(e)}")
                st.session_state.user_data = []
                st.rerun()
        else:
            st.info("아직 제출된 데이터가 없습니다.")

# 탭 3: 실시간 업데이트
with tab3:
    st.header("실시간 데이터 업데이트")
    st.write("자동으로 업데이트되는 데이터를 시뮬레이션합니다.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("실시간 차트")
        
        # 실시간 데이터 시뮬레이션
        if st.button("실시간 업데이트 시작"):
            chart_placeholder = st.empty()
            status_placeholder = st.empty()
            
            for i in range(5):  # 10회에서 5회로 줄임
                # 랜덤 데이터 생성
                data = pd.DataFrame({
                    'x': range(20),
                    'y': np.random.randn(20).cumsum()
                })
                
                # 차트 업데이트
                fig = px.line(data, x='x', y='y', title=f'실시간 데이터 (업데이트 {i+1}/5)')
                chart_placeholder.plotly_chart(fig, use_container_width=True)
                
                # 상태 업데이트
                status_placeholder.write(f"업데이트 {i+1}/5 완료")
                
                time.sleep(0.5)  # 1초에서 0.5초로 줄임
            
            status_placeholder.success("실시간 업데이트 완료!")
    
    with col2:
        st.subheader("진행률 표시")
        
        if st.button("작업 시뮬레이션"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(50):  # 100회에서 50회로 줄임
                progress_bar.progress((i + 1) * 2)  # 2%씩 증가
                status_text.text(f'작업 진행률: {(i+1)*2}%')
                time.sleep(0.1)  # 0.05초에서 0.1초로 조정
            
            status_text.text('작업 완료!')
            st.balloons()

# 탭 4: 조건부 렌더링
with tab4:
    st.header("조건부 렌더링과 동적 콘텐츠")
    st.write("사용자 선택에 따라 다른 콘텐츠를 표시합니다.")
    
    # 페이지 네비게이션
    st.subheader("페이지 네비게이션")
    page_options = ["홈", "프로필", "설정", "도움말"]
    selected_page = st.selectbox("페이지 선택", page_options)
    
    # 선택된 페이지에 따른 콘텐츠 표시
    if selected_page == "홈":
        st.write("홈페이지에 오신 것을 환영합니다!")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("총 사용자", "1,234", "12%")
        with col2:
            st.metric("활성 세션", "89", "5%")
        with col3:
            st.metric("일일 방문", "456", "8%")
    
    elif selected_page == "프로필":
        st.write("사용자 프로필 페이지입니다.")
        if st.session_state.user_name:
            st.write(f"이름: {st.session_state.user_name}")
            st.write(f"테마: {st.session_state.user_theme}")
        else:
            st.warning("먼저 '세션 상태' 탭에서 사용자 정보를 설정해주세요.")
    
    elif selected_page == "설정":
        st.write("설정 페이지입니다.")
        
        # 동적 설정 옵션
        notification = st.checkbox("알림 받기")
        if notification:
            notification_type = st.radio("알림 유형", ["이메일", "SMS", "푸시"])
            st.write(f"선택된 알림 유형: {notification_type}")
        
        language = st.selectbox("언어 설정", ["한국어", "English", "日本語"])
        if language != "한국어":
            st.info(f"언어가 {language}로 설정되었습니다.")
    
    elif selected_page == "도움말":
        st.write("도움말 페이지입니다.")
        
        help_category = st.selectbox("도움말 카테고리", 
                                   ["시작하기", "기능 설명", "문제 해결", "연락처"])
        
        if help_category == "시작하기":
            st.markdown("""
            ### 시작하기 가이드
            1. 사용자 정보를 입력하세요
            2. 원하는 기능을 선택하세요
            3. 결과를 확인하세요
            """)
        elif help_category == "기능 설명":
            st.markdown("""
            ### 주요 기능
            - 세션 상태 관리
            - 폼 처리
            - 실시간 업데이트
            - 조건부 렌더링
            """)
        elif help_category == "문제 해결":
            st.markdown("""
            ### 자주 묻는 질문
            **Q: 데이터가 사라져요**
            A: 페이지를 새로고침하면 세션 상태가 초기화됩니다.
            
            **Q: 업데이트가 안 돼요**
            A: 브라우저를 새로고침해보세요.
            """)
        else:
            st.markdown("""
            ### 연락처
            - 이메일: support@example.com
            - 전화: 02-1234-5678
            """)

# 탭 5: 데이터 관리
with tab5:
    st.header("동적 데이터 관리")
    st.write("사용자가 데이터를 추가, 수정, 삭제할 수 있습니다.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("항목 추가")
        with st.form("add_item"):
            new_name = st.text_input("항목 이름")
            new_value = st.number_input("값", min_value=0, value=0)
            new_status = st.selectbox("상태", ["활성", "비활성"])
            
            if st.form_submit_button("추가"):
                if new_name:
                    new_item = {
                        "id": st.session_state.next_id,
                        "이름": new_name,
                        "값": new_value,
                        "상태": new_status
                    }
                    st.session_state.items.append(new_item)
                    st.session_state.next_id += 1
                    st.success("항목이 추가되었습니다!")
                    st.rerun()
    
    with col2:
        st.subheader("항목 목록")
        
        # 안전한 데이터 확인
        items_data = getattr(st.session_state, 'items', [])
        if not isinstance(items_data, list):
            items_data = []
            st.session_state.items = []
        
        if items_data and len(items_data) > 0:
            try:
                df = pd.DataFrame(items_data)
                
                # 편집 가능한 데이터 표시
                edited_df = st.data_editor(
                    df,
                    column_config={
                        "상태": st.column_config.SelectboxColumn(
                            "상태",
                            options=["활성", "비활성"]
                        )
                    },
                    disabled=["id"],
                    use_container_width=True,
                    key="data_editor"
                )
                
                # 변경사항 저장
                if st.button("변경사항 저장", key="save_changes"):
                    st.session_state.items = edited_df.to_dict('records')
                    st.success("변경사항이 저장되었습니다!")
                    st.rerun()
                
                # 선택된 항목 삭제
                st.subheader("항목 삭제")
                if len(items_data) > 0:
                    item_options = [f"{item.get('id', 'N/A')}: {item.get('이름', 'Unknown')}" for item in items_data]
                    item_to_delete = st.selectbox(
                        "삭제할 항목 선택",
                        options=item_options,
                        key="delete_selector"
                    )
                    
                    if st.button("선택된 항목 삭제", type="secondary", key="delete_item"):
                        try:
                            item_id = int(item_to_delete.split(":")[0])
                            st.session_state.items = [item for item in st.session_state.items if item.get('id') != item_id]
                            st.success("항목이 삭제되었습니다!")
                            st.rerun()
                        except (ValueError, AttributeError) as e:
                            st.error(f"삭제 중 오류가 발생했습니다: {str(e)}")
                            
            except Exception as e:
                st.error(f"데이터 표시 중 오류가 발생했습니다: {str(e)}")
                st.write("세션 상태를 초기화합니다...")
                initialize_session_state()
                st.rerun()
        else:
            st.info("항목이 없습니다. 새 항목을 추가해보세요.")
            st.write("초기 데이터를 로드하려면 페이지를 새로고침하세요.")
    
    # 통계 표시
    stats_items = getattr(st.session_state, 'items', [])
    if isinstance(stats_items, list) and len(stats_items) > 0:
        st.subheader("통계")
        try:
            df = pd.DataFrame(stats_items)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("총 항목", len(df))
            with col2:
                active_count = len(df[df['상태'] == '활성']) if '상태' in df.columns else 0
                st.metric("활성 항목", active_count)
            with col3:
                total_value = df['값'].sum() if '값' in df.columns else 0
                st.metric("총 값", total_value)
            with col4:
                avg_value = df['값'].mean() if '값' in df.columns and len(df) > 0 else 0
                st.metric("평균 값", f"{avg_value:.1f}")
        except Exception as e:
            st.error(f"통계 계산 중 오류가 발생했습니다: {str(e)}")
            st.write("통계를 표시할 수 없습니다. 데이터를 확인해주세요.")

# 사이드바 정보
st.sidebar.header("인터랙티브 기능 가이드")
st.sidebar.markdown("""
### 주요 기능
1. **세션 상태**: 앱 상태 유지
2. **폼 처리**: 여러 입력 한번에 처리
3. **실시간 업데이트**: 동적 콘텐츠
4. **조건부 렌더링**: 상황별 다른 화면
5. **데이터 관리**: CRUD 기능

### 팁
- `st.session_state`로 상태 관리
- `st.form`으로 입력 그룹화
- `st.rerun()`으로 화면 새로고침
- 조건문으로 동적 콘텐츠 구성
""")

st.sidebar.info("각 탭에서 다양한 인터랙티브 기능을 체험해보세요!")
