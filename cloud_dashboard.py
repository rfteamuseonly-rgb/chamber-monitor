import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# 設定網頁標題與寬度 (初始隱藏側邊欄)
st.set_page_config(page_title="Chamber 環境雲端看板", layout="wide", initial_sidebar_state="collapsed")

# ==========================================
# 0. 網頁自動重整機制
# ==========================================
st_autorefresh(interval=300000, limit=None, key="data_refresh")

st.markdown("<h2 style='margin-bottom:10px;'>🏭 Chamber 溫濕度雲端即時監控</h2>", unsafe_allow_html=True)

# ==========================================
# 1. 樓層定義與狀態選單
# ==========================================
Chambers = {
    "5F": ["502", "503", "504", "505", "509", "510", "511"],
    "6F": ["602", "603", "604", "605", "607", "608"],
    "7F": ["703", "706", "707", "708"],
    "8F": ["803", "804", "808", "809", "810"]
}
all_floors = list(Chambers.keys())

STYLE_OPTIONS = [
    "經典簡約卡片", "科技儀表板 (深色)", "新擬態風格 (柔和)", "極簡進度條 (直觀)",
    "賽博龐克 (霓虹科幻)", "玻璃擬物 (液體波紋)", "極簡光環 (脈動警報)"
]

with st.expander("⚙️ 點擊展開 / 隱藏介面設定 (風格切換)", expanded=False):
    style_choice = st.radio(
        "請選擇您喜歡的顯示風格：",
        STYLE_OPTIONS,
        index=0, 
        key="ui_style", 
        horizontal=True
    )
    
    selected_floors = st.multiselect(
        "🏢 請選擇要監控的樓層 (支援單選與多選)：",
        options=all_floors,
        default=all_floors,
        key="floor_filter"
    )

st.markdown("<hr style='margin-top: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)

# ==========================================
# 2. 完整展開的 CSS 樣式定義
# ==========================================
st.markdown("""
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;} 
    .block-container { padding-top: 1.5rem !important; padding-bottom: 1rem !important; }
    h3 { margin-top: 5px !important; margin-bottom: 10px !important; }
</style>
""", unsafe_allow_html=True)

# 1. 經典簡約卡片
css_classic = """
<style>
    .sensor-card { border-radius: 8px; padding: 12px; margin-bottom: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: 1px solid #e0e0e0; background-color: white; color: #333; }
    .status-green { border-left: 6px solid #28a745; background-color: #f5faf6; }
    .status-yellow { border-left: 6px solid #ffc107; background-color: #ffffeb; }
    .status-red { border-left: 6px solid #dc3545; background-color: #f8d7da; }
    .status-offline { border-left: 6px solid #6c757d; background-color: #f2f2f2; }
    .card-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee; padding-bottom: 6px; margin-bottom: 8px;}
    .room-name { font-size: 1.25em; font-weight: bold; }
    .data-val { font-weight: bold; margin-left: 5px; font-size: 1.15em;}
    .data-row { margin: 3px 0; }
    .timestamp { font-size: 0.75em; color: #888; text-align: right; margin-top: 6px; }
</style>
"""

# 2. 科技儀表板 (深色)
css_modern = """
<style>
    .stApp { background-color: #121420; color: white; }
    h1, h2, h3, h4, h5, h6, span { color: #e2e8f0 !important; }
    .tech-card { background: linear-gradient(145deg, #2A2D43, #1e2030); border-radius: 10px; padding: 12px; margin-bottom: 12px; box-shadow: 0 6px 12px rgba(0,0,0,0.3); border: 1px solid #3b3f5c; }
    .tech-header { display: flex; justify-content: space-between; border-bottom: 1px solid #4b5070; padding-bottom: 6px; margin-bottom: 10px; }
    .tech-room { font-size: 1.25em; font-weight: bold; }
    .gauges-container { display: flex; justify-content: space-around; margin-bottom: 5px;}
    .gauge-wrapper { display: flex; flex-direction: column; align-items: center; }
    .gauge-ring { width: 70px; height: 70px; border-radius: 50%; display: flex; justify-content: center; align-items: center; background: #1e2030; border: 4px solid #4b5070; }
    .gauge-val { font-size: 1.1em; font-weight: bold; }
    .gauge-title { margin-top: 6px; font-size: 0.8em; color: #8fa1cd; }
    .status-green .gauge-ring { border-color: #00d2ff; box-shadow: 0 0 10px rgba(0,210,255,0.3); }
    .status-yellow .gauge-ring { border-color: #f6ad55; box-shadow: 0 0 10px rgba(246,173,85,0.4); }
    .status-red .gauge-ring { border-color: #fc8181; box-shadow: 0 0 10px rgba(252,129,129,0.5); }
    .tech-timestamp { font-size: 0.75em; color: #6b7280; text-align: center; margin-top: 8px; }
</style>
"""

# 3. 新擬態風格
css_neumorphism = """
<style>
    .stApp { background-color: #e0e5ec; color: #4a4a4a; }
    h1, h2, h3 { color: #4a4a4a !important; text-shadow: 1px 1px 2px rgba(163,177,198,0.5); }
    .neu-card { background-color: #e0e5ec; border-radius: 15px; padding: 15px; margin-bottom: 15px; box-shadow: 6px 6px 12px rgb(163,177,198,0.5), -6px -6px 12px rgba(255,255,255, 0.5); }
    .neu-header { display: flex; justify-content: space-between; margin-bottom: 10px; }
    .neu-room { font-size: 1.3em; font-weight: bold; color: #5a6a85; }
    .neu-data { background-color: #e0e5ec; border-radius: 8px; padding: 8px; margin-bottom: 8px; text-align: center; box-shadow: inset 4px 4px 8px rgb(163,177,198,0.5), inset -4px -4px 8px rgba(255,255,255, 0.5); font-size: 0.9em;}
    .neu-val { font-size: 1.3em; font-weight: 900; }
    .neu-green .neu-val { color: #2ecc71; }
    .neu-yellow .neu-val { color: #f39c12; }
    .neu-red .neu-val { color: #e74c3c; }
    .neu-timestamp { font-size: 0.75em; color: #8fa1cd; text-align: right; margin-top: 8px; }
</style>
"""

# 4. 極簡進度條
css_minimal = """
<style>
    .min-card { background: #fff; border-radius: 10px; padding: 15px; margin-bottom: 12px; border: 1px solid #f0f0f0; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    .min-header { font-size: 1.1em; font-weight: bold; color: #222; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;}
    .bar-bg { background: #f0f0f0; border-radius: 8px; height: 8px; width: 100%; margin: 4px 0 12px 0; overflow: hidden; }
    .bar-fill { height: 100%; border-radius: 8px; transition: width 0.5s ease-in-out; }
    
    .min-status-green { border-left: 6px solid #28a745; }
    .min-status-green .bar-fill { background: linear-gradient(90deg, #84fab0 0%, #8fd3f4 100%); }
    
    .min-status-yellow { border-left: 6px solid #ffc107; background-color: #fffffc; }
    .min-status-yellow .bar-fill { background: linear-gradient(90deg, #f6d365 0%, #fda085 100%); }
    
    .min-status-red { border-left: 6px solid #dc3545; background-color: #fffafa; }
    .min-status-red .bar-fill { background: linear-gradient(90deg, #ff9a9e 0%, #fecfef 100%); }
    
    .min-label { display: flex; justify-content: space-between; font-size: 0.85em; color: #666; font-weight: bold; margin-bottom: 4px; }
    .min-timestamp { font-size: 0.75em; color: #aaa; text-align: right; margin-top: 8px; }
</style>
"""

# 5. 賽博龐克 (大幅修改排版與字體大小)
css_cyberpunk = """
<style>
    .stApp { background-color: #010103; color: #0ff; font-family: 'Courier New', Courier, monospace; }
    h1, h2, h3 { color: #0ff !important; text-shadow: 0 0 5px #0ff; }
    .cyber-card { background: #010103; border: 2px solid #0ff; border-radius: 8px; padding: 15px; margin-bottom: 15px; position: relative; }
    .cyber-header { font-size: 1.4em; font-weight: bold; display: flex; justify-content: space-between; margin-bottom: 10px; padding-bottom: 5px; border-bottom: 1px dashed; }
    
    /* 新增左右並排容器 */
    .cyber-data-container { display: flex; justify-content: space-around; align-items: center; margin: 15px 0; }
    .cyber-data { font-size: 1.1em; text-align: center; } 
    
    /* 將數值變大並設定為 block 讓它換行顯示在標籤下方 */
    .cyber-val { font-size: 2.4em; font-weight: bold; display: block; margin-top: 5px; }
    
    .cyber-warn-badge { display: none; color: #fff; padding: 2px 6px; font-size: 0.6em; border-radius: 3px; animation: blink 0.5s infinite;}
    
    .cyber-green { border-color: #0ff; box-shadow: 0 0 10px rgba(0,255,255,0.3); }
    .cyber-green .cyber-header { color: #0ff; border-bottom-color: #0ff; text-shadow: 0 0 5px #0ff; }
    .cyber-green .cyber-data { color: #0ff; text-shadow: 0 0 5px #0ff; }
    .cyber-green .cyber-val { color: #0f0; text-shadow: 0 0 8px #0f0; }
    
    .cyber-yellow { border-color: #ff0; box-shadow: 0 0 10px rgba(255,255,0,0.4); }
    .cyber-yellow .cyber-header { color: #ff0; border-bottom-color: #ff0; text-shadow: 0 0 5px #ff0; }
    .cyber-yellow .cyber-data { color: #e6a817; text-shadow: 0 0 5px #e6a817; }
    .cyber-yellow .cyber-val { color: #ff0; text-shadow: 0 0 8px #ff0; }
    .cyber-yellow .cyber-warn-badge { display: inline-block; background: #e6a817; }
    
    .cyber-red { border-color: #f00; box-shadow: 0 0 15px rgba(255,0,0,0.6); animation: glitch-border 0.5s infinite; }
    .cyber-red .cyber-header { color: #f00; border-bottom-color: #f00; text-shadow: 2px 0 #0ff, -2px 0 #f00; animation: glitch-text 0.3s infinite; }
    .cyber-red .cyber-data { color: #f00; text-shadow: 0 0 5px #f00; }
    .cyber-red .cyber-val { color: #f00; text-shadow: 0 0 8px #f00; }
    .cyber-red .cyber-warn-badge { display: inline-block; background: #f00; }

    @keyframes glitch-border { 0%, 100% { opacity: 1; transform: translateX(0); } 50% { opacity: 0.8; transform: translateX(1px); } }
    @keyframes glitch-text { 0%, 100% { transform: skew(0deg); } 50% { transform: skew(-5deg); } }
    @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
</style>
"""

# 6. 玻璃擬物
css_glassmorphism = """
<style>
    .stApp { background-color: #e6e6e6; color: #333; }
    h1, h2, h3 { color: #333 !important; }
    .glass-card { background: rgba(255, 255, 255, 0.4); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border-radius: 16px; padding: 15px; margin-bottom: 15px; position: relative; overflow: hidden;}
    .glass-header { font-size: 1.2em; font-weight: bold; margin-bottom: 12px; z-index: 2; position: relative;}
    .glass-data-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; z-index: 2; position: relative;}
    .glass-data-block { border-radius: 8px; padding: 8px 12px; text-align: center; }
    .glass-label { font-size: 0.8em; color: #555; margin-bottom: 4px; }
    .glass-val { font-size: 1.5em; font-weight: 800; }
    .glass-liquid { position: absolute; bottom: -50%; left: -50%; width: 200%; height: 200%; border-radius: 40%; z-index: 0; }
    .glass-timestamp { font-size: 0.7em; color: #666; text-align: right; margin-top: 8px; z-index: 2; position: relative; }
    
    .glass-green { border: 1px solid rgba(255, 255, 255, 0.6); box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1); }
    .glass-green .glass-data-block { background: rgba(52, 152, 219, 0.15); }
    .glass-green .glass-val { color: #2c3e50; }
    .glass-green .glass-liquid { background: rgba(52, 152, 219, 0.1); animation: liquid-spin 6s linear infinite; }
    
    .glass-yellow { background: rgba(255, 230, 150, 0.3); border: 1px solid rgba(255, 200, 50, 0.5); box-shadow: 0 8px 32px 0 rgba(243, 156, 18, 0.15); }
    .glass-yellow .glass-data-block { background: rgba(243, 156, 18, 0.2); }
    .glass-yellow .glass-val { color: #d35400; }
    .glass-yellow .glass-liquid { background: rgba(243, 156, 18, 0.2); animation: liquid-spin 4.5s linear infinite; }
    
    .glass-red { background: rgba(255, 200, 200, 0.4); border: 1px solid rgba(255, 100, 100, 0.6); box-shadow: 0 8px 32px 0 rgba(255, 50, 50, 0.25); }
    .glass-red .glass-data-block { background: rgba(231, 76, 60, 0.2); }
    .glass-red .glass-val { color: #c0392b; }
    .glass-red .glass-liquid { background: rgba(231, 76, 60, 0.25); animation: liquid-spin 3s linear infinite; }
    
    @keyframes liquid-spin { 0% { transform: translateY(50%) rotate(0deg); } 100% { transform: translateY(50%) rotate(360deg); } }
</style>
"""

# 7. 極簡光環
css_ringpulse = """
<style>
    .stApp { background-color: #f7f9fa; color: #1f2937; }
    h1, h2, h3 { color: #1f2937 !important; }
    .ring-card { border-radius: 12px; padding: 16px; margin-bottom: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.03); display: flex; flex-direction: column; align-items: center; transition: transform 0.2s;}
    .ring-header { font-size: 1.1em; font-weight: bold; width: 100%; text-align: left; margin-bottom: 10px; color: #4a5568;}
    .ring-container { display: flex; gap: 15px; justify-content: center; width: 100%;}
    .ring-gauge { width: 70px; height: 70px; border-radius: 50%; display: flex; align-items: center; justify-content: center; position: relative; }
    .ring-inner { width: 56px; height: 56px; background: #ffffff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 0.9em; box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);}
    .ring-data-val { font-size: 1.1em; font-weight: bold; margin-top: 5px; }
    .ring-timestamp { font-size: 0.75em; color: #a0aec0; text-align: right; width: 100%; margin-top: 12px; }
    
    .ring-green { background: #ffffff; border: 1px solid #edf2f7; }
    .ring-yellow { background: #fffff0; border: 2px solid #ecc94b; }
    .ring-yellow .ring-inner { color: #b7791f; }
    .ring-red { background: #fff5f5; border: 2px solid #fc8181; animation: heartbeat 1.2s infinite; }
    .ring-red .ring-inner { color: #e53e3e; }
    
    @keyframes heartbeat { 0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(229, 62, 62, 0.4); } 50% { transform: scale(1.03); box-shadow: 0 0 0 10px rgba(229, 62, 62, 0); } 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(229, 62, 62, 0); } }
</style>
"""

# 套用樣式
if style_choice == "經典簡約卡片": st.markdown(css_classic, unsafe_allow_html=True)
elif style_choice == "科技儀表板 (深色)": st.markdown(css_modern, unsafe_allow_html=True)
elif style_choice == "新擬態風格 (柔和)": st.markdown(css_neumorphism, unsafe_allow_html=True)
elif style_choice == "極簡進度條 (直觀)": st.markdown(css_minimal, unsafe_allow_html=True)
elif style_choice == "賽博龐克 (霓虹科幻)": st.markdown(css_cyberpunk, unsafe_allow_html=True)
elif style_choice == "玻璃擬物 (液體波紋)": st.markdown(css_glassmorphism, unsafe_allow_html=True)
elif style_choice == "極簡光環 (脈動警報)": st.markdown(css_ringpulse, unsafe_allow_html=True)

# ==========================================
# 3. 資料獲取與處理邏輯
# ==========================================
SHEET_ID = "17msOHAvXZ9iND5fMJVUd7n3C_TFXD-uTFH4rvVLwJ7k".strip()
GID = "0" 
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid={GID}&tq=SELECT%20*%20ORDER%20BY%20A%20DESC%20LIMIT%2050"

@st.cache_data(ttl=60)
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
# 4. 介面渲染函數
# ==========================================
def render_card(chamber_id, data_dict):
    temp = data_dict.get(chamber_id, {}).get('temp', "---")
    humi = data_dict.get(chamber_id, {}).get('humi', "---")
    time_raw = data_dict.get(chamber_id, {}).get('time', "無資料")
    
    temp_disp = f"{float(temp):.1f}°C" if temp != "---" else "--"
    humi_disp = f"{float(humi):.1f}%" if humi != "---" else "--"
    status = get_status_color(temp, humi) 
    time_disp = str(time_raw).split(" ")[-1] if " " in str(time_raw) else time_raw
    
    temp_pct = min((float(temp) / 40.0) * 100, 100) if temp != "---" else 0
    humi_pct = min((float(humi) / 100.0) * 100, 100) if humi != "---" else 0

    if style_choice == "經典簡約卡片":
        return f'<div class="sensor-card status-{status}"><div class="card-header"><span class="room-name">{chamber_id}</span></div><div class="data-row">Temp: <span class="data-val">{temp_disp}</span></div><div class="data-row">Humidity: <span class="data-val">{humi_disp}</span></div><div class="timestamp">Updated: {time_disp}</div></div>'
    
    elif style_choice == "科技儀表板 (深色)":
        return f'<div class="tech-card status-{status}"><div class="tech-header"><span class="tech-room">{chamber_id}</span></div><div class="gauges-container"><div class="gauge-wrapper"><div class="gauge-ring"><span class="gauge-val">{temp_disp}</span></div></div><div class="gauge-wrapper"><div class="gauge-ring"><span class="gauge-val">{humi_disp}</span></div></div></div><div class="tech-timestamp">Updated: {time_disp}</div></div>'
    
    elif style_choice == "新擬態風格 (柔和)":
        return f'<div class="neu-card neu-{status}"><div class="neu-header"><span class="neu-room">{chamber_id}</span></div><div class="neu-data">溫度 <br><span class="neu-val">{temp_disp}</span></div><div class="neu-data">濕度 <br><span class="neu-val">{humi_disp}</span></div><div class="neu-timestamp">Updated: {time_disp}</div></div>'
    
    elif style_choice == "極簡進度條 (直觀)":
        icon = "🟢" if status == "green" else "🟡" if status == "yellow" else "🔴"
        return f'<div class="min-card min-status-{status}"><div class="min-header"><span>{chamber_id}</span><span>{icon}</span></div><div class="min-label"><span>溫度</span> <span>{temp_disp}</span></div><div class="bar-bg"><div class="bar-fill" style="width: {temp_pct}%;"></div></div><div class="min-label"><span>濕度</span> <span>{humi_disp}</span></div><div class="bar-bg"><div class="bar-fill" style="width: {humi_pct}%;"></div></div><div class="min-timestamp">Updated: {time_disp}</div></div>'
    
    elif style_choice == "賽博龐克 (霓虹科幻)":
        warn_txt = "SYS.OK" if status == "green" else ("SYS.WARN" if status == "yellow" else "SYS.ERR")
        # 修改點：加入了 cyber-data-container，將資料並排並加大文字
        return f'<div class="cyber-card cyber-{status}"><div class="cyber-header"><span>{chamber_id}</span><span class="cyber-warn-badge">{warn_txt}</span></div><div class="cyber-data-container"><div class="cyber-data">TMP<span class="cyber-val">{temp_disp}</span></div><div class="cyber-data">HUM<span class="cyber-val">{humi_disp}</span></div></div><div style="font-size:0.7em; color:#888; text-align:right; margin-top:8px;">LAST_SYNC: {time_disp}</div></div>'
    
    elif style_choice == "玻璃擬物 (液體波紋)":
        return f'<div class="glass-card glass-{status}"><div class="glass-liquid" style="top: {100 - (humi_pct * 0.8)}%;"></div><div class="glass-header">{chamber_id}</div><div class="glass-data-row"><div class="glass-data-block"><div class="glass-label">溫度</div><div class="glass-val">{temp_disp}</div></div><div class="glass-data-block"><div class="glass-label">濕度</div><div class="glass-val">{humi_disp}</div></div></div><div class="glass-timestamp">Updated: {time_disp}</div></div>'
    
    elif style_choice == "極簡光環 (脈動警報)":
        color_t = "#fc8181" if status == "red" else ("#ecc94b" if status == "yellow" else "#4299e1")
        color_h = "#fc8181" if status == "red" else ("#ecc94b" if status == "yellow" else "#48bb78")
        return f'<div class="ring-card ring-{status}"><div class="ring-header">{chamber_id}</div><div class="ring-container"><div style="text-align:center;"><div class="ring-gauge" style="background: conic-gradient({color_t} {temp_pct}%, #edf2f7 0);"><div class="ring-inner">Temp</div></div><div class="ring-data-val">{temp_disp}</div></div><div style="text-align:center;"><div class="ring-gauge" style="background: conic-gradient({color_h} {humi_pct}%, #edf2f7 0);"><div class="ring-inner">Humi</div></div><div class="ring-data-val">{humi_disp}</div></div></div><div class="ring-timestamp">Updated: {time_disp}</div></div>'

# ==========================================
# 5. 主畫面佈局渲染
# ==========================================
data_dict = get_latest_data()

if not selected_floors:
    st.info("💡 請從上方選單中至少選擇一個樓層來顯示資料。")
else:
    for floor in all_floors:
        if floor in selected_floors:
            rooms = Chambers[floor]
            st.markdown(f"### 📍 {floor} Chamber")
            cols = st.columns(4) 
            for i, chamber in enumerate(rooms):
                with cols[i % 4]:
                    st.markdown(render_card(chamber, data_dict), unsafe_allow_html=True)
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
