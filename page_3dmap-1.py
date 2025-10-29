import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

st.title("Pydeck 3D 地圖 (向量 - 密度圖)")
st.header("1. 台北市 YouBike 租賃站點資料")

# --- 1. 生成範例資料 (向量) ---
url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"

data_youbike = pd.read_json(url)
data = data_youbike[['latitude','longitude']].rename(columns={'lng':'lon'})

center_lat = 25.0478
center_lon = 121.5170
data = pd.DataFrame({
'lat': center_lat + np.random.randn(1000) / 50,
'lon': center_lon + np.random.randn(1000) / 50,
})

# --- 2. 設定 Pydeck圖層 (Layer) ---
layer_hexagon = pdk.Layer( 
    'HexagonLayer',
    data = data,
    get_position = '[lon, lat]',
    radius = 100,
    elevation_scale = 4,
    elevation_range = [0, 1000],
    pickable = True,
    extruded = True,
)

# --- 3. 設定攝影機視角 (View State) ---
view_state_hexagon = pdk.ViewState( # 稍微改個名字避免混淆
    latitude = center_lat,
    longitude = center_lon,
    zoom=12,
    pitch=50,
)

# --- 4. 組合圖層和視角並顯示 (第一個地圖) ---
r_hexagon = pdk.Deck( # 稍微改個名字避免混淆
    layers=[layer_hexagon],
    initial_view_state=view_state_hexagon,
    tooltip={"text": "這個區域有 {elevationValue} 個熱點"}
)
st.pydeck_chart(r_hexagon)


# ===============================================
#          第二個地圖：模擬 DEM
# ===============================================

st.title("桃園市 DEM 模擬（Pydeck 3D 地圖）")

# --- 1. 模擬桃園 DEM 資料 ---
x, y = np.meshgrid(np.linspace(-1, 1, 60), np.linspace(-1, 1, 60))

# 模擬桃園地形（北低南高）
z = np.exp(-(x**2 + y**2) * 2) * 800 + np.random.rand(50, 50) * 200

data_dem_list = []
base_lat, base_lon = 24.99, 121.3
for i in range(50):
    for j in range(50):
        data_dem_list.append({
            "lon": base_lon + x[i, j] * 0.2,
            "lat": base_lat + y[i, j] * 0.15,
            "elevation": z[i, j]
        })
df_dem = pd.DataFrame(data_dem_list)

# --- 2. Pydeck GridLayer 設定 ---
layer_grid = pdk.Layer(
    "GridLayer",
    data=df_dem,
    get_position='[lon, lat]',
    get_elevation_weight='elevation',
    elevation_scale=1,
    cell_size=2000,
    extruded=True,
    pickable=True
)

# --- 3. 視角設定 ---
view_state_grid = pdk.ViewState(
    latitude=base_lat,
    longitude=base_lon,
    zoom=10,
    pitch=50
)

# --- 4. 顯示地圖 ---
r_grid = pdk.Deck(
    layers=[layer_grid],
    initial_view_state=view_state_grid,
    tooltip={"text": "海拔高度: {elevationValue} 公尺"}
)

st.pydeck_chart(r_grid)