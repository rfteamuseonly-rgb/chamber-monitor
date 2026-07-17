import streamlit as st
import pandas as pd
import time

# 設定網頁標題與寬度
st.set_page_config(page_title="Chamber 環境雲端看板", layout="wide")

# ==========================================
# 0. 側邊欄：選擇介面風格
# ==========================================
with st.sidebar:
    st.title("⚙️ 介面設定")
    style_choice = st.radio(
        "選擇您喜歡的顯示風格：",
        ["經典簡約卡片", "科技儀表板 (深色)", "新擬態風格 (柔和)", "極簡進度條 (直觀)"],
        index=2 # 預設展示新擬態風格
    )
    st.markdown("---")

# ==========================================
# 1. 各種 CSS 樣式定義
# ==========================================
# 共通隱藏元素
common_css = "<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>"
st.markdown(common_css, unsafe_allow_html=True)

# --- 風格 A: 原版經典卡片 ---
css_classic = """
<style>
    .sensor-card { border-radius: 8px; padding: 15px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: 1px solid #e0e0e0; background-color: white; color: #333; }
    .status-green { border-left: 8px solid #28a745; background-color: #f5faf6; }
    .status-yellow { border-left: 8px solid #ffc107; background-color: #ffffeb; }
    .status-red { border-left: 8px solid #dc3545; background-color: #f8d7da; }
    .status-offline { border-left: 8px solid #6c757d; background-color: #f2f2f2; }
    .card-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee; padding-bottom: 8px; margin-bottom: 10px;}
    .room-name { font-size: 1.4em; font-weight: bold; }
    .history-btn { background-color: #a9d0fc; color: white; padding: 2px 10px; border-radius: 4px; font-size: 0.8em; text-decoration: none; }
    .data-val { font-weight: bold; margin-left: 5px; font-size: 1.2em;}
</style>
"""

# --- 風格 B: 科技儀表板 ---
css_modern = """
<style>
    .stApp { background-color: #121420; color: white; }
    h1, h2, h3, h4, h5, h6, span { color: #e2e8f0 !important; }
    .tech-card { background: linear-gradient(145deg, #2A2D43, #1e2030); border-radius: 12px; padding: 15px; margin-bottom: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.4); border: 1px solid #3b3f5c; }
    .tech-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #4b5070; padding-bottom: 10px; margin-bottom: 15px; }
    .tech-room { font-size: 1.4em; font-weight: bold; }
    .gauges-container { display: flex; justify-content: space-around; margin-bottom: 15px; }
    .gauge-wrapper { display: flex; flex-direction: column; align-items: center; }
    .gauge-ring { width: 85px; height: 85px; border-radius: 50%; display: flex; justify-content: center; align-items: center; background: #1e2030; border: 5px solid #4b5070; }
    .status-green .gauge-ring { border-color: #00d2ff; box-shadow: 0 0 10px rgba(0,210,255,0.3); }
    .status-yellow .gauge-ring { border-color: #f6ad55; box-shadow: 0 0 10px rgba(246,173,85,0.3); }
    .status-red .gauge-ring { border-color: #fc8181; box-shadow: 0 0 10px rgba(252,129,129,0.3); }
</style>
"""

# --- 風格 C: 新擬態風格 (Neumorphism) ---
css_neumorphism = """
<style>
    .stApp { background-color: #e0e5ec; color: #4a4a4a; }
    h1, h2, h3 { color: #4a4a4a !important; text-shadow: 2px 2px 4px rgba(163,177,198,0.5); }
    .neu-card { 
        background-color: #e0e5ec; border-radius: 20px; padding: 20px; margin-bottom: 20px;
        box-shadow: 9px 9px 16px rgb(163,177,198,0.6), -9px -9px 16px rgba(255,255,255, 0.5);
    }
    .neu-header { display: flex; justify-content: space-between; margin-bottom: 15px; }
    .neu-room { font-size: 1.5em; font-weight: bold; color: #5a6a85; }
    .neu-data { 
        background-color: #e0e5ec; border-radius: 10px; padding: 10px; margin-bottom: 10px; text-align: center;
        box-shadow: inset 5px 5px 10px rgb(163,177,198,0.5), inset -5px -5px 10px rgba(255,255,255, 0.5);
    }
    .neu-val { font-size: 1.4em; font-weight: 900; }
    .neu-green .neu-val { color: #2ecc71; }
    .neu-red .neu-val { color: #e74c3c; }
    .neu-yellow .neu-val { color: #f1c40f; }
</style>
"""

# --- 風格 D: 極簡進度條 ---
css_minimal = """
<style>
    .min-card { background: #fff; border-radius: 12px; padding: 20px; margin-bottom: 15px; border: 1px solid #f0f0f0; }
    .min-header { font-size: 1.2em; font-weight: bold; color: #222; margin-bottom: 15px; display: flex; justify-content: space-between;}
    .bar-bg { background: #f0f0f0; border-radius: 10px; height: 12px; width: 100%; margin: 5px 0 15px 0; overflow: hidden; }
    .bar-fill-temp { height: 100%; border-radius: 10px; background: linear-gradient(90deg, #ff9a9e 0%, #fecfef 99%, #fecfef 100%); }
    .bar-fill-humi { height: 100%; border-radius: 10px; background: linear-gradient(90deg, #a1c4fd 0%, #c2e9fb 100%); }
    .min-label { display: flex; justify-content: space-between; font-size: 0.9em; color: #666; font-weight: bold; }
</style>
"""

# 注入對應的 CSS
if style_choice == "經典簡約卡片": st.markdown(css_classic, unsafe_allow_html=True)
elif style_choice == "科技儀表板 (深色)": st.markdown(css_modern, unsafe_allow_html=True)
elif style_choice == "新擬態風格 (柔和)": st.markdown(css_neumorphism, unsafe_allow_html=True)
elif style_choice == "極簡進度條 (直觀)": st.markdown(css_minimal, unsafe_allow_html=True)

# ==========================================
# 2. 資料獲取與處理
# ==========================================
SHEET_ID = "17msOHAvXZ9iND5fMJVUd7n3C_TFXD-uTFH4rvVLwJ7k".strip()
GID = "0" 
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid={GID}&tq=SELECT%20*%20ORDER%20BY%20A%20DESC%20LIMIT%2050"

@st.cache_data(ttl=300)
def get_latest_data():
    try:
        df = pd.read_csv(CSV_URL)
        df.columns = ['更新時間', 'Chamber', '溫度', '濕度', '狀態']
        df['Chamber'] = df['Chamber'].astype(str)
        latest_df = df.drop_duplicates(subset=['Chamber'], keep='first')
        data_dict = {}
        for _, row in latest_df.iterrows():
            data_dict[row['Chamber']] = {"temp": row['溫度'], "humi": row['濕度'], "time": row['更新時間']}
        return data_dict
    except: return {}

def get_status_color(temp, humi):
    if pd.isna(temp) or pd.isna(humi) or temp == "---" or humi == "---": return "offline"
    try:
        t, h = float(temp), float(humi)
        if t > 26 or h > 75: return "red"
        if (17 <= t <= 24) and (10 <= h <= 65): return "green"
        return "yellow"
    except: return "offline"

# ==========================================
# 3. 介面渲染
# ==========================================
def render_card(chamber_id, data_dict):
    temp = data_dict.get(chamber_id, {}).get('temp', "---")
    humi = data_dict.get(chamber_id, {}).get('humi', "---")
    time_str = data_dict.get(chamber_id, {}).get('time', "無資料")
    
    temp_disp = f"{float(temp):.1f}°C" if temp != "---" else "--"
    humi_disp = f"{float(humi):.1f}%" if humi != "---" else "--"
    status = get_status_color(temp, humi)
    time_disp = str(time_str).split(" ")[-1] if " " in str(time_str) else time_str
    
    # 計算進度條百分比 (假設溫度最高 40，濕度最高 100)
    temp_pct = min((float(temp) / 40.0) * 100, 100) if temp != "---" else 0
    humi_pct = min((float(humi) / 100.0) * 100, 100) if humi != "---" else 0

    if style_choice == "經典簡約卡片":
        return f"""
        <div class="sensor-card status-{status}">
            <div class="card-header"><span class="room-name">{chamber_id}</span></div>
            <div>Temp: <span class="data-val">{temp_disp}</span></div>
            <div>Humidity: <span class="data-val">{humi_disp}</span></div>
        </div>"""
        
    elif style_choice == "科技儀表板 (深色)":
        return f"""
        <div class="tech-card status-{status}">
            <div class="tech-header"><span class="tech-room">{chamber_id}</span></div>
            <div class="gauges-container">
                <div class="gauge-wrapper"><div class="gauge-ring"><span class="gauge-val">{temp_disp}</span></div></div>
                <div class="gauge-wrapper"><div class="gauge-ring"><span class="gauge-val">{humi_disp}</span></div></div>
            </div>
        </div>"""
        
    elif style_choice == "新擬態風格 (柔和)":
        return f"""
        <div class="neu-card neu-{status}">
            <div class="neu-header"><span class="neu-room">{chamber_id}</span></div>
            <div class="neu-data">🌡️ 溫度 <br><span class="neu-val">{temp_disp}</span></div>
            <div class="neu-data">💧 濕度 <br><span class="neu-val">{humi_disp}</span></div>
        </div>"""
        
    elif style_choice == "極簡進度條 (直觀)":
        return f"""
        <div class="min-card">
            <div class="min-header"><span>{chamber_id}</span> <span>{status.upper()}</span></div>
            <div class="min-label"><span>溫度</span> <span>{temp_disp}</span></div>
            <div class="bar-bg"><div class="bar-fill-temp" style="width: {temp_pct}%;"></div></div>
            <div class="min-label"><span>濕度</span> <span>{humi_disp}</span></div>
            <div class="bar-bg"><div class="bar-fill-humi" style="width: {humi_pct}%;"></div></div>
        </div>"""

# ==========================================
# 4. 主畫面佈局
# ==========================================
st.title("🏭 Chamber 環境雲端看板")
st.markdown("---")

Chambers = {
    "5F": ["502", "503", "504", "505", "509", "510", "511"],
    "6F": ["602", "603", "604", "605", "607", "608"],
    "7F": ["703", "706", "707", "708"],
    "8F": ["803", "804", "808", "809", "810"]
}

placeholder = st.empty()

while True:
    data_dict = get_latest_data()
    with placeholder.container():
        for floor, rooms in Chambers.items():
            st.subheader(f"📍 {floor} Chamber")
            cols = st.columns(4)
            for i, chamber in enumerate(rooms):
                with cols[i % 4]:
                    st.markdown(render_card(chamber, data_dict), unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
    time.sleep(300)
    st.rerun()
