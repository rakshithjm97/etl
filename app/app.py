import streamlit as st
import geopandas as gpd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import folium
from streamlit_folium import folium_static

# Load .env variables
load_dotenv()
DB_URI = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@" \
         f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_engine(DB_URI)

st.set_page_config(page_title="Alabama Wetlands Viewer", layout="wide")

st.title("🌿 Alabama Wetlands Viewer")
st.markdown("Visualize wetlands data from the National Wetlands Inventory (NWI).")

# Choose layer
layer = st.selectbox("Choose a data layer to view", ["al_al_wetlands", "al_al_wetlands_project_metadata"])

@st.cache_data
def load_data(table):
    sql = f"SELECT * FROM {table} LIMIT 10000;"  # Limit for performance
    gdf = gpd.read_postgis(sql, con=engine, geom_col='geometry')
    return gdf

gdf = load_data(layer)

if gdf.empty:
    st.warning("No data found in the selected layer.")
else:
    st.success(f"{len(gdf)} features loaded.")

    # Center map on AL
    center = [32.8067, -86.7911]
    m = folium.Map(location=center, zoom_start=6, tiles="CartoDB positron")

    # Add data to map
    folium.GeoJson(
        gdf.to_json(),
        name="Wetlands",
        tooltip=folium.GeoJsonTooltip(fields=gdf.columns[:3].tolist(), aliases=["Field 1", "Field 2", "Field 3"]),
        style_function=lambda x: {"fillColor": "green", "color": "green", "weight": 1, "fillOpacity": 0.4}
    ).add_to(m)

    folium.LayerControl().add_to(m)

    folium_static(m, width=1100, height=700)
