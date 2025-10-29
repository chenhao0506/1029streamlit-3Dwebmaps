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

st.title("Pydeck 3D 地圖 (網格 - 舊金山高程模擬)")

# --- 1. 載入舊金山建築高度資料 (作為高程點位模擬) ---
ELEVATION_DATA_URL = 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/sf-bike-parking.json'

# 載入 JSON 格式的點位資料
df_dem = pd.read_json(ELEVATION_DATA_URL)

# 處理資料：將 'position' 欄位的 [lon, lat] 展開
df_dem['lon'] = df_dem['position'].apply(lambda x: x[0])
df_dem['lat'] = df_dem['position'].apply(lambda x: x[1])

# 設定地圖中心點和 GridLayer 參數 (舊金山區域)
base_lat, base_lon = 37.78, -122.42 
cell_size_param = 200 # 網格大小 (公尺)
elevation_scale_param = 10 # 放大高程視覺效果


# --- 2. 設定 Pydeck 圖層 (GridLayer) ---
layer_grid = pdk.Layer(
    'GridLayer',
    data=df_dem, # 使用舊金山資料
    get_position='[lon, lat]',
    get_elevation_weight='elevation', # 使用 'elevation' 欄位當作高度
    elevation_scale=elevation_scale_param,
    cell_size=cell_size_param,
    extruded=True,
    pickable=True, 
    color_range=[ # 添加顏色漸變
        [0, 255, 0], [255, 255, 0], [255, 140, 0], [255, 0, 0]
    ],
    get_color_weight='elevation',
)

# --- 3. 設定視角 (View) ---
view_state_grid = pdk.ViewState(
    latitude=base_lat, longitude=base_lon, zoom=12, pitch=50
)

# --- 4. 組合並顯示 (第二個地圖) ---
r_grid = pdk.Deck(
    layers=[layer_grid],
    initial_view_state=view_state_grid,
    tooltip={"text": "高程/建築高度: {elevationValue} 公尺"}
)
st.pydeck_chart(r_grid)