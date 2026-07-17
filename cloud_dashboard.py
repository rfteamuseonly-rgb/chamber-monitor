import streamlit as st
import pandas as pd
import time

# 設定網頁標題與寬度 (使用 wide 模式並透過 CSS 進一步擴展)
st.set_page_config(page_title="Chamber 環境雲端看板", layout="wide")

# ==========================================
# 0. 側邊欄：選擇介面風格
# ==========================================
with st.sidebar:
    st.title("⚙️ 介面設定")
    style_choice = st.radio(
        "選擇顯示風格：",
        ["經典簡約卡片 (高密度)", "科技儀表板 (高密度)", "新擬態風格 (高密度)", "極簡進度條 (高密度)"],
        index=1 # 預設科技風格
    )
    st.markdown("---")
    st.info("💡 目前為高密度佈局模式，一行顯示 7 個機台，讓 5F 與 6F 能在同一頁面完整呈現。")

# ==========================================
# 1. 高密度 CSS 樣式定義
# ==========================================
# 共通 CSS：極大化可用空間，隱藏預設頂部留白與選單
common_css = """
<style>
    #MainMenu {visibility: hidden;} 
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { 
        padding-top: 1rem !important; 
        padding-bottom: 0rem !important; 
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }
    h4 { margin-top: 0px !important; margin-bottom: 5px !important; padding-top: 0px !important;}
</style>
"""
st.markdown(common_css, unsafe_allow_html=True)

# --- 風格 A: 經典簡約卡片 (高密度) ---
css_classic = """
<style>
    .sensor-card { border-radius: 6px; padding: 8px; margin-bottom: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border: 1px solid #e0e0e0; background-color: white; color: #333; line-height: 1.2;}
    .status-green { border-left: 5px solid #28a745; background-color: #f5faf6; }
    .status-yellow { border-left: 5px solid #ffc107; background-color: #ffffeb; }
    .status-red { border-left: 5px solid #dc3545; background-color: #f8d7da; }
    .status-offline { border-left: 5px solid #6c757d; background-color: #f2f2f2; }
    .card-header { border-bottom: 1px solid #eee; padding-bottom: 4px; margin-bottom: 6px;}
    .room-name { font-size: 1.1em; font-weight: bold; }
    .data-val { font-weight: bold; margin-left: 3px; font-size: 1.1em;}
    .data-row { font-size: 0.9em; margin: 3px 0; }
</style>
"""

# --- 風格 B: 科技儀表板 (高密度) ---
css_modern = """
<style>
    .stApp { background-color: #0b0e14; color: white; }
    h1, h2, h3, h4, h5, h6, span { color: #e2e8f0 !important; }
    .tech-card { background: linear-gradient(145deg, #1f2233, #151722); border-radius: 8px; padding: 8px; margin-bottom: 5px; border: 1px solid #2a2e45; }
    .tech-header { border-bottom: 1px solid #3b3f5c; padding-bottom: 5px; margin-bottom: 10px; text-align: center;}
    .tech-room { font-size: 1.1em; font-weight: bold; }
    .gauges-container { display: flex; justify-content: space-around; }
    .gauge-wrapper { display: flex; flex-direction: column; align-items: center; }
    .gauge-ring { width: 50px; height: 50px; border-radius: 50%; display: flex; justify-content: center; align-items: center; background: #151722; border: 3px solid #3b3f5c; }
    .gauge-val { font-size: 0.9em; font-weight: bold; }
    .gauge-title { margin-top: 4px; font-size: 0.7em; color: #8fa1cd; }
    .status-green .gauge-ring { border-color: #00d2ff; box-shadow: 0 0 8px rgba(0,210,255,0.4); }
    .status-yellow .gauge-ring { border-color: #f6ad55; box-shadow: 0 0 8px rgba(246,173,85,0.4); }
    .status-red .gauge-ring { border-color: #fc8181; box-shadow: 0 0 8px rgba(252,129,129,0.5); }
</style>
"""

# --- 風格 C: 新擬態風格 (高密度) ---
css_neumorphism = """
<style>
    .stApp { background-color: #e0e5ec; color: #4a4a4a; }
    h1, h2, h3, h4 { color: #4a4a4a !important; }
    .neu-card { background-color: #e0e5ec; border-radius: 12px; padding: 10px; margin-bottom: 10px; box-shadow: 5px 5px 10px rgb(163,177,198,0.5), -5px -5px 10px rgba(255,255,255, 0.6); }
    .neu-header { margin-bottom: 8px; text-align: center;}
    .neu-room { font-size: 1.1em; font-weight: bold; color: #5a6a85; }
    .neu-data { background-color: #e0e5ec; border-radius: 8px; padding: 6px; margin-bottom: 6px; text-align: center; box-shadow: inset 3px 3px 6px rgb(163,177,198,0.5), inset -3px -3px 6px rgba(255,255,255, 0.6); font-size: 0.8em;}
    .neu-val { font-size: 1.2em; font-weight: 900; display: block; margin-top: 2px;}
    .neu-green .neu-val { color: #2ecc71; }
    .neu-red .neu-val { color: #e74c3c; }
    .neu-yellow .neu-val { color: #f1c40f; }
</style>
"""

# --- 風格 D: 極簡進度條 (高密度) ---
css_minimal = """
<style>
    .min-card { background: #fff; border-radius: 8px; padding: 10px; margin-bottom: 5px; border: 1px solid #eaeaea; box-shadow: 0 1px 3px rgba(0,0,0,0.05);}
    .min-header { font-size: 1em; font-weight: bold; color: #222; margin-bottom: 8px; display: flex; justify-content: space-between;}
    .bar-bg { background: #f0f0f0; border-radius: 5px; height: 6px; width: 100%; margin: 3px 0 8px 0; overflow: hidden; }
    .bar-fill-temp { height: 100%; border-radius: 5px; background: linear-gradient(90deg, #ff9a9e 0%, #fecfef 100%); }
    .bar-fill-humi { height: 100%; border-radius: 5px; background: linear-gradient(90deg, #a1c4fd 0%, #c2e9fb 100%); }
    .min-label { display: flex; justify-content: space-between; font-size: 0.8em; color: #666; font-weight: bold; }
</style>
"""

# 注入對應的 CSS
if "經典" in style_choice: st.markdown(css_classic, unsafe_allow_html=True)
elif "科技" in style_choice: st.markdown(css_modern, unsafe_allow_html=True)
elif "新擬態" in style_choice: st.markdown(css_neumorphism, unsafe_allow_html=True)
elif "極簡" in style_choice: st.markdown(css_minimal, unsafe_allow_html=True)

# ==========================================
# 2. 資料獲取邏輯
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
# 3. 卡片渲染邏輯
# ==========================================
def render_card(chamber_id, data_dict):
    temp = data_dict.get(chamber_id, {}).get('temp', "---")
    humi = data_dict.get(chamber_id, {}).get('humi', "---")
    
    temp_disp = f"{float(temp):.1f}°C" if temp != "---" else "--"
    humi_disp = f"{float(humi):.1f}%" if humi != "---" else "--"
    status = get_status_color(temp, humi)
    
    temp_pct = min((float(temp) / 40.0) * 100, 100) if temp != "---" else 0
    humi_pct = min((float(humi) / 100.0) * 100, 100) if humi != "---" else 0

    if "經典" in style_choice:
        return f"""
        <div class="sensor-card status-{status}">
            <div class="card-header"><span class="room-name">{chamber_id}</span></div>
            <div class="data-row">T: <span class="data-val">{temp_disp}</span></div>
            <div class="data-row">H: <span class="data-val">{humi_disp}</span></div>
        </div>"""
        
    elif "科技" in style_choice:
        return f"""
        <div class="tech-card status-{status}">
            <div class="tech-header"><span class="tech-room">{chamber_id}</span></div>
            <div class="gauges-container">
                <div class="gauge-wrapper"><div class="gauge-ring"><span class="gauge-val">{temp_disp}</span></div><div class="gauge-title">Temp</div></div>
                <div class="gauge-wrapper"><div class="gauge-ring"><span class="gauge-val">{humi_disp}</span></div><div class="gauge-title">Humi</div></div>
            </div>
        </div>"""
        
    elif "新擬態" in style_choice:
        return f"""
        <div class="neu-card neu-{status}">
            <div class="neu-header"><span class="neu-room">{chamber_id}</span></div>
            <div class="neu-data">Temp <span class="neu-val">{temp_disp}</span></div>
            <div class="neu-data">Humi <span class="neu-val">{humi_disp}</span></div>
        </div>"""
        
    elif "極簡" in style_choice:
        icon = "🟢" if status == "green" else "🔴" if status == "red" else "🟡" if status == "yellow" else "⚪"
        return f"""
        <div class="min-card">
            <div class="min-header"><span>{chamber_id}</span> <span>{icon}</span></div>
            <div class="min-label"><span>T</span> <span>{temp_disp}</span></div>
            <div class="bar-bg"><div class="bar-fill-temp" style="width: {temp_pct}%;"></div></div>
            <div class="min-label"><span>H</span> <span>{humi_disp}</span></div>
            <div class="bar-bg"><div class="bar-fill-humi" style="width: {humi_pct}%;"></div></div>
        </div>"""

# ==========================================
# 4. 主畫面佈局 (強制 7 欄位)
# ==========================================
# 隱藏標題的底線，節省空間
st.markdown("<h3 style='margin-bottom:10px;'>🏭 溫濕度雲端即時監控</h3>", unsafe_allow_html=True)

Chambers = {
    "5F": ["502", "503", "504", "505", "509", "510", "511"], # 剛好 7 個
    "6F": ["602", "603", "604", "605", "607", "608"],        # 6 個
    "7F": ["703", "706", "707", "708"],                      # 4 個
    "8F": ["803", "804", "808", "809", "810"]                # 5 個
}

placeholder = st.empty()

while True:
    data_dict = get_latest_data()
    with placeholder.container():
        for floor, rooms in Chambers.items():
            st.markdown(f"#### 📍 {floor} Chamber")
            
            # 關鍵修改：強制每一層樓都切分成 7 個欄位
            cols = st.columns(7) 
            
            for i, chamber in enumerate(rooms):
                with cols[i]: # 依序填入前幾個欄位，剩下的會自然留白
                    st.markdown(render_card(chamber, data_dict), unsafe_allow_html=True)
            
            # 使用極小的間距取代原本的 st.markdown("<br>")
            st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)
            
    time.sleep(300)
    st.rerun()
