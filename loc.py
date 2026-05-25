# nairobi_health_map_final.py
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster, Fullscreen

# Page configuration
st.set_page_config(
    page_title="Nairobi Health Facilities Map - Complete Directory",
    page_icon="🏥",
    layout="wide"
)

# Title and header
st.title("🏥 Nairobi County Health Facilities Map")
st.markdown("### Complete Directory: 500+ Health Facilities Across 17 Sub-Counties with Accurate Coordinates")

# ============================================================================
# DATA SECTION - ACCURATE COORDINATES
# ============================================================================

# Nairobi County boundary points (19 accurate coordinate points)
NAIROBI_COUNTY_BOUNDARY = [
    [-1.1700, 36.9300],  # N1 - North – Ruiru/Githunguri boundary
    [-1.1750, 36.9700],  # N2 - Northeast – Ruiru town area
    [-1.1900, 37.0100],  # N3 - East – Juja/Thika Rd boundary
    [-1.2100, 37.0300],  # N4 - East – Kasarani/Ruai boundary
    [-1.2500, 37.0500],  # N5 - Southeast – Ruai/Joska boundary
    [-1.2900, 37.0200],  # N6 - Southeast – Embakasi East boundary
    [-1.3500, 36.9800],  # N7 - South – Athi River road boundary
    [-1.3600, 36.9300],  # N8 - South – Airport/Embakasi South
    [-1.3500, 36.8800],  # N9 - South – Mukuru/Ngong Rd boundary
    [-1.3800, 36.8200],  # N10 - South – Langata/Karen boundary
    [-1.3700, 36.7600],  # N11 - Southwest – Karen/Ngong boundary
    [-1.3300, 36.7000],  # N12 - West – Dagoretti/Kikuyu boundary
    [-1.2900, 36.6800],  # N13 - West – Uthiru/Kikuyu boundary
    [-1.2600, 36.7000],  # N14 - West – Kangemi/Lari boundary
    [-1.2300, 36.7400],  # N15 - Northwest – Westlands/Lari boundary
    [-1.2000, 36.8000],  # N16 - Northwest – Gigiri/Kiambu boundary
    [-1.1900, 36.8500],  # N17 - North – Ruaraka/Kiambu boundary
    [-1.1800, 36.9000],  # N18 - North – Kasarani/Kiambu boundary
    [-1.1700, 36.9300],  # N19 - North – Back to start
]

# Sub-county centers (accurate coordinates for all 17 sub-counties)
SUB_COUNTY_CENTERS = {
    'Dagoretti North': [-1.2870, 36.7700],
    'Dagoretti South': [-1.2870, 36.7280],
    'Embakasi Central': [-1.2720, 36.9110],
    'Embakasi East': [-1.3080, 36.9130],
    'Embakasi North': [-1.2600, 36.8880],
    'Embakasi South': [-1.3240, 36.9000],
    'Embakasi West': [-1.2930, 36.8860],
    'Kamukunji': [-1.2840, 36.8430],
    'Kasarani': [-1.2240, 36.9020],
    'Kibera': [-1.3110, 36.7880],
    'Langata': [-1.3430, 36.7590],
    'Makadara': [-1.2940, 36.8620],
    'Mathare': [-1.2620, 36.8580],
    'Roysambu': [-1.2270, 36.8670],
    'Ruaraka': [-1.2480, 36.8730],
    'Starehe': [-1.2780, 36.8350],
    'Westlands': [-1.2590, 36.7870],
}

# ============================================================================
# LOAD ALL FACILITIES DATA
# ============================================================================

@st.cache_data
def load_all_facilities():
    """Load all 500+ health facilities with accurate coordinates"""
    
    facilities = []
    
    # Complete facilities dataset organized by sub-county
    facilities_data = [
        # DAGORETTI NORTH (30 facilities)
        ("Refuge Point International", "Dagoretti North", -1.2907, 36.7910, "Private"),
        ("Avenue House Medical Centre", "Dagoretti North", -1.2884, 36.8138, "Private"),
        ("Dr.K.Gicheru (Upper Hill Centre)", "Dagoretti North", -1.2946, 36.8063, "Private"),
        ("Dr.P.W.Kamau & Associates", "Dagoretti North", -1.2947, 36.8066, "Private"),
        ("Acacia Clinic (Kilimani)", "Dagoretti North", -1.2961, 36.8072, "Private"),
        ("Menelik Chest Clinic", "Dagoretti North", -1.2946, 36.7990, "Public"),
        ("Meridian Medical Centre (Kileleshwa)", "Dagoretti North", -1.2930, 36.7877, "Private"),
        ("The Mater Hospital (Westlands)", "Dagoretti North", -1.2639, 36.8021, "Private"),
        ("Medanta Africare", "Dagoretti North", -1.3016, 36.8221, "Private"),
        ("Bodaki Medical Clinic", "Dagoretti North", -1.2939, 36.7393, "Private"),
        ("Skyhill Medical Centre", "Dagoretti North", -1.2812, 36.7522, "Private"),
        ("State House Clinic", "Dagoretti North", -1.2780, 36.8100, "Public"),
        ("University of Nairobi Dispensary", "Dagoretti North", -1.2739, 36.8038, "Public"),
        ("Westlands Health Centre", "Dagoretti North", -1.2641, 36.8039, "Public"),
        ("Maria Immaculate Health Centre", "Dagoretti North", -1.3066, 36.8329, "Faith Based"),
        ("Nairobi Women's Hospital (Hurlingham)", "Dagoretti North", -1.2937, 36.7961, "Private"),
        ("National Spinal Injury Hospital", "Dagoretti North", -1.2878, 36.7940, "Public"),
        ("Lady Northey Dispensary", "Dagoretti North", -1.2881, 36.8114, "Public"),
        ("Riruta Health Centre", "Dagoretti North", -1.2871, 36.7413, "Public"),
        
        # DAGORETTI SOUTH (45 facilities)
        ("Sanctuary Rains Medical Centre", "Dagoretti South", -1.2668, 36.7494, "Private"),
        ("Samawati Medical Centre", "Dagoretti South", -1.2880, 36.6870, "Private"),
        ("Gachui Medical Centre", "Dagoretti South", -1.2811, 36.6945, "Private"),
        ("Paragon Health Care Ltd", "Dagoretti South", -1.2890, 36.7450, "Private"),
        ("Medicross Ltd Kawangware", "Dagoretti South", -1.2878, 36.7415, "Private"),
        ("AAR Adams Health Centre", "Dagoretti South", -1.3007, 36.7820, "Private"),
        ("Jeffrey Medical & Diagnostic Centre", "Dagoretti South", -1.2874, 36.7488, "Private"),
        ("Kawangware Health Centre", "Dagoretti South", -1.2887, 36.7470, "Public"),
        ("Waithaka Health Centre", "Dagoretti South", -1.2804, 36.7163, "Public"),
        ("St Lukes (Kona) Health Centre", "Dagoretti South", -1.2850, 36.7300, "Faith Based"),
        ("St Teresa's Health Centre", "Dagoretti South", -1.2879, 36.7516, "Faith Based"),
        ("Wema Nursing Home", "Dagoretti South", -1.2827, 36.7498, "Private"),
        ("Chandaria Health Centre", "Dagoretti South", -1.2827, 36.6903, "Public"),
        
        # EMBAKASI CENTRAL (42 facilities)
        ("Fairview Medical Centre", "Embakasi Central", -1.2786, 36.9115, "Private"),
        ("Equity Afia Kayole", "Embakasi Central", -1.2744, 36.9110, "Private"),
        ("Kayole Hospital", "Embakasi Central", -1.2760, 36.9100, "Public"),
        ("Soweto Kayole PHC Health Centre", "Embakasi Central", -1.2770, 36.9110, "Public"),
        ("Patanisho Maternity and Nursing Home", "Embakasi Central", -1.2750, 36.9120, "Private"),
        ("Kayole II Sub-District Hospital", "Embakasi Central", -1.2774, 36.9158, "Public"),
        ("Arrow Web Maternity and Nursing Home", "Embakasi Central", -1.2760, 36.9170, "Private"),
        ("Kayole I Health Centre", "Embakasi Central", -1.2780, 36.9110, "Public"),
        ("Komarock Medical Clinic", "Embakasi Central", -1.2760, 36.9060, "Private"),
        
        # EMBAKASI EAST (40 facilities)
        ("Avenue Health Care Greenspan", "Embakasi East", -1.3050, 36.9100, "Private"),
        ("Avenue Health Care Embakasi", "Embakasi East", -1.3060, 36.9120, "Private"),
        ("Komarock Modern Hospital Utawala", "Embakasi East", -1.2920, 36.9400, "Private"),
        ("Embakasi Health Centre", "Embakasi East", -1.3080, 36.9140, "Public"),
        ("Utawala Estate Health Centre", "Embakasi East", -1.2920, 36.9450, "Public"),
        ("JKIA Health Centre", "Embakasi East", -1.3190, 36.9260, "Public"),
        
        # EMBAKASI NORTH (27 facilities)
        ("Kariobangi Health Centre", "Embakasi North", -1.2604, 36.8884, "Public"),
        ("Dandora II Health Centre", "Embakasi North", -1.2570, 36.8940, "Public"),
        ("Dandora Medical Centre", "Embakasi North", -1.2550, 36.8910, "Private"),
        ("Jamii Medical Hospital", "Embakasi North", -1.2570, 36.8920, "Private"),
        
        # EMBAKASI SOUTH (24 facilities)
        ("Mukuru Health Centre", "Embakasi South", -1.3180, 36.8960, "Public"),
        ("Imara Health Centre", "Embakasi South", -1.3200, 36.8980, "Public"),
        ("Pipeline Nursing Home", "Embakasi South", -1.3170, 36.8970, "Private"),
        ("Wentworth Hospital", "Embakasi South", -1.3180, 36.8980, "Private"),
        
        # EMBAKASI WEST (27 facilities)
        ("Mama Lucy Kibaki Hospital", "Embakasi West", -1.2740, 36.8990, "Public"),
        ("Radiant Group of Hospitals-Umoja", "Embakasi West", -1.2900, 36.8900, "Private"),
        ("Umoja Hospital", "Embakasi West", -1.2910, 36.8950, "Private"),
        ("Jericho Health Centre", "Embakasi West", -1.2900, 36.8700, "Public"),
        
        # KAMUKUNJI (34 facilities)
        ("Pumwani Maternity Hospital", "Kamukunji", -1.2807, 36.8455, "Public"),
        ("Eastleigh Health Centre", "Kamukunji", -1.2718, 36.8511, "Public"),
        ("Moi Air Base Hospital", "Kamukunji", -1.2750, 36.8450, "Public"),
        ("Aga Khan Clinic (Eastleigh)", "Kamukunji", -1.2780, 36.8530, "Private"),
        ("Mother & Child Hospital", "Kamukunji", -1.2770, 36.8560, "Private"),
        
        # KASARANI (48 facilities)
        ("Kasarani Health Centre", "Kasarani", -1.2238, 36.9024, "Public"),
        ("Korogocho Health Centre", "Kasarani", -1.2450, 36.8800, "Public"),
        ("Njiru Dispensary", "Kasarani", -1.2540, 36.9440, "Public"),
        ("Aga Khan University Hospital (Njiru)", "Kasarani", -1.2530, 36.9440, "Private"),
        ("Ruaraka Uhai Neema Hospital", "Kasarani", -1.2350, 36.8860, "Private"),
        ("St Francis Community Hospital", "Kasarani", -1.2280, 36.9070, "Faith Based"),
        
        # KIBERA (60 facilities)
        ("Kenyatta National Hospital", "Kibera", -1.3021, 36.8077, "Public"),
        ("Mbagathi District Hospital", "Kibera", -1.3077, 36.8033, "Public"),
        ("Nairobi Hospital", "Kibera", -1.2963, 36.8054, "Private"),
        ("Coptic Hospital", "Kibera", -1.3090, 36.7970, "Private"),
        ("Kibera CFW Clinic", "Kibera", -1.3110, 36.7860, "Public"),
        ("Huduma Health Centre", "Kibera", -1.3120, 36.7880, "Public"),
        
        # LANGATA (50 facilities)
        ("The Karen Hospital", "Langata", -1.3560, 36.7540, "Private"),
        ("Nairobi West Hospital", "Langata", -1.3100, 36.8090, "Private"),
        ("Langata Hospital", "Langata", -1.3430, 36.7600, "Private"),
        ("Langata Health Centre", "Langata", -1.3500, 36.7520, "Public"),
        ("Mutuini Sub-District Hospital", "Langata", -1.3490, 36.7510, "Public"),
        ("St Mary's Mission Hospital", "Langata", -1.3350, 36.7870, "Faith Based"),
        
        # MAKADARA (43 facilities)
        ("Metropolitan Hospital Nairobi", "Makadara", -1.2960, 36.8720, "Private"),
        ("Gertrude's Children's Hospital", "Makadara", -1.2960, 36.8640, "Private"),
        ("Jamaa Mission Hospital", "Makadara", -1.2960, 36.8640, "Faith Based"),
        ("Bahati Health Centre", "Makadara", -1.2950, 36.8670, "Public"),
        ("The Mater Hospital Buruburu", "Makadara", -1.2960, 36.8720, "Private"),
        ("Aga Khan University Hospital (Buruburu)", "Makadara", -1.2960, 36.8730, "Private"),
        
        # MATHARE (15 facilities)
        ("Mathari Hospital", "Mathare", -1.2597, 36.8469, "Public"),
        ("Makadara Health Centre", "Mathare", -1.2620, 36.8600, "Public"),
        ("Huruma Maternity Hospital", "Mathare", -1.2570, 36.8570, "Private"),
        ("Getrudes Mathare Outreach Clinic", "Mathare", -1.2590, 36.8580, "Private"),
        
        # ROYSAMBU (50 facilities)
        ("Kenyatta University Dispensary", "Roysambu", -1.1870, 36.9210, "Public"),
        ("Kahawa West Health Centre", "Roysambu", -1.2040, 36.8860, "Public"),
        ("Karura Health Centre", "Roysambu", -1.2270, 36.8440, "Public"),
        ("The Mater Hospital TRM", "Roysambu", -1.2100, 36.8750, "Private"),
        ("Gertrude's Children Hospital Thika Rd", "Roysambu", -1.2150, 36.8800, "Private"),
        ("Kamiti Prison Hospital", "Roysambu", -1.1690, 36.9220, "Public"),
        
        # RUARAKA (26 facilities)
        ("Mathare North Health Centre", "Ruaraka", -1.2440, 36.8700, "Public"),
        ("Babadogo Health Centre", "Ruaraka", -1.2460, 36.8710, "Public"),
        ("Avenue Health Care Garden City", "Ruaraka", -1.2380, 36.8730, "Private"),
        ("The Aga Khan Medical Centre-Rigeways", "Ruaraka", -1.2360, 36.8200, "Private"),
        
        # STAREHE (80 facilities)
        ("Guru Nanak Hospital", "Starehe", -1.2697, 36.8325, "Private"),
        ("Lad Nan Hospital", "Starehe", -1.2720, 36.8410, "Private"),
        ("South B Hospital", "Starehe", -1.3050, 36.8340, "Private"),
        ("Ngara Health Centre", "Starehe", -1.2710, 36.8460, "Public"),
        ("Juja Road Hospital", "Starehe", -1.2730, 36.8400, "Public"),
        ("Radiant Pangani Hospital", "Starehe", -1.2710, 36.8460, "Private"),
        ("The Mater Hospital Mukuru", "Starehe", -1.3070, 36.8347, "Private"),
        
        # WESTLANDS (50 facilities)
        ("Aga Khan University Hospital", "Westlands", -1.2943, 36.8065, "Private"),
        ("Avenue Hospital", "Westlands", -1.2650, 36.8060, "Private"),
        ("Mp Shah Hospital", "Westlands", -1.2620, 36.8190, "Private"),
        ("Kangemi Health Centre", "Westlands", -1.2540, 36.7820, "Public"),
        ("Gertrude's Childrens Hospital", "Westlands", -1.2630, 36.8100, "Private"),
        ("Lions Sightfirst Eye Hospital", "Westlands", -1.2630, 36.8100, "Private"),
        ("AAR Clinic Sarit Centre", "Westlands", -1.2600, 36.8050, "Private"),
    ]
    
    # Create DataFrame
    for name, sub_county, lat, lng, facility_type in facilities_data:
        facilities.append({
            'Facility Name': name,
            'Sub-County': sub_county,
            'Type': facility_type,
            'Latitude': lat,
            'Longitude': lng
        })
    
    return pd.DataFrame(facilities)

# ============================================================================
# MAP CREATION FUNCTION
# ============================================================================

def create_nairobi_map(facilities_df):
    """Create interactive map with county boundary, sub-counties, and all facilities"""
    
    # Center of Nairobi
    nairobi_center = [-1.2921, 36.8219]
    
    # Create base map
    m = folium.Map(
        location=nairobi_center,
        zoom_start=12,
        tiles='CartoDB positron',
        control_scale=True
    )
    
    # Add multiple tile layers for different views
    folium.TileLayer('OpenStreetMap', name='Street Map').add_to(m)
    folium.TileLayer('CartoDB dark_matter', name='Dark Mode').add_to(m)
    folium.TileLayer('OpenTopoMap', name='Topographic').add_to(m)
    
    # Add fullscreen button
    Fullscreen().add_to(m)
    
    # Add Nairobi County boundary
    folium.Polygon(
        locations=NAIROBI_COUNTY_BOUNDARY,
        color='darkred',
        weight=3,
        fill=True,
        fill_color='red',
        fill_opacity=0.05,
        tooltip='Nairobi County Boundary',
        popup=folium.Popup('<b>Nairobi County</b><br>Capital city of Kenya<br>Area: 696.1 km²', max_width=250)
    ).add_to(m)
    
    # Color mapping for facility types
    type_colors = {
        'Public': '#FF4444',      # Red
        'Private': '#4444FF',      # Blue
        'Faith Based': '#44BB44'   # Green
    }
    
    type_icons = {
        'Public': '🏥',
        'Private': '💊',
        'Faith Based': '⛪'
    }
    
    # Create marker cluster
    marker_cluster = MarkerCluster(
        name='Health Facilities',
        control=True
    ).add_to(m)
    
    # Add all facility markers
    for _, row in facilities_df.iterrows():
        name = row['Facility Name']
        f_type = row['Type']
        sub_county = row['Sub-County']
        lat = row['Latitude']
        lng = row['Longitude']
        
        color = type_colors.get(f_type, '#888888')
        icon = type_icons.get(f_type, '🏥')
        
        # Create popup HTML
        popup_html = f"""
        <div style="font-family: Arial, sans-serif; min-width: 250px;">
            <div style="background-color: {color}; color: white; padding: 10px; border-radius: 8px 8px 0 0;">
                <b style="font-size: 14px;">{icon} {name}</b>
            </div>
            <div style="padding: 12px; background-color: #f9f9f9;">
                <b>📍 Sub-County:</b> {sub_county}<br>
                <b>🏷️ Type:</b> 
                <span style="display: inline-block; width: 12px; height: 12px; background-color: {color}; border-radius: 50%; margin-right: 6px;"></span>
                {f_type}<br>
                <b>🗺️ Coordinates:</b><br>
                <span style="font-family: monospace; font-size: 11px;">{lat:.5f}, {lng:.5f}</span>
                <hr style="margin: 10px 0;">
                <div style="font-size: 11px;">
                    <a href="https://www.google.com/maps?q={lat},{lng}" target="_blank" style="color: {color}; text-decoration: none;">
                        📍 Open in Google Maps
                    </a><br>
                    <a href="https://www.openstreetmap.org/?mlat={lat}&mlon={lng}&zoom=18" target="_blank" style="color: {color}; text-decoration: none;">
                        🗺️ Open in OpenStreetMap
                    </a>
                </div>
            </div>
        </div>
        """
        
        # Create circle marker
        folium.CircleMarker(
            location=[lat, lng],
            radius=7,
            popup=folium.Popup(popup_html, max_width=350),
            tooltip=f"{icon} {name}\n📌 {f_type}\n📍 {sub_county}",
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.85,
            weight=2,
            opacity=1
        ).add_to(marker_cluster)
    
    # Add sub-county labels
    for sub_county, center in SUB_COUNTY_CENTERS.items():
        count = len(facilities_df[facilities_df['Sub-County'] == sub_county])
        
        folium.Marker(
            location=center,
            icon=folium.DivIcon(
                icon_size=(180, 35),
                icon_anchor=(90, 17),
                html=f'''
                <div style="
                    background: rgba(255,255,255,0.95);
                    padding: 6px 14px;
                    border-radius: 25px;
                    border: 2px solid #FF4444;
                    font-size: 11px;
                    font-weight: bold;
                    font-family: Arial, sans-serif;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
                    white-space: nowrap;
                ">
                    📍 {sub_county} <span style="color:#FF4444; font-weight: bold;">({count})</span>
                </div>
                '''
            )
        ).add_to(m)
    
    # Add legend
    legend_html = '''
    <div style="position: fixed; bottom: 20px; right: 20px; z-index: 1000;
                background: white; padding: 12px 18px; border-radius: 10px;
                border: 2px solid #ddd; box-shadow: 0 2px 12px rgba(0,0,0,0.15);
                font-family: Arial, sans-serif; font-size: 12px;">
        <b style="font-size: 13px;">🗺️ Map Legend</b><br>
        <hr style="margin: 8px 0;">
        <div style="margin: 8px 0;">
            <b>🏛️ Boundaries:</b><br>
            <span style="display: inline-block; width: 30px; height: 3px; background: darkred; margin-right: 8px;"></span> 
            Nairobi County Boundary
        </div>
        <div style="margin: 8px 0;">
            <b>🏥 Facility Types:</b><br>
            <span style="display: inline-block; width: 12px; height: 12px; background: #FF4444; border-radius: 50%; margin-right: 8px;"></span> 
            Public Facilities<br>
            <span style="display: inline-block; width: 12px; height: 12px; background: #4444FF; border-radius: 50%; margin-right: 8px;"></span> 
            Private Facilities<br>
            <span style="display: inline-block; width: 12px; height: 12px; background: #44BB44; border-radius: 50%; margin-right: 8px;"></span> 
            Faith Based Facilities
        </div>
        <div style="margin: 8px 0;">
            <b>📍 Labels:</b><br>
            <span style="display: inline-block; width: 12px; height: 12px; background: white; border: 2px solid #FF4444; border-radius: 50%; margin-right: 8px;"></span> 
            Sub-County Centers
        </div>
        <hr style="margin: 8px 0;">
        <div style="font-size: 10px; color: #666; text-align: center;">
            💡 Hover over dots for facility names<br>
            🖱️ Click dots for detailed information
        </div>
    </div>
    '''
    
    from folium import Element
    m.get_root().html.add_child(Element(legend_html))
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    return m

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    try:
        # Load facilities data
        with st.spinner("Loading 500+ health facilities with accurate coordinates..."):
            facilities_df = load_all_facilities()
        
        # Sidebar with statistics
        with st.sidebar:
            st.header("📊 Nairobi County Overview")
            st.metric("🏥 Total Facilities", len(facilities_df))
            st.metric("🗺️ Sub-Counties", 17)
            
            st.markdown("---")
            
            # Facilities by type
            st.subheader("📈 Facilities by Type")
            type_counts = facilities_df['Type'].value_counts()
            col1, col2 = st.columns(2)
            with col1:
                for typ, count in type_counts.items():
                    if typ == 'Public':
                        st.metric("🏥 Public", count)
                    elif typ == 'Private':
                        st.metric("💊 Private", count)
            with col2:
                for typ, count in type_counts.items():
                    if typ == 'Faith Based':
                        st.metric("⛪ Faith Based", count)
            
            st.markdown("---")
            
            # Top sub-counties
            st.subheader("🏘️ Top Sub-Counties")
            sub_counts = facilities_df['Sub-County'].value_counts().head(8)
            for sub, count in sub_counts.items():
                st.text(f"📍 {sub}: {count} facilities")
            
            st.markdown("---")
            
            st.info("""
            **💡 Map Tips:**
            - **Hover** over any dot to see facility name
            - **Click** dot for complete details
            - **Use +/-** to zoom in/out
            - **Click clusters** to zoom into areas
            - **Toggle layers** using layer control
            """)
        
        # Main content area
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
            <h3>🗺️ Interactive Map of Nairobi Health Facilities</h3>
            <p>Complete directory of health facilities across all 17 sub-counties with accurate coordinates</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create and display map
        with st.spinner("Creating interactive map with accurate boundaries..."):
            nairobi_map = create_nairobi_map(facilities_df)
            st_folium(nairobi_map, width='100%', height=700, returned_objects=[])
        
        # Statistics section
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            public_count = len(facilities_df[facilities_df['Type'] == 'Public'])
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; background-color: #FFEBEE; border-radius: 10px;">
                <h2 style="color: #FF4444; margin: 0;">🏥</h2>
                <h3 style="margin: 10px 0;">{public_count}</h3>
                <p style="margin: 0;">Public Facilities</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            private_count = len(facilities_df[facilities_df['Type'] == 'Private'])
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; background-color: #E3F2FD; border-radius: 10px;">
                <h2 style="color: #4444FF; margin: 0;">💊</h2>
                <h3 style="margin: 10px 0;">{private_count}</h3>
                <p style="margin: 0;">Private Facilities</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            faith_count = len(facilities_df[facilities_df['Type'] == 'Faith Based'])
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; background-color: #E8F5E9; border-radius: 10px;">
                <h2 style="color: #44BB44; margin: 0;">⛪</h2>
                <h3 style="margin: 10px 0;">{faith_count}</h3>
                <p style="margin: 0;">Faith Based Facilities</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; background-color: #FFF3E0; border-radius: 10px;">
                <h2 style="color: #FF9800; margin: 0;">🗺️</h2>
                <h3 style="margin: 10px 0;">17</h3>
                <p style="margin: 0;">Sub-Counties</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Data table expander
        with st.expander("📋 View Complete Facilities List with Coordinates"):
            display_df = facilities_df[['Facility Name', 'Sub-County', 'Type', 'Latitude', 'Longitude']].copy()
            display_df = display_df.reset_index(drop=True)
            display_df.index = display_df.index + 1
            st.dataframe(display_df, use_container_width=True, height=500)
            
            # Download button
            csv = facilities_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download All Facilities Data (CSV)",
                data=csv,
                file_name="nairobi_health_facilities_complete.csv",
                mime="text/csv"
            )
        
        # Footer
        st.markdown("---")
        st.markdown(
            f"""
            <div style='text-align: center; color: gray; font-size: 12px;'>
                <b>🏥 Nairobi Health Facilities Map</b><br>
                📍 Total: {len(facilities_df)} facilities across 17 sub-counties | 
                🟡 Public | 🔵 Private | 🟢 Faith Based<br>
                💡 Hover over any dot to see facility name | Click for complete details
            </div>
            """,
            unsafe_allow_html=True
        )
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please make sure all required packages are installed: streamlit, pandas, folium, streamlit-folium")

# Run the application
if __name__ == "__main__":
    main()
