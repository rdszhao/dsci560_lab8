# %%
import pandas as pd
import folium
from folium.plugins import HeatMap

df = get_data(10, 29, dur=48)
avg_pressure_df = df.groupby(['latitude', 'longitude'])['BMP280 Barometer'].mean().reset_index()
heatmap_data = avg_pressure_df[['latitude', 'longitude', 'BMP280 Barometer']].values.tolist()
center_lat = df['latitude'].mean()
center_lon = df['longitude'].mean()
folium_map = folium.Map(location=[center_lat, center_lon], zoom_start=12)
HeatMap(heatmap_data, radius=10, max_zoom=13).add_to(folium_map)
folium_map.save("pressure_heatmap.html")