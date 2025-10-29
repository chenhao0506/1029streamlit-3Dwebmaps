import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# 設定頁面標題
st.title("🌎 Plotly 3D 地圖展示 (向量)")

## --- 第一個圖表：3D 地理散點圖 (地震) ---
st.header("1. 3D 地理散點圖 (地球儀 - 地震)")

# 1. 載入 Plotly 內建的範例資料
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/earthquakes-23k.csv")

# 2. 建立 3D 地理散點圖 (scatter_geo)
# 🚨 修正: 將 'color' 和 'hover_name' 替換為資料框中現有的欄位。
# 資料框中可用的欄位為: 'Date', 'Latitude', 'Longitude', 'Magnitude'
fig_earthquake = px.scatter_geo(
    df,
    lat="Latitude",
    lon="Longitude",
    color="Magnitude",      
    hover_name="Date",      
    projection="orthographic", 
    title="全球地震分佈 (23k 筆資料)"
)

st.plotly_chart(fig_earthquake, use_container_width=True)

st.title("Plotly 3D 地圖 (網格 -聖布魯諾山高程)")

# --- 1. 讀取範例 DEM 資料 ---
MT_BRUNO_URL = "https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv"
z_data_bruno = pd.read_csv(MT_BRUNO_URL)

# --- 2. 建立 3D Surface 圖 ---
fig_bruno = go.Figure(
    data=[
        go.Surface(
            z=z_data_bruno.values,
            colorscale="Earth", # 設定為適合地形的顏色方案
            reversescale=True
        )
    ] 
)

# --- 3. 調整 3D 視角和外觀 ---
fig_bruno.update_layout(
    title="聖布魯諾山脈高程 (Surface Plot)",
    autosize=False,
    width=800,
    height=700,
    scene=dict(
        xaxis_title='X 軸',
        yaxis_title='Y 軸',
        zaxis_title='海拔高度 (Z)'
    )
)

# --- 4. 在 Streamlit 中顯示 ---
st.plotly_chart(fig_bruno, use_container_width=True)