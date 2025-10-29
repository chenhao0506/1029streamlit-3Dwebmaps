import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


st.title("Plotly 3D 地圖 (向量 - 全球航班起始點)")

# --- 1. 載入 Plotly 內建的範例資料 ---
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/2011_february_aa_flight_paths.csv")

# --- 2. 建立 3D 地理散點圖 (scatter_geo) ---
fig = px.scatter_geo(
    df,
    lat="start_lat",    
    lon="start_lon",    
    color="airport",   
    hover_name="airport", 
    size=None,          
    projection="orthographic",
)

st.plotly_chart(fig, use_container_width=True)


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