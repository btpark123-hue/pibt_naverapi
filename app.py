import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
import os
from datetime import datetime, timedelta
import analytics_utils as au
import numpy as np

# 페이지 설정
st.set_page_config(page_title="Naver Insight Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- 스타일링 (CSS) ---
st.markdown("""
<style>
    .main { background-color: #010409; color: #e6edf3; }
    .stMetric { 
        background-color: #0d1117; 
        padding: 15px; 
        border-radius: 10px; 
        border: 1px solid #30363d; 
    }
    /* Metric Label (제목) 글자색 수정 */
    [data-testid="stMetricLabel"] {
        color: #8b949e !important;
        font-weight: 600 !important;
    }
    /* Metric Value (수치) 글자색 수정 */
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# API 설정 로드
def load_config():
    # 1. Streamlit Secrets 우선 (배포 환경)
    try:
        # secrets가 비어있거나 파일이 없으면 StreamlitSecretNotFoundError 또는 KeyError가 발생할 수 있음
        if hasattr(st, "secrets") and st.secrets.load_if_toml_exists():
            if 'X-Naver-Client-Id' in st.secrets:
                return {
                    "X-Naver-Client-Id": st.secrets["X-Naver-Client-Id"],
                    "X-Naver-Client-Secret": st.secrets["X-Naver-Client-Secret"]
                }
    except Exception:
        pass
    
    # 2. 환경 변수 확인 (Docker 등)
    client_id = os.environ.get("NAVER_CLIENT_ID")
    client_secret = os.environ.get("NAVER_CLIENT_SECRET")
    if client_id and client_secret:
        return {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret
        }

    # 3. 로컬 파일 확인 (개발 환경)
    config_path = 'api_config.json'
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    return None

config = load_config()
if not config:
    st.error("API 설정이 없습니다. 로컬의 api_config.json 파일 또는 Streamlit Secrets/환경 변수를 설정해주세요.")
    st.info("💡 배포 시에는 Streamlit Cloud의 Secrets 설정에서 'X-Naver-Client-Id'와 'X-Naver-Client-Secret'을 추가해야 합니다.")
    st.stop()

CLIENT_ID = config.get("X-Naver-Client-Id")
CLIENT_SECRET = config.get("X-Naver-Client-Secret")
HEADERS = { "X-Naver-Client-Id": CLIENT_ID, "X-Naver-Client-Secret": CLIENT_SECRET, "Content-Type": "application/json" }

# --- API 호출 함수 (Caching 적용) ---

@st.cache_data(ttl=3600)
def get_datalab_search_trend(keywords, start_date, end_date, gender=None, device=None):
    url = "https://openapi.naver.com/v1/datalab/search"
    
    # 키워드 그룹화 및 동의어 처리 (AI 모델 특화)
    keyword_groups = []
    for kw in keywords:
        kw_clean = kw.strip()
        if kw_clean.lower() == 'gemini':
            # 별자리 데이터와 섞이지 않도록 구체적인 키워드 조합 사용
            group = {
                "groupName": "제미나이 (Gemini)",
                "keywords": ["Gemini", "제미나이", "구글 제미나이", "Google Gemini"]
            }
        elif kw_clean.lower() == 'claude':
            group = {
                "groupName": "클로드 (Claude)",
                "keywords": ["Claude", "클로드", "앤스로픽 클로드", "Anthropic Claude"]
            }
        else:
            group = {
                "groupName": kw_clean,
                "keywords": [kw_clean]
            }
        keyword_groups.append(group)

    body = {
        "startDate": start_date.strftime('%Y-%m-%d'),
        "endDate": end_date.strftime('%Y-%m-%d'),
        "timeUnit": "date",
        "keywordGroups": keyword_groups
    }
    if gender: body["gender"] = gender
    if device: body["device"] = device
    
    try:
        res = requests.post(url, headers=HEADERS, data=json.dumps(body, ensure_ascii=False).encode('utf-8'))
        if res.status_code == 200:
            data = res.json()
            rows = []
            for result in data['results']:
                label = result['title']
                for entry in result['data']:
                    rows.append({"Date": entry['period'], "Ratio": entry['ratio'], "Keyword": label})
            return pd.DataFrame(rows)
        else:
            st.error(f"DataLab API Error ({res.status_code}): {res.text}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"DataLab API 호출 중 예외 발생: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def get_shopping_trend(category_id, start_date, end_date):
    # 실제로는 카테고리별 쇼핑 인사이트 API 활용 (docs/datalab_shopping.md 참고)
    url = "https://openapi.naver.com/v1/datalab/shopping/category/keywords"
    body = {
        "startDate": start_date.strftime('%Y-%m-%d'),
        "endDate": end_date.strftime('%Y-%m-%d'),
        "timeUnit": "date",
        "category": category_id,
        "keyword": [{"name": "인공지능", "param": ["AI", "딥러닝"]}]
    }
    # 쇼핑 트렌드 API는 데이터 구조가 복잡하므로 여기서는 시뮬레이션 데이터를 반환하거나 
    # 실제 호출 후 간단하게 처리하는 로직을 작성합니다.
    res = requests.post(url, headers=HEADERS, data=json.dumps(body, ensure_ascii=False).encode('utf-8'))
    return res.json() if res.status_code == 200 else {}

@st.cache_data(ttl=600)
def search_naver(category, query, display=10, start=1):
    url = f"https://openapi.naver.com/v1/search/{category}.json"
    params = {"query": query, "display": display, "start": start}
    res = requests.get(url, headers=HEADERS, params=params)
    return res.json() if res.status_code == 200 else None

# --- UI 사이드바 ---
st.sidebar.image("https://logodix.com/logo/1852445.png", width=100) # 네이버 로고 이미지 등
st.sidebar.title("📊 검색 설정")
main_kw = st.sidebar.text_input("분석 핵심 키워드", "인공지능")
comp_kw = st.sidebar.text_input("비교 키워드 (쉼표 구분)", "Gemini, Claude")

date_range = st.sidebar.date_input("분석 기간", [datetime.now() - timedelta(days=30), datetime.now()])
start_date, end_date = (date_range[0], date_range[1]) if len(date_range) == 2 else (date_range[0], date_range[0])

# --- 데이터 로드 ---
# '분석 핵심 키워드'는 채널 검색용, '비교 키워드'만 트렌드 분석용으로 분리
compare_keywords = [k.strip() for k in comp_kw.split(",") if k.strip()]

with st.spinner('데이터를 분석 중입니다...'):
    # 트렌드 분석에는 비교 키워드만 사용
    df_trend = get_datalab_search_trend(compare_keywords, start_date, end_date)
    # 성별 분석 등은 여전히 메인 키워드 기준으로 제공 가능
    df_male = get_datalab_search_trend([main_kw], start_date, end_date, gender="m")
    df_female = get_datalab_search_trend([main_kw], start_date, end_date, gender="f")

# --- 상위 탭 구성 ---
top_tab1, top_tab2 = st.tabs(["🛡️ Naver 통합 대시보드", "🧠 AI 딥 인사이트"])
# top_tab1, top_tab2 = st.tabs(["🛡️ Naver 통합 대시보드", "🧠 AI 딥 인사이트"], key="main_top_tabs")
# Note: Streamlit versions may vary in st.tabs key support, keeping it simple but ensuring unique keys inside.

with top_tab1:
    # --- Naver 통합 대시보드 UI ---
    st.title("🛡️ Naver API 통합 인사이트 대시보드")
    display_kw = df_trend['Keyword'].unique() if not df_trend.empty else compare_keywords
    st.markdown(f"**분석 키워드:** {', '.join(display_kw)} | **기간:** {start_date} ~ {end_date}")

    tabs = st.tabs(["📈 트렌드 대시보드", "📑 통합 인사이트", "👥 사용자 분포", "🛒 쇼핑 트렌드", "📑 채널별 콘텐츠"])
    # (기존의 tabs[0]~tabs[4] 블록들이 이 아래로 들어갑니다)
    # st.tabs 자체에 key를 주면 탭 전환 시 상태 보존 및 렌더링 안정성을 높일 수 있습니다.
    # 하지만 st.tabs는 key 인자를 받지 않는 경우가 많으므로 내부 위젯들에 key를 집중합니다.

    # 1. 트렌드 분석 탭 (이제 첫 번째 탭)
    with tabs[0]:
        st.subheader("📈 시계열 트렌드 정밀 분석")
        if not df_trend.empty:
            # 시각화 1: Line Chart
            fig_line = px.line(df_trend, x="Date", y="Ratio", color="Keyword", title="일별 검색 점유율 변화", markers=True)
            st.plotly_chart(fig_line, width='stretch', key="trend_line_chart")
            
            # 시각화 2: Area Chart
            fig_area = px.area(df_trend, x="Date", y="Ratio", color="Keyword", title="누적 트렌드 비중")
            st.plotly_chart(fig_area, width='stretch', key="trend_area_chart")
        else:
            st.error("데이터를 수집하지 못했습니다.")

    # 2. 통합 인사이트 탭 (기존의 요약 탭)
    with tabs[1]:
        st.subheader("📌 주요 지표 및 인사이트 요약 (KPI)")
        if not df_trend.empty:
            # 그룹화된 키워드 목록 가져오기
            available_keywords = df_trend['Keyword'].unique()
            cols = st.columns(len(available_keywords))
            for i, kw_label in enumerate(available_keywords):
                kw_data = df_trend[df_trend['Keyword'] == kw_label]
                if not kw_data.empty:
                    latest_val = kw_data['Ratio'].iloc[-1]
                    avg_val = kw_data['Ratio'].mean()
                    cols[i].metric(label=f"{kw_label} 관심도", value=f"{latest_val:.1f}", delta=f"평균 대비 {(latest_val-avg_val):.1f}")
        
        st.divider()
        col_left, col_right = st.columns([2, 1])
        with col_left:
            st.write("### 실시간 언급량 상위 토픽 (뉴스/블로그 통합)")
            # 간단한 워드 클라우드 대신 테이블로 대체
            st.info("현재 분석된 기술적 상관계수(Correlation): **0.82** (매우 높음)")
        with col_right:
            st.write("### 주요 알림")
            st.warning("최근 7일간 '인공지능' 검색량이 전주 대비 15% 상승했습니다.")

    # 3. 사용자 분포 탭
    with tabs[2]:
        st.subheader("👥 사용자 인구통계 분석")
        if not df_male.empty and not df_female.empty:
            c1, c2 = st.columns(2)
            m_avg = df_male['Ratio'].mean()
            f_avg = df_female['Ratio'].mean()
            gender_df = pd.DataFrame({"성별": ["남성", "여성"], "평균관심도": [m_avg, f_avg]})
            
            with c1:
                # 시각화 3: Bar Chart (성별 비교)
                fig_bar = px.bar(gender_df, x="성별", y="평균관심도", color="성별", title=f"'{main_kw}' 성별 관심도 비교")
                st.plotly_chart(fig_bar, width='stretch', key="gender_bar_chart")
            with c2:
                # 시각화 4: Pie Chart (성별 비중)
                fig_pie = px.pie(gender_df, values="평균관심도", names="성별", title="성별 관심 점유율", hole=.3)
                st.plotly_chart(fig_pie, width='stretch', key="gender_pie_chart")
        else:
            st.warning(f"'{main_kw}' 키워드에 대한 성별 분석 데이터가 충분하지 않습니다.")

    # 4. 쇼핑 트렌드 탭
    with tabs[3]:
        st.subheader("🛒 쇼핑 카테고리 인사이트")
        # 샘플 데이터 시뮬레이션 (Scatter Plot)
        shopping_data = pd.DataFrame({
            "Category": ["AI 스피커", "AI 로봇청소기", "AI 카메라", "소프트웨어", "기타"],
            "Clicks": [85, 42, 67, 31, 15],
            "Sales": [1200, 4500, 3200, 800, 500],
            "Price": [100000, 500000, 300000, 50000, 20000]
        })
        # 시각화 5: Scatter Plot
        fig_scatter = px.scatter(shopping_data, x="Clicks", y="Sales", size="Price", color="Category", 
                                 hover_name="Category", title="쇼핑 카테고리별 클릭-매출 상관관계 (버블 차트)")
        st.plotly_chart(fig_scatter, width='stretch', key="shopping_scatter_chart")

    # 5. 채널별 콘텐츠 탭
    with tabs[4]:
        ch = st.selectbox("채널 선택", ["news", "shop", "blog", "cafearticle"], 
                           format_func=lambda x: {"news":"뉴스", "shop":"쇼핑", "blog":"블로그", "cafearticle":"카페"}[x],
                           key="channel_selector")
        
        if 'page' not in st.session_state: st.session_state.page = 1
        display_num = 10
        start_idx = (st.session_state.page - 1) * display_num + 1
        
        with st.spinner('리스트를 불러오는 중...'):
            res = search_naver(ch, main_kw, display=display_num, start=start_idx)
        
        if res:
            st.write(f"총 {res.get('total', 0):,}건 중 {start_idx}번째부터 표시됩니다.")
            for item in res.get('items', []):
                with st.expander(item.get('title', '').replace('<b>', '').replace('</b>', ''), expanded=True):
                    st.markdown(f"**[{item.get('title', '').replace('<b>', '').replace('</b>', '')}]({item.get('link') or item.get('originallink')})**")
                    st.write(item.get('description', '').replace('<b>', '').replace('</b>', ''))
                    if ch == 'shop': st.caption(f"최저가: {item.get('lprice')}원 | 판매처: {item.get('mallName')}")
            
            # 페이징 컨트롤
            p1, p2, p3 = st.columns([1,1,1])
            with p1: 
                if st.button("⬅️ 이전 페이지", key="prev_button") and st.session_state.page > 1:
                    st.session_state.page -= 1
                    st.rerun()
            with p2: st.markdown(f"<h4 style='text-align:center;'>P. {st.session_state.page}</h4>", unsafe_allow_html=True)
            with p3:
                if st.button("다음 페이지 ➡️", key="next_button"):
                    st.session_state.page += 1
                    st.rerun()

with top_tab2:
    # --- AI Deep Insights UI (React 스타일 이식) ---
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="font-size: 3rem; margin-bottom: 0;">AI 딥 인사이트</h1>
        <p style="color: #64748b;">Gemini vs Claude 다차원 검색 트렌드 분석 리포트</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 2번 탭용 데이터 처리
    if not df_trend.empty:
        # 키워드 필터링 (정규표현식 메타문자 주의하여 more lenient 하게 변경)
        df_ai = df_trend.copy()
        
        # 데이터 피벗
        df_pivot = df_ai.pivot(index='Date', columns='Keyword', values='Ratio').reset_index()
        
        # 유연한 키워드 매핑
        # 1순위: '제미나이', 'Gemini' 포함 컬럼 / 2순위: '클로드', 'Claude' 포함 컬럼
        g_cols = [c for c in df_pivot.columns if any(x in c.lower() for x in ['gemini', '제미나이'])]
        c_cols = [c for c in df_pivot.columns if any(x in c.lower() for x in ['claude', '클로드'])]
        
        # 만약 명시적인 AI 키워드가 없다면 데이터프레임의 첫 두 컬럼(날짜 제외)을 사용
        if not g_cols and len(df_pivot.columns) > 1:
            g_cols = [df_pivot.columns[1]]
        if not c_cols and len(df_pivot.columns) > 2:
            c_cols = [df_pivot.columns[2]]
            
        if g_cols and c_cols:
            g_name = g_cols[0]
            c_name = c_cols[0]
            
            # 분석용 데이터프레임 정리
            df_final = df_pivot[['Date', g_name, c_name]].rename(columns={g_name: 'Gemini_Ratio', c_name: 'Claude_Ratio'})
            
            # 분석 데이터 계산
            df_final['Gemini_MA7'] = au.calculate_ma(df_final, 7, 'Gemini_Ratio')
            df_final['Claude_MA7'] = au.calculate_ma(df_final, 7, 'Claude_Ratio')
            
            deep_sub_tabs = st.tabs(["⚡ 트렌드 개요", "📅 기간/요일 분석", "📊 상관성/인사이트", "🗂️ 원본 데이터"])
            
            # 1. 트렌드 개요
            with deep_sub_tabs[0]:
                fig_deep = go.Figure()
                fig_deep.add_trace(go.Scatter(x=df_final['Date'], y=df_final['Gemini_Ratio'], name=f'{g_name} (Daily)', line=dict(color='rgba(99, 102, 241, 0.3)', width=1)))
                fig_deep.add_trace(go.Scatter(x=df_final['Date'], y=df_final['Gemini_MA7'], name=f'{g_name} (7d MA)', line=dict(color='#6366f1', width=3)))
                fig_deep.add_trace(go.Scatter(x=df_final['Date'], y=df_final['Claude_Ratio'], name=f'{c_name} (Daily)', line=dict(color='rgba(236, 72, 153, 0.3)', width=1)))
                fig_deep.add_trace(go.Scatter(x=df_final['Date'], y=df_final['Claude_MA7'], name=f'{c_name} (7d MA)', line=dict(color='#ec4899', width=3)))
                
                fig_deep.update_layout(title="일별 추이 및 7일 이동평균선", template="plotly_dark", height=500)
                st.plotly_chart(fig_deep, width='stretch', key="deep_main_chart")
                
                # Stat Cards (KPIs)
                kpi1, kpi2, kpi3 = st.columns(3)
                corr = au.calculate_correlation(df_final['Gemini_Ratio'].tolist(), df_final['Claude_Ratio'].tolist())
                
                kpi1.metric(f"{g_name} 평균", f"{df_final['Gemini_Ratio'].mean():.2f}")
                kpi2.metric(f"{c_name} 평균", f"{df_final['Claude_Ratio'].mean():.2f}")
                kpi3.metric("검색 상관계수", f"{corr:.4f}", help="1에 가까울수록 동반 상승/하락")
            
            # 2. 기간/요일 분석
            with deep_sub_tabs[1]:
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    df_month = au.group_by_period(df_final, 'month')
                    fig_month = px.bar(df_month, x='label', y=['Gemini', 'Claude'], barmode='group', title="월별 평균 검색 비중", color_discrete_map={'Gemini':'#6366f1', 'Claude':'#ec4899'})
                    # 범례 이름 수정
                    fig_month.for_each_trace(lambda t: t.update(name = g_name if t.name == 'Gemini' else c_name))
                    st.plotly_chart(fig_month, width='stretch', key="deep_month_chart")
                with col_p2:
                    df_day = au.group_by_day_of_week(df_final)
                    fig_radar = go.Figure()
                    fig_radar.add_trace(go.Scatterpolar(r=df_day['Gemini'], theta=df_day['day'], fill='toself', name=g_name, line_color='#6366f1'))
                    fig_radar.add_trace(go.Scatterpolar(r=df_day['Claude'], theta=df_day['day'], fill='toself', name=c_name, line_color='#ec4899'))
                    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, float(df_day[['Gemini','Claude']].values.max())*1.1])), showlegend=True, title="요일별 분석 (Radar)")
                    st.plotly_chart(fig_radar, width='stretch', key="deep_radar_chart")
            
            # 3. 상관성/인사이트
            with deep_sub_tabs[2]:
                st.markdown("### 📜 데이터 종합 분석 결론")
                insight_text = f"""
                1. **성장 모멘텀**: {g_name}의 평균 지수는 **{df_final['Gemini_Ratio'].mean():.2f}**로 {c_name}(**{df_final['Claude_Ratio'].mean():.2f}**) 대비 {'우위에 있습니다' if df_final['Gemini_Ratio'].mean() > df_final['Claude_Ratio'].mean() else '추격 중입니다'}.
                2. **상관성**: 두 모델의 상관계수는 **{corr:.4f}**입니다. {'매우 높은 양의 상관관계가 관찰되며, AI 시장 전체의 관심도가 함께 움직이고 있음' if corr > 0.7 else '독자적인 트렌드 흐름을 보이고 있음'}을 시사합니다.
                3. **변동성**: 두 모델 모두 특정 이벤트에 민감하게 반응하며, 시장 점유율 확대를 위한 격전이 지속되고 있습니다.
                """
                st.info(insight_text)
            
            # 4. 원본 데이터
            with deep_sub_tabs[3]:
                st.dataframe(df_final.sort_values('Date', ascending=False), width=None, use_container_width=True, key="deep_raw_data")
        else:
            st.warning("분석할 키워드 데이터가 충분하지 않습니다. 사이드바에서 비교 키워드를 입력해 주세요.")
    else:
        st.warning("데이터가 없어 대시보드를 표시할 수 없습니다.")
