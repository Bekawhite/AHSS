# nairobi_health_map_final.py
import streamlit as st
import pandas as pd
import folium
import json
from pathlib import Path
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster, Fullscreen

# --- Page Configuration ---
st.set_page_config(page_title="Nairobi Health Facilities - Official Boundaries", page_icon="🏥", layout="wide")
st.title("🏥 Nairobi County Health Facilities Map")
st.markdown("### Official Boundaries & 494 Health Facilities Across 17 Sub-Counties")

# --- Load Facility Data (Your existing `load_all_facilities()` function here) ---
# ... (Paste your complete `load_all_facilities()` function from your original code) ...
@st.cache_data
def load_all_facilities():
    # ... (Your full function with all 494 facilities) ...
    pass

# --- Load Official GeoJSON Boundaries ---
@st.cache_data
def load_official_boundaries():
    """Loads the official sub-county GeoJSON file."""
    # IMPORTANT: Update this path to where you saved the downloaded file
    geo_json_path = Path("nairobi_sub_counties.geojson")

    if not geo_json_path.exists():
        st.error(f"Boundary file not found at {geo_json_path}. Please download the official GeoJSON from HDX or KNBS and place it in the app directory.")
        st.stop()

    with open(geo_json_path, 'r') as f:
        return json.load(f)

# --- Map Creation Function ---
def create_nairobi_map(facilities_df, sub_counties_geojson):
    """Creates the Folium map with official boundaries and facility markers."""

    # Center map on Nairobi
    m = folium.Map(location=[-1.2921, 36.8219], zoom_start=11, tiles='CartoDB positron', control_scale=True)
    folium.TileLayer('OpenStreetMap', name='Street Map').add_to(m)
    folium.TileLayer('CartoDB voyager', name='Voyager (Light)').add_to(m)
    Fullscreen().add_to(m)

    # --- 1. Add Official Sub-County Boundaries (Blue Lines) ---
    folium.GeoJson(
        sub_counties_geojson,
        name='Sub-County Boundaries',
        style_function=lambda feature: {
            'color': '#0055CC',  # Blue color
            'weight': 2.5,
            'fillOpacity': 0,
            'opacity': 0.8,
        },
        tooltip=folium.GeoJsonTooltip(fields=['Name'], aliases=['Sub-County:'], localize=True),
    ).add_to(m)

    # --- 2. Add Facility Markers (Your existing marker code) ---
    # ... (Paste your marker creation code from your original `create_nairobi_map_with_boundaries` function) ...
    type_colors = {'Private': '#1E88E5', 'Public': '#000000', 'Faith Based': '#43A047', 'NGO': '#E53935'}
    marker_cluster = MarkerCluster(name='Health Facilities').add_to(m)

    for _, row in facilities_df.iterrows():
        color = type_colors.get(row['Type'], '#757575')
        popup_html = f"<b>🏥 {row['Facility Name']}</b><br>📍 {row['Sub-County']}<br>🏷️ {row['Type']}"
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=6,
            popup=popup_html,
            tooltip=f"{row['Facility Name']} ({row['Type']})",
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.85
        ).add_to(marker_cluster)

    # --- 3. Add Legend (Your existing legend code) ---
    # ... (Paste your legend HTML code) ...

    folium.LayerControl().add_to(m)
    return m

# --- Main App Execution ---
def main():
    # Load data
    with st.spinner("Loading health facilities and official boundaries..."):
        facilities_df = load_all_facilities()
        sub_counties_geojson = load_official_boundaries()

    # Sidebar
    with st.sidebar:
        st.header("📊 Nairobi County Overview")
        st.metric("Total Sub-Counties", 17)
        st.metric("Total Health Facilities", len(facilities_df))
        st.markdown("---")
        st.subheader("📈 Facilities by Sub-County")
        for sc, count in facilities_df['Sub-County'].value_counts().items():
            st.metric(sc, count)
        st.markdown("---")
        st.info("**Boundary Data:** Official GeoJSON from KNBS/HDX.\n\n💡 **Hover** over dots for facility name.")

    # Display map
    st.markdown("### 🗺️ Interactive Map")
    nairobi_map = create_nairobi_map(facilities_df, sub_counties_geojson)
    st_folium(nairobi_map, width='100%', height=700)

    # Statistics and data table (Your existing code)
    # ...

if __name__ == "__main__":
    main()
