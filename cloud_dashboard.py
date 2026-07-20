import streamlit as st
import pandas as pd

# 設定網頁標題與寬度 (初始隱藏側邊欄)
st.set_page_config(page_title="Chamber 環境雲端看板", layout="wide", initial_sidebar_state="collapsed")

# ==========================================
# 0. 網頁自動重整與主標題
# ==========================================
# 啟用瀏覽器自動重整 (每 5 分鐘)
st.markdown('<meta http-equiv="refresh" content="300">', unsafe_allow_html=True)
st.markdown("<h2 style='margin-bottom:10px;'>🏭 Chamber 溫濕度雲端即時監控</h2>", unsafe_allow_html=True)

# ==========================================
# 1. 設定選單：折疊面板 (Expander)
# ==========================================
with st.expander("⚙️ 點擊展開 / 隱藏介面設定 (風格切換)", expanded=False):
    style_choice = st.radio(
        "請選擇您喜歡的顯示風格：",
        [
            "經典簡約卡片", "科技儀表板 (深色)", "新擬態風格 (柔和)", "極簡進度條 (直觀)",
            "賽博龐克 (霓虹科幻)", "玻璃擬物 (液體波紋)", "極簡光環 (脈動警報)"
        ],
        index=4, # 預設切換到賽博龐克風格供您預覽
        horizontal=True
    )

# ==========================================
# 2. CSS 樣式定義 (原有 + 新增)
# ==========================================
common_css = """
<style>
    #MainMenu {visibility: hidden;} 
    footer {visibility: hidden;}
    header {visibility: hidden;} 
    .block-container { padding-top: 1.5rem !important; padding-bottom: 1rem !important; }
    h3 { margin-top: 5px !important; margin-bottom: 10px !important; }
</style>
"""
st.markdown(common_css, unsafe_allow_html=True)

# 原有風格 CSS
css_classic = "<style>.sensor-card { border-radius: 8px; padding: 12px; margin-bottom: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: 1px solid #e0e0e0; background-color: white; color: #333; } .status-green { border-left: 6px solid #28a745; background-color: #f5faf6; } .status-yellow { border-left: 6px solid #ffc107; background-color: #ffffeb; } .status-red { border-left: 6px solid #dc3545; background-color: #f8d7da; } .status-offline { border-left: 6px solid #6c757d; background-color: #f2f2f2; } .card-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee; padding-bottom: 6px; margin-bottom: 8px;} .room-name { font-size: 1.25em; font-weight: bold; } .history-btn { background-color: #a9d0fc; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; text-decoration: none; } .data-val { font-weight: bold; margin-left: 5px; font-size: 1.15em;} .data-row { margin: 3px 0; } .timestamp { font-size: 0.75em; color: #888; text-align: right; margin-top: 6px; }</style>"
css_modern = "<style>.stApp { background-color: #121420; color: white; } h1, h2, h3, h4, h5, h6, span { color: #e2e8f0 !important; } .tech-card { background: linear-gradient(145deg, #2A2D43, #1e2030); border-radius: 10px; padding: 12px; margin-bottom: 12px; box-shadow: 0 6px 12px rgba(0,0,0,0.3); border: 1px solid #3b3f5c; } .tech-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #4b5070; padding-bottom: 6px; margin-bottom: 10px; } .tech-room { font-size: 1.25em; font-weight: bold; } .history-btn-tech { background-color: transparent; border: 1px solid #5c638c; color: #8fa1cd !important; padding: 2px 8px; border-radius: 12px; font-size: 0.75em; text-decoration: none; } .gauges-container { display: flex; justify-content: space-around; margin-bottom: 5px;} .gauge-wrapper { display: flex; flex-direction: column; align-items: center; } .gauge-ring { width: 70px; height: 70px; border-radius: 50%; display: flex; justify-content: center; align-items: center; background: #1e2030; border: 4px solid #4b5070; } .gauge-val { font-size: 1.1em; font-weight: bold; } .gauge-title { margin-top: 6px; font-size: 0.8em; color: #8fa1cd; } .status-green .gauge-ring { border-color: #00d2ff; box-shadow: 0 0 10px rgba(0,210,255,0.3); } .status-yellow .gauge-ring { border-color: #f6ad55; box-shadow: 0 0 10px rgba(246,173,85,0.3); } .status-red .gauge-ring { border-color: #fc8181; box-shadow: 0 0 10px rgba(252,129,129,0.3); } .tech-timestamp { font-size: 0.75em; color: #6b7280; text-align: center; margin-top: 8px; }</style>"
css_neumorphism = "<style>.stApp { background-color: #e0e5ec; color: #4a4a4a; } h1, h2, h3 { color: #4a4a4a !important; text-shadow: 1px 1px 2px rgba(163,177,198,0.5); } .neu-card { background-color: #e0e5ec; border-radius: 15px; padding: 15px; margin-bottom: 15px; box-shadow: 6px 6px 12px rgb(163,177,198,0.5), -6px -6px 12px rgba(255,255,255, 0.5); } .neu-header { display: flex; justify-content: space-between; margin-bottom: 10px; } .neu-room { font-size: 1.3em; font-weight: bold; color: #5a6a85; } .neu-data { background-color: #e0e5ec; border-radius: 8px; padding: 8px; margin-bottom: 8px; text-align: center; box-shadow: inset 4px 4px 8px rgb(163,177,198,0.5), inset -4px -4px 8px rgba(255,255,255, 0.5); font-size: 0.9em;} .neu-val { font-size: 1.3em; font-weight: 900; } .neu-green .neu-val { color: #2ecc71; } .neu-red .neu-val { color: #e74c3c; } .neu-yellow .neu-val { color: #f1c40f; } .neu-timestamp { font-size: 0.75em; color: #8fa1cd; text-align: right; margin-top: 5px; }</style>"
css_minimal = "<style>.min-card { background: #fff; border-radius: 10px; padding: 15px; margin-bottom: 12px; border: 1px solid #f0f0f0; box-shadow: 0 2px 5px rgba(0,0,0,0.05); } .min-status-green { border-left: 6px solid #28a745; } .min-status-yellow { border-left: 6px solid #ffc107; background-color: #fffffc; } .min-status-red { border-left: 6px solid #dc3545; background-color: #fffafa; } .min-status-offline { border-left: 6px solid #6c757d; opacity: 0.6; } .min-header { font-size: 1.1em; font-weight: bold; color: #222; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;} .bar-bg { background: #f0f0f0; border-radius: 8px; height: 8px; width: 100%; margin: 4px 0 12px 0; overflow: hidden; } .bar-fill-temp { height: 100%; border-radius: 8px; background: linear-gradient(90deg, #ff9a9e 0%, #fecfef 100%); } .bar-fill-humi { height: 100%; border-radius: 8px; background: linear-gradient(90deg, #a1c4fd 0%, #c2e9fb 100%); } .min-label { display: flex; justify-content: space-between; font-size: 0.85em; color: #666; font-weight: bold; } .min-timestamp { font-size: 0.75em; color: #aaa; text-align: right; margin-top: 5px; }</style>"

# 🌟 新增 1：賽博龐克風 (深黑底 + 霓虹邊框 + 紅色警告閃爍)
css_cyberpunk = """
<style>
    .stApp { background-color: #050510; color: #0ff; font-family: 'Courier New', Courier, monospace; }
    h1, h2, h3 { color: #0ff !important; text-shadow: 0 0 5px #0ff; }
    .cyber-card { background: rgba(0, 0, 0, 0.8); border: 1px solid #0ff; border-radius: 4px; padding: 15px; margin-bottom: 15px; box-shadow: inset 0 0 10px rgba(0,255,255,0.2), 0 0 5px rgba(0,255,255,0.5); position: relative; }
    .cyber-header { font-size: 1.4em; font-weight: bold; color: #0ff; margin-bottom: 10px; border-bottom: 1px dashed #0ff; padding-bottom: 5px; display: flex; justify-content: space-between;}
    .cyber-data { font-size: 1.1em; margin: 5px 0; color: #fff; }
    .cyber-val { color: #0f0; text-shadow: 0 0 5px #0f0; font-size: 1.2em; font-weight: bold;}
    /* 警告狀態：紅色閃爍與 Glitch 效果 */
    .cyber-alert { border: 2px solid #f00; box-shadow: inset 0 0 20px rgba(255,0,0,0.5), 0 0 15px rgba(255,0,0,0.8); animation: glitch-border 0.5s infinite; }
    .cyber-alert .cyber-header { color: #f00; border-bottom: 1px solid #f00; text-shadow: 2px 0 #0ff, -2px 0 #f00; animation: glitch-text 0.3s infinite; }
    .cyber-alert .cyber-val { color: #f00; text-shadow: 0 0 8px #f00; }
    .cyber-warn-badge { display: none; background: #f00; color: #fff; padding: 2px 6px; font-size: 0.6em; border-radius: 3px; animation: blink 0.5s infinite;}
    .cyber-alert .cyber-warn-badge { display: inline-block; }
    @keyframes glitch-border { 0%, 100% { opacity: 1; transform: translateX(0); } 50% { opacity: 0.8; transform: translateX(1px); } }
    @keyframes glitch-text { 0%, 100% { transform: skew(0deg); } 50% { transform: skew(-5deg); } }
    @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
</style>
"""

# 🌟 新增 2：玻璃擬物風 (漸層背景 + 毛玻璃 + 警告時紅色液體光暈)
css_glassmorphism = """
<style>
    /* 漸層背景營造立體感 */
    .stApp { background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%); color: #333; }
    h1, h2, h3 { color: #333 !important; }
    .glass-card { 
        background: rgba(255, 255, 255, 0.35); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); 
        border: 1px solid rgba(255, 255, 255, 0.6); box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1); 
        border-radius: 16px; padding: 15px; margin-bottom: 15px; position: relative; overflow: hidden;
    }
    .glass-header { font-size: 1.2em; font-weight: bold; margin-bottom: 12px; z-index: 2; position: relative;}
    .glass-flex { display: flex; justify-content: space-around; z-index: 2; position: relative;}
    .glass-item { text-align: center; }
    .glass-val { font-size: 1.5em; font-weight: 800; color: #2c3e50; }
    
    /* 正常狀態下的波浪液體特效 (用在底圖) */
    .glass-liquid { position: absolute; bottom: -50%; left: -50%; width: 200%; height: 200%; background: rgba(52, 152, 219, 0.15); border-radius: 40%; animation: liquid-spin 6s linear infinite; z-index: 0; }
    
    /* 警告狀態：波浪變紅加速、毛玻璃發出紅光 */
    .glass-alert { background: rgba(255, 200, 200, 0.4); border: 1px solid rgba(255, 100, 100, 0.6); box-shadow: 0 8px 32px 0 rgba(255, 50, 50, 0.25); }
    .glass-alert .glass-liquid { background: rgba(231, 76, 60, 0.3); animation: liquid-spin 3s linear infinite; }
    .glass-alert .glass-val { color: #c0392b; }
    @keyframes liquid-spin { 0% { transform: translateY(50%) rotate(0deg); } 100% { transform: translateY(50%) rotate(360deg); } }
</style>
"""

# 🌟 新增 3：極簡光環風 (乾淨背景 + Conic Gradient 環形 + 警告脈動心跳)
css_ringpulse = """
<style>
    .stApp { background-color: #f7f9fa; color: #1f2937; }
    h1, h2, h3 { color: #1f2937 !important; }
    .ring-card { background: #ffffff; border-radius: 12px; padding: 16px; margin-bottom: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.03); display: flex; flex-direction: column; align-items: center; border: 1px solid #edf2f7; transition: transform 0.2s;}
    .ring-header { font-size: 1.1em; font-weight: bold; width: 100%; text-align: left; margin-bottom: 10px; color: #4a5568;}
    .ring-container { display: flex; gap: 15px; justify-content: center; width: 100%;}
    
    /* 動態計算進度的光環 (透過 inline style 控制 conic-gradient) */
    .ring-gauge { width: 70px; height: 70px; border-radius: 50%; display: flex; align-items: center; justify-content: center; position: relative; }
    .ring-inner { width: 56px; height: 56px; background: #ffffff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 0.9em; box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);}
    
    /* 警告狀態：外框變紅，加入心跳脈動特效 */
    .ring-alert { border: 2px solid #fc8181; background: #fff5f5; animation: heartbeat 1.2s infinite; }
    .ring-alert .ring-inner { color: #e53e3e; }
    @keyframes heartbeat { 0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(229, 62, 62, 0.4); } 50% { transform: scale(1.03); box-shadow: 0 0 0 10px rgba(229, 62, 62, 0); } 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(229, 62, 62, 0); } }
</style>
"""

# 套用選擇的樣式
if style_choice == "經典簡約卡片": st.markdown(css_classic, unsafe_allow_html=True)
elif style_choice == "科技儀表板 (深色)": st.markdown(css_modern, unsafe_allow_html=True)
elif style_choice == "新擬態風格 (柔和)": st.markdown(css_neumorphism, unsafe_allow_html=True)
elif style_choice == "極簡進度條 (直觀)": st.markdown(css_minimal, unsafe_allow_html=True)
elif style_choice == "賽博龐克 (霓虹科幻)": st.markdown(css_cyberpunk, unsafe_allow_html=True)
elif style_choice == "玻璃擬物 (液體波紋)": st.markdown(css_glassmorphism, unsafe_allow_html=True)
elif style_choice == "極簡光環 (脈動警報)": st.markdown(css_ringpulse, unsafe_allow_html=True)

# ==========================================
# 3. 資料獲取與處理
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
# 4. 介面渲染函數 (整合 3 種新風格)
# ==========================================
def render_card(chamber_id, data_dict):
    temp = data_dict.get(chamber_id, {}).get('temp', "---")
    humi = data_dict.get(chamber_id, {}).get('humi', "---")
    time_raw = data_dict.get(chamber_id, {}).get('time', "無資料")
    
    temp_disp = f"{float(temp):.1f}°C" if temp != "---" else "--"
    humi_disp = f"{float(humi):.1f}%" if humi != "---" else "--"
    status = get_status_color(temp, humi)
    
    time_disp = str(time_raw).split(" ")[-1] if " " in str(time_raw) else time_raw
    sheet_link = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}"
    
    # 計算百分比，用於進度條或光環填充 (溫度假設最高 40，濕度最高 100)
    temp_pct = min((float(temp) / 40.0) * 100, 100) if temp != "---" else 0
    humi_pct = min((float(humi) / 100.0) * 100, 100) if humi != "---" else 0

    if style_choice == "經典簡約卡片":
        return f'<div class="sensor-card status-{status}"><div class="card-header"><span class="room-name">{chamber_id}</span></div><div class="data-row">Temp: <span class="data-val">{temp_disp}</span></div><div class="data-row">Humidity: <span class="data-val">{humi_disp}</span></div><div class="timestamp">{time_disp}</div></div>'
    
    elif style_choice == "科技儀表板 (深色)":
        return f'<div class="tech-card status-{status}"><div class="tech-header"><span class="tech-room">{chamber_id}</span></div><div class="gauges-container"><div class="gauge-wrapper"><div class="gauge-ring"><span class="gauge-val">{temp_disp}</span></div></div><div class="gauge-wrapper"><div class="gauge-ring"><span class="gauge-val">{humi_disp}</span></div></div></div><div class="tech-timestamp">{time_disp}</div></div>'
    
    elif style_choice == "新擬態風格 (柔和)":
        return f'<div class="neu-card neu-{status}"><div class="neu-header"><span class="neu-room">{chamber_id}</span></div><div class="neu-data">溫度 <br><span class="neu-val">{temp_disp}</span></div><div class="neu-data">濕度 <br><span class="neu-val">{humi_disp}</span></div></div>'
    
    elif style_choice == "極簡進度條 (直觀)":
        icon = "🔴" if status == "red" else "🟢"
        return f'<div class="min-card min-status-{status}"><div class="min-header"><span>{chamber_id}</span><span>{icon}</span></div><div class="bar-bg"><div class="bar-fill-temp" style="width: {temp_pct}%;"></div></div><div class="bar-bg"><div class="bar-fill-humi" style="width: {humi_pct}%;"></div></div></div>'
    
    # 🌟 新風格 1：賽博龐克
    elif style_choice == "賽博龐克 (霓虹科幻)":
        alert_class = "cyber-alert" if status == "red" else ""
        return f"""
        <div class="cyber-card {alert_class}">
            <div class="cyber-header">
                <span>{chamber_id}</span>
                <span class="cyber-warn-badge">SYS.WARN</span>
            </div>
            <div class="cyber-data">TMP: <span class="cyber-val">{temp_disp}</span></div>
            <div class="cyber-data">HUM: <span class="cyber-val">{humi_disp}</span></div>
            <div style="font-size:0.7em; color:#888; text-align:right; margin-top:8px;">LAST_SYNC: {time_disp}</div>
        </div>
        """
    
    # 🌟 新風格 2：玻璃擬物
    elif style_choice == "玻璃擬物 (液體波紋)":
        alert_class = "glass-alert" if status == "red" else ""
        return f"""
        <div class="glass-card {alert_class}">
            <div class="glass-liquid" style="top: {100 - (humi_pct * 0.8)}%;"></div>
            <div class="glass-header">{chamber_id}</div>
            <div class="glass-flex">
                <div class="glass-item"><div style="font-size:0.8em; color:#555;">溫度</div><div class="glass-val">{temp_disp}</div></div>
                <div class="glass-item"><div style="font-size:0.8em; color:#555;">濕度</div><div class="glass-val">{humi_disp}</div></div>
            </div>
        </div>
        """
        
    # 🌟 新風格 3：極簡光環
    elif style_choice == "極簡光環 (脈動警報)":
        alert_class = "ring-alert" if status == "red" else ""
        # 使用 inline CSS 的 conic-gradient 來繪製圓環進度
        color_t = "#fc8181" if status == "red" else "#4299e1"
        color_h = "#fc8181" if status == "red" else "#48bb78"
        return f"""
        <div class="ring-card {alert_class}">
            <div class="ring-header">{chamber_id}</div>
            <div class="ring-container">
                <div style="text-align:center;">
                    <div class="ring-gauge" style="background: conic-gradient({color_t} {temp_pct}%, #edf2f7 0);">
                        <div class="ring-inner">{temp_disp}</div>
                    </div>
                </div>
                <div style="text-align:center;">
                    <div class="ring-gauge" style="background: conic-gradient({color_h} {humi_pct}%, #edf2f7 0);">
                        <div class="ring-inner">{humi_disp}</div>
                    </div>
                </div>
            </div>
        </div>
        """

# ==========================================
# 5. 主畫面佈局
# ==========================================
Chambers = {
    "5F": ["502", "503", "504", "505", "509", "510", "511"],
    "6F": ["602", "603", "604", "605", "607", "608"],
    "7F": ["703", "706", "707", "708"],
    "8F": ["803", "804", "808", "809", "810"]
}

data_dict = get_latest_data()

for floor, rooms in Chambers.items():
    st.markdown(f"### 📍 {floor} Chamber")
    cols = st.columns(4) 
    for i, chamber in enumerate(rooms):
        with cols[i % 4]:
            st.markdown(render_card(chamber, data_dict), unsafe_allow_html=True)
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
