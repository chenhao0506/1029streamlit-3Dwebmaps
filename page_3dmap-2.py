import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


st.title("Plotly 3D 地圖 (向量 - 地球儀-地震)")

# --- 1. 載入 Plotly 內建的範例資料 ---
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/earthquakes-23k.csv")

# --- 2. 建立 3D 地理散點圖 (scatter_geo) ---
fig = px.scatter_geo(
    df,
    lat = "Latitude",
    lon = "Longitude",
    color = "Magnitude",      # 依據地震規模上色
    hover_name="Date",   # 滑鼠懸停時顯示日期
    size="Magnitude",             # 點子大小代表地震規模
    projection="orthographic",
)

st.plotly_chart(fig, use_container_width=True)


st.title("Plotly 3D 地圖 (網格 - 全球氣溫網格)")

# --- 1. 讀取範例 DEM 資料 ---
z_data = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/heatmap_data.csv")

# --- 2. 建立 3D Surface 圖 ---
fig = go.Figure(
    data=[
        go.Surface(
            z=z_data.values,
            colorscale="RdBu_r",
            reversescale=True
        )
    ] 
)

# --- 3. 調整 3D 視角和外觀 ---
fig.update_layout(
    title="全球氣溫格網（模擬資料)",
    width=800,
    height=700,
    scene=dict(
        xaxis_title='經度 (X)',
        yaxis_title='緯度 (Y)',
        zaxis_title='海拔 (Z)'
    )
)

# --- 4. 在 Streamlit 中顯示 ---
st.plotly_chart(fig, use_container_width=True)