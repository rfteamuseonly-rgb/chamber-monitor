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
        ["經典簡約卡片", "科技儀表板 (深色)"],
        index=0
    )
    st.markdown("---")
    st.markdown("💡 **提示**：切換風格後，畫面會立即更新為您選擇的樣式。資料每 5 分鐘會自動刷新一次。")

# ==========================================
# 1. CSS 樣式設計 (包含兩種風格)
# ==========================================
# --- 風格 A: 原版經典卡片 ---
css_classic = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .sensor-card {
        border-radius: 8px; padding: 15px; margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: 1px solid #e0e0e0;
        transition: transform 0.2s; font-family: "Microsoft JhengHei", sans-serif;
        background-color: white; color: #333;
    }
    .sensor-card:hover { transform: translateY(-2px); box-shadow: 0 6px 12px rgba(0,0,0,0.15); }
    .status-green { border-left: 8px solid #28a745; background-color: #f5faf6; }
    .status-yellow { border-left: 8px solid #ffc107; background-color: #ffffeb; }
    .status-red { border-left: 8px solid #dc3545; background-color: #f8d7da; }
    .status-offline { border-left: 8px solid #6c757d; background-color: #f2f2f2; }
    .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 8px; }
    .room-name { font-size: 1.4em; font-weight: bold; color: #333; }
    .history-btn { background-color: #a9d0fc; color: white; padding: 2px 10px; border-radius: 4px; font-size: 0.8em; text-decoration: none; }
    .data-row { font-size: 1.1em; margin: 5px 0; color: #444; }
    .data-val { font-weight: bold; margin-left: 5px; }
    .timestamp { font-size: 0.8em; color: #999; margin-top: 10px; text-align: right;}
</style>
"""

# --- 風格 B: 科技儀表板 ---
css_modern = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 將背景稍微改暗一點以凸顯科技感 (僅限資料區塊) */
    .stApp { background-color: #121420; color: white; }
    h1, h2, h3, h4, h5, h6, span { color: #e2e8f0 !important; }
    
    .tech-card {
        background: linear-gradient(145deg, #2A2D43, #1e2030);
        border-radius: 12px; padding: 15px; margin-bottom: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.4);
        border: 1px solid #3b3f5c;
        font-family: "Microsoft JhengHei", sans-serif;
    }
    .tech-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #4b5070; padding-bottom: 10px; margin-bottom: 15px; }
    .tech-room { font-size: 1.4em; font-weight: bold; color: #fff; letter-spacing: 1px; }
    .history-btn-tech { background-color: transparent; border: 1px solid #5c638c; color: #8fa1cd !important; padding: 3px 10px; border-radius: 15px; font-size: 0.8em; text-decoration: none; transition: 0.3s; }
    .history-btn-tech:hover { background-color: #5c638c; color: #fff !important; }
    
    /* 圓形儀表板區塊 */
    .gauges-container { display: flex; justify-content: space-around; margin-bottom: 15px; }
    .gauge-wrapper { display: flex; flex-direction: column; align-items: center; }
    .gauge-ring {
        width: 85px; height: 85px; border-radius: 50%; display: flex; justify-content: center; align-items: center;
        background: #1e2030; position: relative; border: 5px solid #4b5070;
    }
    .gauge-val { font-size: 1.2em; font-weight: bold; z-index: 2; }
    .gauge-title { margin-top: 8px; font-size: 0.85em; color: #8fa1cd; }
    
    /* 狀態顏色定義 (發光效果) */
    .status-green .gauge-ring { border-color: #00d2ff; box-shadow: 0 0 15px rgba(0, 210, 255, 0.3), inset 0 0 10px rgba(0, 210, 255, 0.2); }
    .status-yellow .gauge-ring { border-color: #f6ad55; box-shadow: 0 0 15px rgba(246, 173, 85, 0.3), inset 0 0 10px rgba(246, 173, 85, 0.2); }
    .status-red .gauge-ring { border-color: #fc8181; box-shadow: 0 0 15px rgba(252, 129, 129, 0.4), inset 0 0 10px rgba(252, 129, 129, 0.2); }
    .status-offline .gauge-ring { border-color: #4a5568; opacity: 0.5; }
    
    /* 底部狀態提示條 */
    .tech-footer { border-radius: 6px; padding: 8px; font-size: 0.85em; display: flex; justify-content: space-between; align-items: center; background: rgba(0,0,0,0.2); }
    .status-green .tech-footer { background: rgba(0, 210, 255, 0.1); border-left: 4px solid #00d2ff; }
    .status-yellow .tech-footer { background: rgba(246, 173, 85, 0.1); border-left: 4px solid #f6ad55; }
    .status-red .tech-footer { background: rgba(252, 129, 129, 0.15); border-left: 4px solid #fc8181; color: #fc8181 !important; }
</style>
"""

# 依據選擇注入對應的 CSS
if style_choice == "經典簡約卡片":
    st.markdown(css_classic, unsafe_allow_html=True)
else:
    st.markdown(css_modern, unsafe_allow_html=True)


# ==========================================
# 2. 獲取資料邏輯 (保留您原有的設定)
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
            data_dict[row['Chamber']] = {
                "temp": row['溫度'],
                "humi": row['濕度'],
                "time": row['更新時間']
            }
        return data_dict
    except Exception as e:
        st.error(f"讀取 Google 表單失敗，錯誤原因：{e}")
        return {}

def get_status_color(temp, humi):
    if pd.isna(temp) or pd.isna(humi) or temp == "---" or humi == "---":
        return "offline"
    try:
        t, h = float(temp), float(humi)
        if t > 26 or h > 75: return "red"
        if (17 <= t <= 24) and (10 <= h <= 65): return "green"
        return "yellow"
    except:
        return "offline"

# ==========================================
# 3. 渲染介面函數
# ==========================================
def render_card(chamber_id, data_dict):
    if chamber_id in data_dict:
        temp = data_dict[chamber_id]['temp']
        humi = data_dict[chamber_id]['humi']
        update_time = data_dict[chamber_id]['time']
        
        temp_disp = f"{float(temp):.1f}°C" if temp != "---" else "--"
        humi_disp = f"{float(humi):.1f}%" if humi != "---" else "--"
        status = get_status_color(temp, humi)
        time_disp = str(update_time).split(" ")[-1] if " " in str(update_time) else update_time
    else:
        temp_disp, humi_disp, time_disp, status = "--", "--", "無資料", "offline"

    sheet_link = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}"
    
    # 依據選擇回傳對應的 HTML
    if style_choice == "經典簡約卡片":
        return f"""
        <div class="sensor-card status-{status}">
            <div class="card-header">
                <span class="room-name">{chamber_id}</span>
                <a href="{sheet_link}" target="_blank" class="history-btn">History</a>
            </div>
            <div class="card-body">
                <div class="data-row">Temp: <span class="data-val">{temp_disp}</span></div>
                <div class="data-row">Humidity: <span class="data-val">{humi_disp}</span></div>
                <div class="timestamp">Updated: {time_disp}</div>
            </div>
        </div>
        """
    else:
        # 定義科技風格的提示文字與圖示
        if status == "green": status_msg = "💧 當前溫濕度正常"; icon = "✅"
        elif status == "red": status_msg = "🔥 溫濕度偏高，請調試！"; icon = "⚠️"
        elif status == "yellow": status_msg = "⚡ 數值邊緣，請注意"; icon = "👀"
        else: status_msg = "連線中斷"; icon = "🔌"

        return f"""
        <div class="tech-card status-{status}">
            <div class="tech-header">
                <span class="tech-room">{chamber_id}</span>
                <a href="{sheet_link}" target="_blank" class="history-btn-tech">⛭ History</a>
            </div>
            <div class="gauges-container">
                <div class="gauge-wrapper">
                    <div class="gauge-ring"><span class="gauge-val">{temp_disp}</span></div>
                    <div class="gauge-title">溫度 (Temp)</div>
                </div>
                <div class="gauge-wrapper">
                    <div class="gauge-ring"><span class="gauge-val">{humi_disp}</span></div>
                    <div class="gauge-title">濕度 (Humidity)</div>
                </div>
            </div>
            <div class="tech-footer">
                <span>{icon} {status_msg}</span>
                <span style="font-size: 0.85em; opacity: 0.6;">{time_disp}</span>
            </div>
        </div>
        """

# ==========================================
# 4. 主程式介面佈局
# ==========================================
st.title("🏭 Chamber 溫濕度雲端即時監控")
st.markdown("---")

placeholder = st.empty()

Chamber_5F = ["502", "503", "504", "505", "509", "510", "511"]
Chamber_6F = ["602", "603", "604", "605", "607", "608"]
Chamber_7F = ["703", "706", "707", "708"]
Chamber_8F = ["803", "804", "808", "809", "810"]

# 迴圈負責自動更新畫面資料
while True:
    data_dict = get_latest_data()
    
    with placeholder.container():
        st.subheader("📍 5F Chamber")
        cols = st.columns(4)
        for i, chamber in enumerate(Chamber_5F):
            with cols[i % 4]:
                st.markdown(render_card(chamber, data_dict), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader("📍 6F Chamber")
        cols_6 = st.columns(4)
        for i, chamber in enumerate(Chamber_6F):
            with cols_6[i % 4]:
                st.markdown(render_card(chamber, data_dict), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader("📍 7F Chamber")
        cols_7 = st.columns(4)
        for i, chamber in enumerate(Chamber_7F):
            with cols_7[i % 4]:
                st.markdown(render_card(chamber, data_dict), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader("📍 8F Chamber")
        cols_8 = st.columns(4)
        for i, chamber in enumerate(Chamber_8F):
            with cols_8[i % 4]:
                st.markdown(render_card(chamber, data_dict), unsafe_allow_html=True)

    # 暫停 300 秒後重新整理畫面
    time.sleep(300)
    st.rerun()
