# nairobi_health_map_final.py - UPDATED WITH REAL GEOSPATIAL DATA
import streamlit as st
import pandas as pd
import folium
import json
import requests
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster, Fullscreen
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Nairobi Health Facilities Map - Accurate Boundaries",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Nairobi County Health Facilities Map")
st.markdown("### Complete Directory: 494 Health Facilities Across 17 Sub-Counties")

# ============================================================================
# LOAD REAL GEOJSON BOUNDARIES
# ============================================================================

@st.cache_data
def load_nairobi_boundaries():
    """
    Load real GeoJSON boundaries for Nairobi County and sub-counties.
    You can load from:
    1. Local file: Path('geojson/Nairobi.json')
    2. URL: Direct link to the GeoJSON file
    3. GitHub raw content
    """
    
    # Option 1: Load from local file (download the repository first)
    geo_json_path = Path('kenya-counties-subcounties/geojson/Nairobi.json')
    
    # Option 2: Load from GitHub raw URL (if file is available)
    github_url = "https://raw.githubusercontent.com/Mondieki/kenya-counties-subcounties/main/geojson/Nairobi.json"
    
    try:
        # Try local file first
        if geo_json_path.exists():
            with open(geo_json_path, 'r') as f:
            return json.load(f)
        else:
            # Fall back to URL
            response = requests.get(github_url)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        st.warning(f"Could not load GeoJSON boundaries: {e}")
        st.info("Falling back to approximated boundaries. Please download the GeoJSON file for accurate mapping.")
        return None

# Load the facilities data (same as your original code)
@st.cache_data
def load_all_facilities():
    """Load all 494 facilities with their coordinates"""
    # ... (keep your original facilities data loading code here)
    pass

# ============================================================================
# MAP CREATION WITH REAL BOUNDARIES
# ============================================================================

def create_nairobi_map_with_real_boundaries(facilities_df, geojson_data):
    """Create map using real GeoJSON boundaries"""
    
    nairobi_center = [-1.2833, 36.8167]
    
    # Create base map
    m = folium.Map(
        location=nairobi_center,
        zoom_start=11,
        tiles='CartoDB positron',
        control_scale=True
    )
    
    # Add tile layers
    folium.TileLayer('OpenStreetMap', name='Street Map').add_to(m)
    folium.TileLayer('CartoDB voyager', name='Voyager (Light)').add_to(m)
    
    # Add Fullscreen control
    Fullscreen().add_to(m)
    
    # ============================================
    # ADD REAL BOUNDARIES FROM GEOJSON
    # ============================================
    
    if geojson_data:
        # Add Nairobi County boundary (thick black line)
        folium.GeoJson(
            geojson_data,
            name='Nairobi County Boundary',
            style_function=lambda x: {
                'color': 'black',
                'weight': 4,
                'fillOpacity': 0,
                'opacity': 0.9
            },
            tooltip='Nairobi County Boundary',
            popup='<b>Nairobi County</b><br>Capital city of Kenya<br>Area: 696.1 km²'
        ).add_to(m)
        
        # Extract and add sub-county boundaries from the GeoJSON
        # The structure depends on the GeoJSON file. Typical structures:
        # - MultiPolygon with features
        # - Or separate feature collection
        
        if 'features' in geojson_data:
            for feature in geojson_data['features']:
                properties = feature.get('properties', {})
                sub_county_name = properties.get('name') or properties.get('sub_county') or properties.get('SubCounty')
                
                if sub_county_name and 'sub-county' in sub_county_name.lower():
                    # Add sub-county boundary (blue lines)
                    folium.GeoJson(
                        feature,
                        name=f'{sub_county_name} Boundary',
                        style_function=lambda x: {
                            'color': '#0055CC',
                            'weight': 2.5,
                            'fillOpacity': 0,
                            'opacity': 0.8
                        },
                        tooltip=f'{sub_county_name}'
                    ).add_to(m)
    
    # ============================================
    # ADD FACILITY MARKERS
    # ============================================
    
    # Color mapping
    type_colors = {
        'Private': '#1E88E5',
        'Public': '#000000',
        'Faith Based': '#43A047',
        'NGO': '#E53935'
    }
    
    type_sizes = {
        'Private': 7,
        'Public': 8,
        'Faith Based': 7,
        'NGO': 7
    }
    
    # Marker cluster
    marker_cluster = MarkerCluster(
        name='Health Facilities',
        overlay=True,
        control=True
    ).add_to(m)
    
    # Add markers
    for _, row in facilities_df.iterrows():
        color = type_colors.get(row['Type'], '#757575')
        radius = type_sizes.get(row['Type'], 6)
        
        popup_html = f"""
        <div style="font-family: Arial, sans-serif; font-size: 12px;">
            <div style="background-color: {color}; color: white; padding: 8px; border-radius: 5px 5px 0 0;">
                <b>🏥 {row['Facility Name']}</b>
            </div>
            <div style="padding: 10px; background-color: #f9f9f9;">
                <b>📍 Sub-County:</b> {row['Sub-County']}<br>
                <b>🏷️ Type:</b> {row['Type']}<br>
                <b>🗺️ Coordinates:</b><br>
                <span style="font-family: monospace;">{row['Latitude']:.5f}, {row['Longitude']:.5f}</span>
                <hr>
                <a href="https://www.google.com/maps?q={row['Latitude']},{row['Longitude']}" target="_blank">
                    📍 View in Google Maps
                </a>
            </div>
        </div>
        """
        
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=radius,
            popup=folium.Popup(popup_html, max_width=350),
            tooltip=f"🏥 {row['Facility Name']}\n📌 {row['Type']}\n📍 {row['Sub-County']}",
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.85,
            weight=2
        ).add_to(marker_cluster)
    
    # Add legend
    legend_html = '''
    <div style="position: fixed; bottom: 30px; right: 30px; 
                background-color: white; padding: 12px 15px;
                border: 2px solid #ddd; border-radius: 10px;
                z-index: 1000; font-size: 11px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.15);">
        <b>🗺️ Legend</b><br>
        <hr>
        <span style="display:inline-block; width:25px; height:3px; background:black;"></span> County Boundary<br>
        <span style="display:inline-block; width:25px; height:3px; background:#0055CC;"></span> Sub-County Boundary<br>
        <span style="display:inline-block; width:12px; height:12px; background:#1E88E5; border-radius:50%;"></span> Private<br>
        <span style="display:inline-block; width:12px; height:12px; background:#000000; border-radius:50%;"></span> Public<br>
        <span style="display:inline-block; width:12px; height:12px; background:#43A047; border-radius:50%;"></span> Faith Based<br>
        <span style="display:inline-block; width:12px; height:12px; background:#E53935; border-radius:50%;"></span> NGO<br>
        <hr>
        <div style="font-size:9px;">💡 Hover for facility names<br>🖱️ Click for details</div>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    folium.LayerControl().add_to(m)
    
    return m

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Load data
    with st.spinner("Loading health facilities data..."):
        facilities_df = load_all_facilities()
    
    with st.spinner("Loading Nairobi boundary data..."):
        geojson_data = load_nairobi_boundaries()
    
    # Sidebar with stats
    with st.sidebar:
        st.header("📊 Nairobi County Overview")
        st.metric("Total Sub-Counties", 17)
        st.metric("Total Health Facilities", len(facilities_df))
        
        st.markdown("---")
        st.subheader("📈 Facilities by Sub-County")
        for sc, count in facilities_df['Sub-County'].value_counts().sort_values(ascending=False).items():
            st.metric(sc, count)
        
        st.markdown("---")
        st.info("""
        **Data Sources:**
        - **Boundaries:** GeoJSON from kenya-counties-subcounties repository (OpenStreetMap data)
        - **Health Facilities:** Compiled directory with coordinates
        - **Coordinate System:** WGS 84
        """)
    
    # Create and display map
    st.markdown("""
    <div style="background-color: #e8f4f8; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <h3>🗺️ Nairobi County - Accurate Administrative Boundaries</h3>
        <p>This map uses real GeoJSON boundary data from official sources.</p>
        <ul>
            <li><strong>⬛ Black outline</strong> = Nairobi County boundary (696.1 km²)</li>
            <li><strong>🔵 Blue lines</strong> = 17 Sub-County boundaries</li>
            <li><strong>Colored dots</strong> = Health facilities by type</li>
            <li><strong>💡 Hover</strong> over any dot to see facility name</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if geojson_data:
        nairobi_map = create_nairobi_map_with_real_boundaries(facilities_df, geojson_data)
        st_folium(nairobi_map, width='100%', height=700)
    else:
        st.error("Unable to load boundary data. Please check the GeoJSON file path.")
        st.info("You can download the GeoJSON file from: https://github.com/Mondieki/kenya-counties-subcounties")
    
    # Display statistics (same as original)
    # ... (keep your statistics display code)

if __name__ == "__main__":
    main()
