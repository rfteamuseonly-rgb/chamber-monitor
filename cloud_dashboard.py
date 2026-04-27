import streamlit as st
import pandas as pd
import time
import urllib.parse

# 設定網頁標題與寬度
st.set_page_config(page_title="Chamber 環境雲端看板", layout="wide")

# ==========================================
# 1. CSS 樣式設計 (完全保留您最喜歡的卡片風格)
# ==========================================
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .sensor-card {
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        transition: transform 0.2s;
        font-family: "Microsoft JhengHei", sans-serif;
    }
    .sensor-card:hover { transform: translateY(-2px); box-shadow: 0 6px 12px rgba(0,0,0,0.15); }

    /* 狀態顏色定義 (紅綠燈底色) */
    .status-green { border-left: 8px solid #28a745; background-color: #edfaf0; }
    .status-yellow { border-left: 8px solid #ffc107; background-color: #fff3cd; }
    .status-red { border-left: 8px solid #dc3545; background-color: #f8d7da; }
    .status-offline { border-left: 8px solid #6c757d; background-color: #f2f2f2; }

    .card-header {
        display: flex; justify-content: space-between; align-items: center;
        margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 8px;
    }
    .room-name { font-size: 1.4em; font-weight: bold; color: #333; }
    .history-btn { 
        background-color: #4a90e2; color: white; 
        padding: 2px 10px; border-radius: 4px; font-size: 0.8em; text-decoration: none;
    }
    .data-row { font-size: 1.1em; margin: 5px 0; color: #444; }
    .data-val { font-weight: bold; margin-left: 5px; }
    .timestamp { font-size: 0.8em; color: #999; margin-top: 10px; text-align: right;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 設定 Google Sheets 來源
# ==========================================
# ⚠️ 請把引號內的文字換成您剛剛複製的 Sheet ID
# ⚠️ 1. 您的試算表 ID
SHEET_ID = "17msOHAvXZ9iND5fMJVUd7n3C_TFXD-uTFH4rvVLwJ7k".strip()

# ⚠️ 2. 請將下方的 "0" 換成您網址列最後面的 gid 數字
GID = "0" 

# 直接使用 gid 來抓取，徹底避開中文名稱編碼問題
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid={GID}&tq=SELECT%20*%20ORDER%20BY%20A%20DESC%20LIMIT%2050"

@st.cache_data(ttl=300) # 設定快取 10 秒，避免太多人看時塞爆 Google
def get_latest_data():
    try:
        # 讀取雲端 CSV
        df = pd.read_csv(CSV_URL)
        # 統一欄位名稱
        df.columns = ['更新時間', 'Chamber', '溫度', '濕度', '狀態']
        df['Chamber'] = df['Chamber'].astype(str)
        
        # 過濾：每個 Chamber 號碼只保留最新的一筆資料
        latest_df = df.drop_duplicates(subset=['Chamber'], keep='first')
        
        # 轉換成方便讀取的字典格式
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

def render_card(chamber_id, data_dict):
    if chamber_id in data_dict:
        temp = data_dict[chamber_id]['temp']
        humi = data_dict[chamber_id]['humi']
        update_time = data_dict[chamber_id]['time']
        
        temp_disp = f"{float(temp):.1f}°C" if temp != "---" else "--"
        humi_disp = f"{float(humi):.1f}%" if humi != "---" else "--"
        status = get_status_color(temp, humi)
        
        # 把日期去掉，只顯示時間 (HH:MM:SS)
        time_disp = str(update_time).split(" ")[-1] if " " in str(update_time) else update_time
    else:
        temp_disp, humi_disp, time_disp, status = "--", "--", "無資料", "offline"

    # History 按鈕現在連往 Google Sheets 方便看歷史數據
    sheet_link = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}"
    
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

# ==========================================
# 3. 主程式介面
# ==========================================
st.title("🏭 Chamber 溫濕度雲端即時監控")
st.markdown("---")

placeholder = st.empty()

# 設備清單 (根據您的房間號碼)
Chamber_5F = ["502", "503", "504", "505", "509", "510", "511"]
Chamber_6F = ["602", "603", "604", "605", "607", "608"]
Chamber_7F = ["703", "706", "707", "708"]
Chamber_8F = ["803", "804", "808", "809", "810"]

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
        cols_6 = st.columns(4)
        for i, chamber in enumerate(Chamber_7F):
            with cols_6[i % 4]:
                st.markdown(render_card(chamber, data_dict), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader("📍 8F Chamber")
        cols_6 = st.columns(4)
        for i, chamber in enumerate(Chamber_8F):
            with cols_6[i % 4]:
                st.markdown(render_card(chamber, data_dict), unsafe_allow_html=True)

    # 暫停 10 秒後重新整理畫面 (避免狂刷 Google API)
    time.sleep(300)
    st.rerun()
