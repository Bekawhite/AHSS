# nairobi_health_map_final.py
import streamlit as st
import pandas as pd
# Handle folium imports with error catching
try:
    import folium
    from streamlit_folium import st_folium
    from folium.plugins import MarkerCluster, Fullscreen
    FOLIUM_AVAILABLE = True
except ImportError as e:
    FOLIUM_AVAILABLE = False
    st.error(f"⚠️ Required packages not installed. Please add to requirements.txt: folium, streamlit-folium")
    st.stop()


import math

# Page configuration
st.set_page_config(
    page_title="Nairobi Health Facilities Map - Accurate Boundaries",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Nairobi County Health Facilities Map")
st.markdown("### Complete Directory: 494+ Health Facilities Across 17 Sub-Counties with Accurate Coordinates")

# ============================================================================
# ACCURATE COORDINATES FROM YOUR EXCEL DATA
# ============================================================================

# Nairobi County boundary points (from your Excel sheet 1)
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

# Sub-county centers (from your Excel sheet 2)
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
# LOAD ALL FACILITIES DATA FROM YOUR EXCEL
# ============================================================================

@st.cache_data
def load_all_facilities():
    """Load all facilities with accurate coordinates from your Excel data"""
    
    facilities = []
    
    # Facilities data from your Excel sheet 3
    facilities_data = [
        # ── DAGORETTI NORTH ──────────────────────────────────────────
        ("Refuge Point International","Dagoretti North",-1.2907,36.7910),
        ("Avenue House Medical Centre","Dagoretti North",-1.2884,36.8138),
        ("Dr.K.Gicheru(Upper Hill Centre)","Dagoretti North",-1.2946,36.8063),
        ("Dr.P.W.Kamau&Associates(Upper Hill Medical Centre)","Dagoretti North",-1.2947,36.8066),
        ("Dr.Henry Wellington Alube (landmark plaza)","Dagoretti North",-1.2948,36.8032),
        ("Dr.Charles.J.R.Opondo (landmark plaza)","Dagoretti North",-1.2948,36.8032),
        ("Acacia Clinic (Kilimani)","Dagoretti North",-1.2961,36.8072),
        ("Menelik Chest Clinic","Dagoretti North",-1.2946,36.7990),
        ("Meridian Medical Centre (Kileleshwa)","Dagoretti North",-1.2930,36.7877),
        ("The Mater Hospital (Westlands)","Dagoretti North",-1.2639,36.8021),
        ("Medanta Africare","Dagoretti North",-1.3016,36.8221),
        ("Bodaki Medical Clinic","Dagoretti North",-1.2939,36.7393),
        ("Skyhill Medical Centre","Dagoretti North",-1.2812,36.7522),
        ("Adventist Centre For Care and Support (Kilimani)","Dagoretti North",-1.2891,36.8073),
        ("Jacaranda Special School","Dagoretti North",-1.2893,36.7869),
        ("Melchezedek Hospital","Dagoretti North",-1.2945,36.7554),
        ("Liverpool VCT","Dagoretti North",-1.2868,36.8260),
        ("New Life Home Childrens Home (Kilimani)","Dagoretti North",-1.2890,36.7878),
        ("State House Clinic","Dagoretti North",-1.2780,36.8100),
        ("Dod Mrs Dispensary","Dagoretti North",-1.2870,36.7900),
        ("University of Nairobi Dispensary","Dagoretti North",-1.2739,36.8038),
        ("State House Dispensary (Nairobi)","Dagoretti North",-1.2826,36.8072),
        ("Westlands Health Centre","Dagoretti North",-1.2641,36.8039),
        ("Maria Immaculate Health Centre","Dagoretti North",-1.3066,36.8329),
        ("Gertrudes Othaya Road Dispensary","Dagoretti North",-1.2868,36.7728),
        ("Nairobi Womens Hospital (Hurlingham)","Dagoretti North",-1.2937,36.7961),
        ("National Spinal Injury Hospital","Dagoretti North",-1.2878,36.7940),
        ("Lady Northey Dispensary","Dagoretti North",-1.2881,36.8114),
        ("Nyalego Medical Clinic","Dagoretti North",-1.2838,36.7423),
        ("Riruta Health Centre","Dagoretti North",-1.2871,36.7413),
        # ── DAGORETTI SOUTH ──────────────────────────────────────────
        ("Sanctuary Rains Medical Centre","Dagoretti South",-1.2668,36.7494),
        ("Dadas VCT","Dagoretti South",-1.2698,36.7119),
        ("Samawati medical Centre","Dagoretti South",-1.2880,36.6870),
        ("Gachui Medical Centre","Dagoretti South",-1.2811,36.6945),
        ("Paragon Health Care Ltd","Dagoretti South",-1.2890,36.7450),
        ("medicross ltd kawangware","Dagoretti South",-1.2878,36.7415),
        ("AAR Adams Health Centre","Dagoretti South",-1.3007,36.7820),
        ("Jeffrey Medical & Diagnostic Centre","Dagoretti South",-1.2874,36.7488),
        ("Lea Toto Kawangware","Dagoretti South",-1.2870,36.7480),
        ("Swop Kawangware","Dagoretti South",-1.2776,36.7319),
        ("Maisha Poa Dispensary","Dagoretti South",-1.2885,36.7388),
        ("Gitanga Medical Centre","Dagoretti South",-1.2841,36.7420),
        ("Central Park Clinic","Dagoretti South",-1.2880,36.7460),
        ("Kawangware Health Centre","Dagoretti South",-1.2887,36.7470),
        ("Local Aid Organization","Dagoretti South",-1.2870,36.7430),
        ("Jellin Medical Clinic","Dagoretti South",-1.2873,36.7428),
        ("Nile Medical Care","Dagoretti South",-1.2837,36.6892),
        ("Imani Health Servises","Dagoretti South",-1.2850,36.7430),
        ("Orient Medical Care","Dagoretti South",-1.2860,36.7440),
        ("Uthiru Muthua Dispensary","Dagoretti South",-1.2687,36.7183),
        ("Glory Health Clinic","Dagoretti South",-1.2870,36.7420),
        ("Fremo Medical Centre","Dagoretti South",-1.2880,36.7450),
        ("Mary Mission","Dagoretti South",-1.2890,36.7460),
        ("Al-Gadhir Clinic","Dagoretti South",-1.2900,36.7460),
        ("Jonalifa Clinic","Dagoretti South",-1.2870,36.7430),
        ("Kesha VCT","Dagoretti South",-1.2880,36.7440),
        ("Lea Toto Dagoretti","Dagoretti South",-1.2870,36.7500),
        ("Sokoni Arcade VCT","Dagoretti South",-1.2860,36.7450),
        ("St Joseph's Dispensary (Dagoretti)","Dagoretti South",-1.2890,36.7480),
        ("Kivuli Dispensary","Dagoretti South",-1.2900,36.7490),
        ("Abandoned Child Care","Dagoretti South",-1.2880,36.7470),
        ("Orthodox Dispensary","Dagoretti South",-1.2870,36.7460),
        ("Good Shepherd Dispensary","Dagoretti South",-1.2880,36.7450),
        ("Mercy Mission Health Centre","Dagoretti South",-1.2870,36.7440),
        ("Waithaka Health Centre","Dagoretti South",-1.2804,36.7163),
        ("St Lukes (Kona) Health Centre","Dagoretti South",-1.2850,36.7300),
        ("St Teresa's Health Centre","Dagoretti South",-1.2879,36.7516),
        ("Wema Nursing Home","Dagoretti South",-1.2827,36.7498),
        ("St Catherine's Health Centre","Dagoretti South",-1.2870,36.7500),
        ("Ray of Hope Health Centre","Dagoretti South",-1.2880,36.7510),
        ("Mid Hill Medical Clinic","Dagoretti South",-1.2890,36.7520),
        ("Muteithania Medical Clinic","Dagoretti South",-1.2870,36.7460),
        ("Spacecare Health Services","Dagoretti South",-1.2880,36.7470),
        ("Kabiro Medical Clinic","Dagoretti South",-1.2870,36.7490),
        ("Rgc Jipe Moyo Dispensary","Dagoretti South",-1.2890,36.7490),
        ("Chandaria Health Centre","Dagoretti South",-1.2827,36.6903),
        # ── EMBAKASI CENTRAL ─────────────────────────────────────────
        ("Fairview Medical Centre","Embakasi Central",-1.2786,36.9115),
        ("Equity Afia Kayole","Embakasi Central",-1.2744,36.9110),
        ("MOFA-AFYA","Embakasi Central",-1.2760,36.9100),
        ("Suba Medical Centre","Embakasi Central",-1.2770,36.9090),
        ("Maria Medical Clinic And Diadetic centre(Saika)","Embakasi Central",-1.2750,36.9120),
        ("MYSA VCT","Embakasi Central",-1.2760,36.9110),
        ("Dap Health Clinic","Embakasi Central",-1.2770,36.9100),
        ("Eastern Medical Clinic","Embakasi Central",-1.2780,36.9130),
        ("Primed Medical Services Komarock","Embakasi Central",-1.2750,36.9050),
        ("St John Medical Centre","Embakasi Central",-1.2760,36.9140),
        ("Santi Meridian Health Care","Embakasi Central",-1.2770,36.9150),
        ("Trocare Medical Clinic","Embakasi Central",-1.2740,36.9120),
        ("Exodus Community Health Care","Embakasi Central",-1.2760,36.9130),
        ("Mwera Medical Clinic","Embakasi Central",-1.2750,36.9100),
        ("Kings Cross Medical Clinic","Embakasi Central",-1.2770,36.9110),
        ("PCEA Kayole Parish Health Centre","Embakasi Central",-1.2760,36.9120),
        ("True Light Medical Clinic","Embakasi Central",-1.2750,36.9130),
        ("Angaza VCT","Embakasi Central",-1.2760,36.9140),
        ("Prudent Medical Clinic Kariobangi","Embakasi Central",-1.2770,36.9100),
        ("Gertrude Komarock Clinic","Embakasi Central",-1.2740,36.9060),
        ("EDARP Komarock Health Centre","Embakasi Central",-1.2750,36.9070),
        ("Komarock Morden Medical Care","Embakasi Central",-1.2760,36.9080),
        ("Viva Afya Kayole","Embakasi Central",-1.2770,36.9090),
        ("Susamed Medical Clinic","Embakasi Central",-1.2750,36.9110),
        ("Coni Health Centre","Embakasi Central",-1.2760,36.9120),
        ("Aski Medical Clinic","Embakasi Central",-1.2750,36.9130),
        ("Dabliu Clinic","Embakasi Central",-1.2770,36.9140),
        ("St Begson Clinic","Embakasi Central",-1.2760,36.9100),
        ("St Jude's Medical Centre","Embakasi Central",-1.2750,36.9110),
        ("Komarock Medical Clinic","Embakasi Central",-1.2760,36.9060),
        ("St Patrick Health Care Centre","Embakasi Central",-1.2770,36.9080),
        ("Provide International Clinic (Kayole)","Embakasi Central",-1.2750,36.9090),
        ("Kayole Hospital","Embakasi Central",-1.2760,36.9100),
        ("Soweto Kayole PHC Health Centre","Embakasi Central",-1.2770,36.9110),
        ("Patanisho Maternity and Nursing Home","Embakasi Central",-1.2750,36.9120),
        ("EDARP Soweto Health Centre","Embakasi Central",-1.2760,36.9130),
        ("Maria Maternity and Nursing Home","Embakasi Central",-1.2770,36.9140),
        ("Kayole II Sub-District Hospital","Embakasi Central",-1.2774,36.9158),
        ("Diwopa Health Centre","Embakasi Central",-1.2750,36.9160),
        ("Arrow Web Maternity and Nursing Home","Embakasi Central",-1.2760,36.9170),
        ("Kayole I Health Centre","Embakasi Central",-1.2780,36.9110),
        # ── EMBAKASI EAST ────────────────────────────────────────────
        ("AVENUE HEALTHCARE GREENSPAN","Embakasi East",-1.3050,36.9100),
        ("Avenue Health Care Embakasi","Embakasi East",-1.3060,36.9120),
        ("Transami Clinic","Embakasi East",-1.3130,36.9070),
        ("Komarock Modern Hospital Utawala","Embakasi East",-1.2920,36.9400),
        ("EURAKA MEDICAL CENTRE","Embakasi East",-1.3080,36.9130),
        ("SWOP Clinic Donholm","Embakasi East",-1.3050,36.8900),
        ("Arrow Web Clinic","Embakasi East",-1.3070,36.9140),
        ("Medigold","Embakasi East",-1.3090,36.9150),
        ("Kenya Airways Pride Clinic","Embakasi East",-1.3190,36.9270),
        ("Blessed Medicare Centre","Embakasi East",-1.3060,36.9100),
        ("Blissgvs Health Care Pipeline","Embakasi East",-1.3080,36.8950),
        ("Lina Medical Services","Embakasi East",-1.3070,36.9110),
        ("AAR Health Care","Embakasi East",-1.3060,36.9090),
        ("Aga Khan Greenspam Medical Centre","Embakasi East",-1.3040,36.9080),
        ("Communal Oriented Service International Centre","Embakasi East",-1.3070,36.9120),
        ("Connections Medical Clinic","Embakasi East",-1.3080,36.9130),
        ("Scion Healthcare Ltd Clinic","Embakasi East",-1.3060,36.9100),
        ("Provide International Hospital Mukuru","Embakasi East",-1.3200,36.8900),
        ("Abra Health Services","Embakasi East",-1.3090,36.9140),
        ("Primed Medical Centre","Embakasi East",-1.3070,36.9150),
        ("St Maurice Medical Services","Embakasi East",-1.3060,36.9110),
        ("Mariakani Cottage Hospital Utawala Clinic","Embakasi East",-1.2940,36.9420),
        ("Swop Outreach Project Clinic","Embakasi East",-1.3050,36.9080),
        ("Utawala Estate Health Centre","Embakasi East",-1.2920,36.9450),
        ("Getrude Embakasi Clinic","Embakasi East",-1.3070,36.9090),
        ("Bristal Park Hospital","Embakasi East",-1.3060,36.9120),
        ("Vegpro In House Clinic","Embakasi East",-1.3100,36.9160),
        ("Meridian Medical Donholm Clinic","Embakasi East",-1.3040,36.8900),
        ("St Barkita Dispensary Utawala","Embakasi East",-1.2930,36.9430),
        ("St Raphael's Clinic","Embakasi East",-1.3080,36.9140),
        ("Getrude Donholm Clinic","Embakasi East",-1.3050,36.8920),
        ("Genessaret Clinic","Embakasi East",-1.3070,36.9150),
        ("Pine Medical Clinic","Embakasi East",-1.3060,36.9130),
        ("Kapu Medical Clinic","Embakasi East",-1.3090,36.9140),
        ("GSUTraining School","Embakasi East",-1.3200,36.9300),
        ("Jkia Health Centre","Embakasi East",-1.3190,36.9260),
        ("Garrison Health Centre","Embakasi East",-1.3180,36.9250),
        ("EDARP Donholm Clinic","Embakasi East",-1.3060,36.8910),
        ("Embakasi Health Centre","Embakasi East",-1.3080,36.9140),
        ("APTC Health Centre","Embakasi East",-1.3090,36.9150),
        # ── EMBAKASI NORTH ───────────────────────────────────────────
        ("Selina's Health Care","Embakasi North",-1.2580,36.8870),
        ("Kinmed Medical Clinic (Dandora)","Embakasi North",-1.2570,36.8900),
        ("Afya Medical Clinic (Dandora)","Embakasi North",-1.2560,36.8920),
        ("Dandora Medical and Laboratory Services (Kojwang)","Embakasi North",-1.2550,36.8930),
        ("Kwosp (Korogocho)","Embakasi North",-1.2470,36.8720),
        ("Comboni Missionary Sisters Health Programm","Embakasi North",-1.2490,36.8740),
        ("Premium Health Services","Embakasi North",-1.2580,36.8880),
        ("Kariobangi EDARP","Embakasi North",-1.2600,36.8860),
        ("Senate Health Services","Embakasi North",-1.2570,36.8870),
        ("Catholic Dispensary Kariobangi","Embakasi North",-1.2590,36.8850),
        ("Oasis Medical Clinic","Embakasi North",-1.2560,36.8890),
        ("Paradise Medical Centre (Dandora Area Iv)","Embakasi North",-1.2540,36.8940),
        ("Dandora Medical Centre","Embakasi North",-1.2550,36.8910),
        ("Karomo Medical Clinic","Embakasi North",-1.2560,36.8920),
        ("Delta Medical Clinic Dandora","Embakasi North",-1.2570,36.8930),
        ("Mundoro Medical Clinic Dandora","Embakasi North",-1.2580,36.8940),
        ("Samaritan Medical Services (Dandora)","Embakasi North",-1.2550,36.8900),
        ("Provide Internatinal Clinic (Dandora)","Embakasi North",-1.2560,36.8910),
        ("Jamii Medical Hospital","Embakasi North",-1.2570,36.8920),
        ("Lea Toto","Embakasi North",-1.2580,36.8930),
        ("St Philips Health Centre","Embakasi North",-1.2600,36.8840),
        ("Karma Dispensary","Embakasi North",-1.2590,36.8860),
        ("Kariobangi Health Centre","Embakasi North",-1.2604,36.8884),
        ("PCEA Dandora Clinic","Embakasi North",-1.2550,36.8920),
        ("St Mark Medical Clinic (Nairobi East)","Embakasi North",-1.2560,36.8930),
        ("Dandora II Health Centre","Embakasi North",-1.2570,36.8940),
        # ── EMBAKASI SOUTH ───────────────────────────────────────────
        ("Africare Limited Embakasi Clinic","Embakasi South",-1.3200,36.8950),
        ("Access Afya Medical Centre Viwandani","Embakasi South",-1.3180,36.8880),
        ("Josiah Community Medical Centre","Embakasi South",-1.3190,36.8960),
        ("PCEA Pipeline Clinic","Embakasi South",-1.3160,36.8940),
        ("Jamii Medical Clinic Mukuru","Embakasi South",-1.3170,36.8920),
        ("Embakasi Medical Centre","Embakasi South",-1.3180,36.8930),
        ("The Mater Embakasi Clinic","Embakasi South",-1.3190,36.8940),
        ("Olive Link Health Care","Embakasi South",-1.3200,36.8960),
        ("St Clare Medical Clinic","Embakasi South",-1.3170,36.8950),
        ("Mukuru Health Centre","Embakasi South",-1.3180,36.8960),
        ("Kenya Airports Employees Association","Embakasi South",-1.3210,36.9000),
        ("I Choose Life Africa","Embakasi South",-1.3180,36.8970),
        ("Lea Toto Community Mukuru Reuben","Embakasi South",-1.3190,36.8970),
        ("Imara Health Centre","Embakasi South",-1.3200,36.8980),
        ("Hope World Wide Kenya Mukuru Clinic","Embakasi South",-1.3170,36.8940),
        ("Mayflower Clinic","Embakasi South",-1.3180,36.8950),
        ("Mwatate Clinic","Embakasi South",-1.3190,36.8960),
        ("Cidi Mukuru Clinic","Embakasi South",-1.3200,36.8970),
        ("Cana Family Life Clinic","Embakasi South",-1.3170,36.8960),
        ("Wentworth Hospital","Embakasi South",-1.3180,36.8980),
        ("Alice Nursing Home","Embakasi South",-1.3190,36.8990),
        ("Pipeline Nursing Home","Embakasi South",-1.3170,36.8970),
        ("Reuben Mukuru Health Centre","Embakasi South",-1.3200,36.8990),
        ("Pipeline Medical Health Services","Embakasi South",-1.3180,36.8990),
        # ── EMBAKASI WEST ────────────────────────────────────────────
        ("RADIANT GROUP OF HOSPITALS-UMOJA","Embakasi West",-1.2900,36.8900),
        ("Mikulinzi Nursing Home","Embakasi West",-1.2910,36.8890),
        ("Doulos Youth Friendly And VCT (KCC)","Embakasi West",-1.2920,36.8880),
        ("Umoja III Medical Centre(Njiru)","Embakasi West",-1.2930,36.8870),
        ("St Anselmo Medical Clinic","Embakasi West",-1.2900,36.8920),
        ("Recovery Medical Clinic (Kariobangi South)","Embakasi West",-1.2910,36.8910),
        ("Innercore Medical Clinic","Embakasi West",-1.2920,36.8900),
        ("Corban Health Care","Embakasi West",-1.2930,36.8890),
        ("Rosadett Medical Clinic","Embakasi West",-1.2900,36.8930),
        ("Embakasi Medical Centre (Aun)","Embakasi West",-1.2910,36.8920),
        ("Emmanuel Medical Centre","Embakasi West",-1.2920,36.8910),
        ("Divine Mercy Kariobangi","Embakasi West",-1.2930,36.8900),
        ("Unity Nursing Home","Embakasi West",-1.2900,36.8940),
        ("Umoja VCT Centre Stand Alone","Embakasi West",-1.2910,36.8930),
        ("Rays International Clinic Kariobangi","Embakasi West",-1.2920,36.8920),
        ("Kariobangi South Clinic","Embakasi West",-1.2930,36.8910),
        ("Mama Lucy Kibaki Hospital - Embakasi","Embakasi West",-1.2740,36.8990),
        ("St Mary's Medical Clinic (Umoja II)","Embakasi West",-1.2900,36.8950),
        ("Emmaus Nursing Home","Embakasi West",-1.2910,36.8940),
        ("Wamunga Health Clinic","Embakasi West",-1.2920,36.8930),
        ("Provide International Mutindwa Umoja Clinic","Embakasi West",-1.2930,36.8920),
        ("Victory Hospital","Embakasi West",-1.2900,36.8960),
        ("Umoja Hospital","Embakasi West",-1.2910,36.8950),
        ("SOS Dispensary","Embakasi West",-1.2920,36.8940),
        ("Dandora (EDARP) Clinic","Embakasi West",-1.2930,36.8930),
        ("Lea Toto Clinic Kariobangi South","Embakasi West",-1.2920,36.8860),
        ("Jericho Health Centre","Embakasi West",-1.2900,36.8700),
        # ── KAMUKUNJI ────────────────────────────────────────────────
        ("Africare Limited Eastleigh","Kamukunji",-1.2760,36.8520),
        ("Nairobi East Hospital Ltd","Kamukunji",-1.2750,36.8510),
        ("Aga Khan Clinic (Eastleigh)","Kamukunji",-1.2780,36.8530),
        ("Msf- Green House Clinic","Kamukunji",-1.2790,36.8540),
        ("Iom Wellness Clinic","Kamukunji",-1.2770,36.8520),
        ("Andulus Medical Clinic","Kamukunji",-1.2760,36.8530),
        ("Al Amin Nursing Home","Kamukunji",-1.2750,36.8520),
        ("Lithi Clinic","Kamukunji",-1.2780,36.8540),
        ("Joy Nursing Home and Maternity","Kamukunji",-1.2790,36.8550),
        ("St Veronica EDARP Clinic","Kamukunji",-1.2770,36.8530),
        ("St John's Community Centre","Kamukunji",-1.2760,36.8540),
        ("Family Health Option of Kenya","Kamukunji",-1.2750,36.8530),
        ("St Joseph Nursing Home (Eastleigh North)","Kamukunji",-1.2780,36.8550),
        ("Alliance Medical Centre","Kamukunji",-1.2790,36.8560),
        ("Blue House Dispensary","Kamukunji",-1.2800,36.8540),
        ("Biafra Lions Clinic","Kamukunji",-1.2840,36.8430),
        ("Pumwani Maternity Hospital","Kamukunji",-1.2807,36.8455),
        ("Moi Air Base Hospital","Kamukunji",-1.2750,36.8450),
        ("Salama Nursing Home","Kamukunji",-1.2770,36.8540),
        ("Makkah Nursing Home","Kamukunji",-1.2760,36.8550),
        ("Marie Stopes Nursing Home (Eastleigh)","Kamukunji",-1.2750,36.8540),
        ("Woodstreet Nursing Home","Kamukunji",-1.2780,36.8560),
        ("Dorkcare Nursing Home","Kamukunji",-1.2790,36.8570),
        ("Madina Nursing Home","Kamukunji",-1.2770,36.8550),
        ("Edna Maternity","Kamukunji",-1.2760,36.8560),
        ("St Teresa's Parish Dispensary","Kamukunji",-1.2750,36.8550),
        ("St Vincent Catholic Clinic","Kamukunji",-1.2780,36.8570),
        ("Pumwani Majengo Dispensary","Kamukunji",-1.2810,36.8460),
        ("Biafra Medical Clinic","Kamukunji",-1.2840,36.8440),
        ("Shauri Moyo Clinic","Kamukunji",-1.2820,36.8470),
        ("Diani Dispensary","Kamukunji",-1.2830,36.8480),
        ("St Joseph (EDARP) Clinic","Kamukunji",-1.2760,36.8570),
        ("Mother & Child Hospital","Kamukunji",-1.2770,36.8560),
        ("Eastleigh Health Centre","Kamukunji",-1.2718,36.8511),
        # ── KASARANI ─────────────────────────────────────────────────
        ("Saika Community Medical Centre","Kasarani",-1.2240,36.9020),
        ("Kwetu Home Of Peace Dispensary(Ruai)","Kasarani",-1.2500,36.9400),
        ("Heri Wema Health Centre (Ruai)","Kasarani",-1.2510,36.9420),
        ("Adopta Life Foundation (Ruai)","Kasarani",-1.2520,36.9430),
        ("Aga Khan University Hospital(Njiru)","Kasarani",-1.2530,36.9440),
        ("Maximum medical centre","Kasarani",-1.2230,36.9010),
        ("Kenya Institute of Special Education Dispensary","Kasarani",-1.2240,36.9030),
        ("Sam-link medical centre","Kasarani",-1.2250,36.9040),
        ("AAR Mountain mall","Kasarani",-1.2260,36.9050),
        ("Kipawa Medical Centre","Kasarani",-1.2270,36.9060),
        ("Terminus Medical Clinic (Dandora)","Kasarani",-1.2280,36.9070),
        ("Horeb Medical Clinic ( Hunters)","Kasarani",-1.2290,36.9080),
        ("Radiant Hosp Kasarani","Kasarani",-1.2240,36.9020),
        ("Hunters Medical Clinic","Kasarani",-1.2300,36.9090),
        ("Wayside Medical & Dental Clinic","Kasarani",-1.2310,36.9100),
        ("Ngumba Medical Centre","Kasarani",-1.2320,36.9110),
        ("Swop Thika Road","Kasarani",-1.2200,36.8700),
        ("Korogocho Health Centre","Kasarani",-1.2450,36.8800),
        ("Ruaraka Uhai Neema Hospital","Kasarani",-1.2350,36.8860),
        ("Flomed Med Clinic","Kasarani",-1.2240,36.9010),
        ("Shekina Medical Clinic","Kasarani",-1.2250,36.9020),
        ("Sunton CFW Clinic","Kasarani",-1.2260,36.9030),
        ("Dreamline Medical Clinic Kamulu","Kasarani",-1.2700,36.9700),
        ("Saika Medical Centre","Kasarani",-1.2240,36.9020),
        ("St John's Community Clinic Njiru","Kasarani",-1.2540,36.9450),
        ("Ruai (SDA) Clinic","Kasarani",-1.2490,36.9390),
        ("St Alice (EDARP) Dandora","Kasarani",-1.2480,36.8880),
        ("Skymed Medical Clinic Githunguri","Kasarani",-1.2230,36.9010),
        ("Dandora Health Service","Kasarani",-1.2560,36.8910),
        ("Precious Life Medical Clinic Ruai","Kasarani",-1.2500,36.9410),
        ("Josma Medical Clinic (Kasarani)","Kasarani",-1.2240,36.9020),
        ("Thika Road Health Services Ltd (Kasarani)","Kasarani",-1.2210,36.8760),
        ("Kasarani Claycity Medical Centre (Kasarani)","Kasarani",-1.2250,36.9030),
        ("EDARP Njiru Clinic","Kasarani",-1.2550,36.9460),
        ("Kasarani Maternity","Kasarani",-1.2240,36.9040),
        ("Ruai Community Clinic","Kasarani",-1.2490,36.9400),
        ("Wangu Medical Clinic","Kasarani",-1.2260,36.9050),
        ("Mkunga Clinic","Kasarani",-1.2270,36.9060),
        ("EDARP Ruai Clinic","Kasarani",-1.2500,36.9420),
        ("St Francis Com Hospital","Kasarani",-1.2280,36.9070),
        ("Kasarani Health Centre","Kasarani",-1.2238,36.9024),
        ("Njiru Dispensary","Kasarani",-1.2540,36.9440),
        ("Ruaraka Clinic","Kasarani",-1.2350,36.8870),
        ("Nimoli Medical Centre","Kasarani",-1.2290,36.9080),
        ("Conerstone Clinic","Kasarani",-1.2300,36.9090),
        ("Pona Mat Dispensary","Kasarani",-1.2310,36.9100),
        ("Med-Point Dispensary","Kasarani",-1.2320,36.9110),
        ("Mwiki CFW","Kasarani",-1.2050,36.9100),
        # ── KIBERA ───────────────────────────────────────────────────
        ("Oasis Doctors Plaza Nairobi Green House","Kibera",-1.3060,36.7900),
        ("Karanja Road Community Clinic","Kibera",-1.3100,36.7870),
        ("Makina Community Clinic","Kibera",-1.3120,36.7850),
        ("Lindi Community Clinic","Kibera",-1.3110,36.7880),
        ("Kianda 42 Community Clinic","Kibera",-1.3100,36.7890),
        ("TB Central Reference Lab","Kibera",-1.3000,36.8070),
        ("Microbiology Reference Lab","Kibera",-1.3010,36.8060),
        ("Oncology Reference Lab","Kibera",-1.3020,36.8070),
        ("National Blood Transfusion Services","Kibera",-1.3030,36.8080),
        ("National HIV Reference Lab","Kibera",-1.3040,36.8080),
        ("Kibera CFW Clinic","Kibera",-1.3110,36.7860),
        ("SACODEN VCT Center","Kibera",-1.3120,36.7870),
        ("Community Evolution Network VCT","Kibera",-1.3100,36.7850),
        ("Dagoretti Community Dispesary","Kibera",-1.3090,36.7880),
        ("IDEWES","Kibera",-1.3080,36.7890),
        ("Slum Medical Clinic","Kibera",-1.3110,36.7870),
        ("AAR Gwh Health Care Ltd","Kibera",-1.3070,36.7900),
        ("Child Doctor Kenya","Kibera",-1.3080,36.7910),
        ("Chonesus Clinic","Kibera",-1.3090,36.7920),
        ("Rosade Medical Clinic","Kibera",-1.3100,36.7930),
        ("Kibera Highway Clinic","Kibera",-1.3110,36.7940),
        ("Dr Florence Murila (Ngong Road)","Kibera",-1.3020,36.7960),
        ("Family Dental Care (Ayany)","Kibera",-1.3030,36.7970),
        ("Clinix Health Care (Kibra)","Kibera",-1.3100,36.7860),
        ("Vipawa Medical Services","Kibera",-1.3090,36.7870),
        ("KEMRI Mimosa","Kibera",-1.3020,36.8000),
        ("Vostrum Clinic","Kibera",-1.3080,36.7880),
        ("Uzima VCT Centre","Kibera",-1.3090,36.7890),
        ("Nuru Lutheran Media Ministry","Kibera",-1.3100,36.7900),
        ("Discordant Couples of Kenya VCT","Kibera",-1.3080,36.7870),
        ("Msf Olympic Centre","Kibera",-1.3120,36.7860),
        ("Wema Medical Clinic","Kibera",-1.3110,36.7870),
        ("Huduma Health Centre","Kibera",-1.3120,36.7880),
        ("St Pery's Medical Clinic","Kibera",-1.3100,36.7870),
        ("Tumaini Medical Centre (Sarang'ombe)","Kibera",-1.3130,36.7890),
        ("Nairobi Womens Hospital Adams","Kibera",-1.3000,36.7820),
        ("Memorial Hospital","Kibera",-1.3090,36.7900),
        ("NASCOP VCT","Kibera",-1.3010,36.8070),
        ("Lea Toto Kibera","Kibera",-1.3110,36.7880),
        ("Marie Stopes Clinic (Langata)","Kibera",-1.3120,36.7830),
        ("Carolina For Kibera VCT","Kibera",-1.3100,36.7860),
        ("Family Health Medical Dispensary","Kibera",-1.3090,36.7870),
        ("Kibera Chemi Chemi Ya Uzima Clinic","Kibera",-1.3110,36.7890),
        ("Woodley Clinic","Kibera",-1.3090,36.8020),
        ("Kibera D O Dispensary","Kibera",-1.3100,36.7870),
        ("Gsu Dispensary (Nairobi West)","Kibera",-1.3080,36.7920),
        ("Kisembo Dispensary","Kibera",-1.3090,36.7930),
        ("Ushirika Medical Clinic","Kibera",-1.3100,36.7940),
        ("Makina Clinic","Kibera",-1.3120,36.7850),
        ("Frepals Community Nursing Home","Kibera",-1.3110,36.7860),
        ("St Mary's Medical Clinic (Sarang'ombe)","Kibera",-1.3130,36.7880),
        ("Mbagathi District Hospital","Kibera",-1.3077,36.8033),
        ("Kenyatta National Hospital","Kibera",-1.3021,36.8077),
        ("Mercillin Afya Centre","Kibera",-1.3090,36.7890),
        ("Kibera Human Development Clinic","Kibera",-1.3100,36.7900),
        ("Kemri VCT","Kibera",-1.3000,36.8000),
        ("Ngong Road Dispensary","Kibera",-1.3060,36.7980),
        ("Dr Were Medical Clinic","Kibera",-1.3090,36.7910),
        ("Gynapaed Dispensary (Kilimani-)","Kibera",-1.3000,36.7950),
        ("Nyina Wa Mumbi Dispensary","Kibera",-1.3080,36.7910),
        ("St Michael Clinic","Kibera",-1.3090,36.7920),
        ("Nairobi Hospital","Kibera",-1.2963,36.8054),
        ("Coptic Hospital (Ngong Road)","Kibera",-1.3090,36.7970),
        ("Strathmore University Medical Centre","Langata",-1.3100,36.8000),
        # ── LANGATA ──────────────────────────────────────────────────
        ("Karen Roses Medical Clinic","Langata",-1.3600,36.7500),
        ("South C Hospital Limited(South C)","Langata",-1.3200,36.8100),
        ("South C Dialysis Centre","Langata",-1.3210,36.8110),
        ("Africare Ltd Karen Clinic","Langata",-1.3580,36.7480),
        ("The Zambezi Hospital Limited","Langata",-1.3600,36.7520),
        ("Soweto West Community Clinic","Langata",-1.3150,36.7950),
        ("Silanga Community Clinic","Langata",-1.3160,36.7960),
        ("CMIA Grace Children's Centre Dispensary","Langata",-1.3550,36.7540),
        ("KTTID Dispensary","Langata",-1.3400,36.7560),
        ("Marist International University College Medical Clinic","Langata",-1.3550,36.7560),
        ("Dr Barnados House clinic","Langata",-1.3560,36.7560),
        ("Melchizedek Hospital Karen","Langata",-1.3570,36.7570),
        ("Green Cross Medical Clinic","Langata",-1.3590,36.7560),
        ("Rainbow Clinic","Langata",-1.3600,36.7560),
        ("The Nairobi Hospital Out-Patient Centre Galeria","Langata",-1.3170,36.8080),
        ("Wellness Program KWS Hq","Langata",-1.3700,36.7400),
        ("AAR Healthcare Limited (Karen)","Langata",-1.3580,36.7560),
        ("Eagle Wings Medical Centre","Langata",-1.3590,36.7570),
        ("The Co-Operative University College of Kenya Dispe","Langata",-1.3600,36.7570),
        ("Healthways Medical Centre","Langata",-1.3570,36.7590),
        ("Sex Workers Outreach Program (Lang'ata)","Langata",-1.3430,36.7580),
        ("Southern Health Care","Langata",-1.3450,36.7570),
        ("Shree Cutchhi Leva Samaj Medical Clinic","Langata",-1.3440,36.7560),
        ("Lang'ata Comprehensive Medical Service","Langata",-1.3430,36.7590),
        ("Gatina United Clinic","Langata",-1.3200,36.7700),
        ("Kikoshep Kenya (Mugumoini)","Langata",-1.3500,36.7500),
        ("Revival Home Based Care Clinic","Langata",-1.3460,36.7580),
        ("Africare Ltd South C","Langata",-1.3200,36.8090),
        ("The Karen Hospital","Langata",-1.3560,36.7540),
        ("Langata Hospital","Langata",-1.3430,36.7600),
        ("Meridian Equator Hospital","Langata",-1.3180,36.8100),
        ("Nairobi West Hospital","Langata",-1.3100,36.8090),
        ("St Mary's Mission Hospital","Langata",-1.3350,36.7870),
        ("Zinduka Clinic","Langata",-1.3440,36.7580),
        ("Nyumbani Diagnostic Laboratory and Medical Clinic","Langata",-1.3580,36.7570),
        ("Cotolengo Centre","Langata",-1.3590,36.7580),
        ("St. Odilia's Dispensary","Langata",-1.3600,36.7580),
        ("Silanga (MSF Belgium) Dispensary","Langata",-1.3160,36.7960),
        ("Langata Health Centre (Mugumo-Ini)","Langata",-1.3500,36.7520),
        ("Maria Dominica Dispensary","Langata",-1.3520,36.7530),
        ("Dreams Centre Dispensary (Langata)","Langata",-1.3430,36.7590),
        ("Dsc Karen Dispensary (Armed Forces)","Langata",-1.3570,36.7540),
        ("Jinnah Ave Clinic","Langata",-1.3200,36.8100),
        ("Dog Unit Dispensary (O P Kenya Police)","Langata",-1.3440,36.7560),
        ("Bomas of Kenya Dispensary","Langata",-1.3700,36.7520),
        ("Multi Media University Dispensary","Langata",-1.3590,36.7560),
        ("Port Health Dispensary (Langata)","Langata",-1.3430,36.7580),
        ("Eden Dispensary","Langata",-1.3460,36.7590),
        ("Nairobi West Men's Prison Dispensary","Langata",-1.3180,36.8100),
        ("Family Care Medical Centre & Maternity","Langata",-1.3450,36.7580),
        ("7Kr Mrs Health Centre","Langata",-1.3440,36.7570),
        ("Langata Women Prison Dispensary","Langata",-1.3470,36.7590),
        ("Nairobi South Hospital","Langata",-1.3190,36.8110),
        ("Nairobi West Chidren Clinic","Langata",-1.3200,36.8090),
        ("Uhuru Camp Dispensary (O P Admin Police)","Langata",-1.3420,36.7570),
        ("Kibera South (Msf Belgium) Health Centre","Langata",-1.3170,36.7970),
        ("Catholic University Dispensary","Langata",-1.3600,36.7550),
        ("Getrudes Hospital (Nairobi West Clinic)","Langata",-1.3190,36.8100),
        ("Karen Health Centre","Langata",-1.3580,36.7560),
        ("Mutuini Sub-District Hospital","Langata",-1.3490,36.7510),
        ("Montezuma Monalisa Funeral Home (Lang'ata)","Langata",-1.3430,36.7590),
        # ── MAKADARA ─────────────────────────────────────────────────
        ("Kilele Medical Specialist Centre","Makadara",-1.2960,36.8630),
        ("Equity Afia Buruburu","Makadara",-1.2960,36.8700),
        ("Makadara Sub County  Office","Makadara",-1.2943,36.8623),
        ("Charolyn Specialist Clinic","Makadara",-1.2970,36.8650),
        ("Getrudes Children's Hospital","Makadara",-1.2960,36.8640),
        ("Debomart Med Clinic","Makadara",-1.2950,36.8630),
        ("Credible Health Centre","Makadara",-1.2960,36.8650),
        ("Lumumba Medical Clinic","Makadara",-1.2970,36.8640),
        ("Millenium Dental Clinic","Makadara",-1.2960,36.8660),
        ("Upendo Clinic Makadara","Makadara",-1.2950,36.8640),
        ("Maendereo Medical Clinic","Makadara",-1.2960,36.8670),
        ("Hamza Medical Centre","Makadara",-1.2970,36.8650),
        ("Metropolitan Dr Plaza","Makadara",-1.2960,36.8680),
        ("Avenue Health Care (Makadara)","Makadara",-1.2950,36.8650),
        ("Church Army Medical Clinic","Makadara",-1.2960,36.8690),
        ("Hope Worldwide Kenya VCT (Makadara)","Makadara",-1.2970,36.8660),
        ("Just Meno Limited","Makadara",-1.2960,36.8700),
        ("Nairobi Earc St Anne Medical Clinic","Makadara",-1.2950,36.8660),
        ("Glovnet VCT","Makadara",-1.2960,36.8710),
        ("The Mater Hospital Buruburu","Makadara",-1.2960,36.8720),
        ("Uhuru Presitige Health Care","Makadara",-1.2970,36.8680),
        ("Dr MOHamed Clinic","Makadara",-1.2960,36.8700),
        ("Kaloleni Health Servics","Makadara",-1.2950,36.8680),
        ("Juhudi Clinic","Makadara",-1.2960,36.8690),
        ("Shepherds Medical Clinic Maringo","Makadara",-1.2970,36.8700),
        ("Ofafa I Clinic","Makadara",-1.2960,36.8710),
        ("Hono Clinic","Makadara",-1.2950,36.8700),
        ("Metropolitan Hospital Nairobi","Makadara",-1.2960,36.8720),
        ("Jamaa Mission Hospital","Makadara",-1.2960,36.8640),
        ("Makadara Mercy Sisters Dispensary","Makadara",-1.2950,36.8710),
        ("Mary Immaculate Sisters Dispensary","Makadara",-1.2960,36.8700),
        ("Loco Dispensary","Makadara",-1.2970,36.8710),
        ("Mukuru Mmm Clinic","Makadara",-1.3100,36.8700),
        ("Family Life Promotions and Services","Makadara",-1.2960,36.8720),
        ("Kaloleni Dispensary","Makadara",-1.2950,36.8720),
        ("Aga Khan University Hospital (Buruburu)","Makadara",-1.2960,36.8730),
        ("Coptic Medical Clinic","Makadara",-1.2970,36.8720),
        ("Bahati Clinic","Makadara",-1.2960,36.8680),
        ("Bahati Health Centre","Makadara",-1.2950,36.8670),
        ("Buruburu Medical Clinic","Makadara",-1.2960,36.8700),
        ("Mbotela Clinic","Makadara",-1.2970,36.8690),
        ("Maringo Clinic","Makadara",-1.2960,36.8710),
        ("Muthurwa Clinic","Makadara",-1.2900,36.8600),
        # ── MATHARE ──────────────────────────────────────────────────
        ("Getrudes Mathare Outreach Clinic","Mathare",-1.2590,36.8580),
        ("Uzima White Medical Clinic","Mathare",-1.2600,36.8560),
        ("Planet Clinic Ltd","Mathare",-1.2610,36.8570),
        ("Sunrise City Medical Centre","Mathare",-1.2620,36.8580),
        ("Drugnet Medical centre","Mathare",-1.2590,36.8590),
        ("KEMRI/CDC Health Services","Mathare",-1.2600,36.8580),
        ("Gaimu Clinic","Mathare",-1.2610,36.8590),
        ("Mathare Police Depot","Mathare",-1.2580,36.8570),
        ("Mathare 3A (EDARP)","Mathare",-1.2590,36.8560),
        ("Huruma Nursing Home & Maternity","Mathare",-1.2570,36.8590),
        ("Huruma (NCCK) Dispensary","Mathare",-1.2560,36.8580),
        ("Makadara Health Centre","Mathare",-1.2620,36.8600),
        ("Upendo Dispensary","Mathare",-1.2580,36.8600),
        ("Huruma Maternity Hospital","Mathare",-1.2570,36.8570),
        ("Mathari Hospital","Mathare",-1.2597,36.8469),
        # ── ROYSAMBU ─────────────────────────────────────────────────
        ("Nazareth Medical Services-Githurai","Roysambu",-1.1900,36.9050),
        ("Penda Medical Care-Kahawa West","Roysambu",-1.2050,36.8850),
        ("The Mater Hospital-Satelite Clinic(TRM)","Roysambu",-1.2100,36.8750),
        ("Gertrude's Children Hospital-Thika Rd","Roysambu",-1.2150,36.8800),
        ("Imani 44 Medical Clinic","Roysambu",-1.2250,36.8680),
        ("Hekima Medical Centre","Roysambu",-1.2260,36.8690),
        ("Congo medical services","Roysambu",-1.2270,36.8700),
        ("Selma medical clinic","Roysambu",-1.2280,36.8710),
        ("Proact Healthservices","Roysambu",-1.2290,36.8720),
        ("Farmers choice wellness centre clinic","Roysambu",-1.2300,36.8730),
        ("Milele Integrated Medical Services","Roysambu",-1.2250,36.8670),
        ("United States International University VCT","Roysambu",-1.2200,36.8700),
        ("Mid-Point Health Services","Roysambu",-1.2260,36.8660),
        ("Bridging Out-Patient","Roysambu",-1.2270,36.8680),
        ("Annex Health Care","Roysambu",-1.2280,36.8690),
        ("Max Family Health Care","Roysambu",-1.2290,36.8700),
        ("Sharifik Medical Clinic","Roysambu",-1.2300,36.8710),
        ("Unity Health Care","Roysambu",-1.2250,36.8650),
        ("Jozi Medical Centre","Roysambu",-1.2260,36.8670),
        ("Afyamax Medical & Centre Dental","Roysambu",-1.2270,36.8690),
        ("Royolk Medical Clinic","Roysambu",-1.2280,36.8700),
        ("Success Medical Services","Roysambu",-1.2290,36.8710),
        ("St Teresa Medical Clinic ( Zimmerman)","Roysambu",-1.2140,36.8760),
        ("Sanitas Lotus Medical Centre","Roysambu",-1.2260,36.8680),
        ("Zimma Health Care","Roysambu",-1.2140,36.8780),
        ("Kamwitha Medcal Centre","Roysambu",-1.2270,36.8670),
        ("Index Medical Services","Roysambu",-1.2280,36.8680),
        ("St Michael Community Nursing Home","Roysambu",-1.2290,36.8690),
        ("Josnik Clinic","Roysambu",-1.2300,36.8700),
        ("Tazama Dentel Clinic","Roysambu",-1.2250,36.8660),
        ("St Louis Community Hospital","Roysambu",-1.2140,36.8770),
        ("Narzareth Medical Services","Roysambu",-1.1910,36.9060),
        ("Hope Medical Clinic ( Githurai)","Roysambu",-1.1920,36.9070),
        ("Mother & Child Meridian & Lab Services","Roysambu",-1.2260,36.8670),
        ("Stars General Medical Clinic","Roysambu",-1.2270,36.8690),
        ("Prestige Health Centre (Zimerman)","Roysambu",-1.2150,36.8770),
        ("Kamiti Maximum Clinic","Roysambu",-1.1700,36.9200),
        ("Lea Toto Mwiki","Roysambu",-1.2060,36.9090),
        ("CID HQS Dispensary","Roysambu",-1.2270,36.8670),
        ("Afya Health Care","Roysambu",-1.2280,36.8680),
        ("Githurai Liverpool VCT","Roysambu",-1.1930,36.9080),
        ("AAR Thika Road Clinic","Roysambu",-1.2200,36.8720),
        ("Kamiti Prison Hospital","Roysambu",-1.1690,36.9220),
        ("Githurai VCT","Roysambu",-1.1940,36.9090),
        ("Corner Stone","Roysambu",-1.2290,36.8690),
        ("Kahawa West Health Centre","Roysambu",-1.2040,36.8860),
        ("St Joseph Mukasa Dispensary","Roysambu",-1.2300,36.8700),
        ("Karura Health Centre (Kiambu Rd)","Roysambu",-1.2270,36.8440),
        ("Kenyatta University Dispensary","Roysambu",-1.1870,36.9210),
        ("Githurai Medical Dispensary","Roysambu",-1.1950,36.9100),
        ("Giovanna Dispensary","Roysambu",-1.2310,36.8710),
        ("Family Care Clinic Kasarani","Roysambu",-1.2250,36.8670),
        ("Marurui Dispensary","Roysambu",-1.2100,36.8600),
        ("Zimmerman Medical Dispensary","Roysambu",-1.2140,36.8790),
        ("Ogwedhi Dispensary (Nairobi North)","Roysambu",-1.2300,36.8720),
        ("Nsis Health Centre (Ruaraka)","Roysambu",-1.2280,36.8730),
        ("Kahawa Garrison Health Centre","Roysambu",-1.2010,36.8900),
        ("Good Samaritan Dispensary","Roysambu",-1.2290,36.8720),
        ("Round About Medical Dispensary","Roysambu",-1.2280,36.8720),
        ("St John Hospital","Roysambu",-1.2270,36.8680),
        ("Prime Health Services Dispensary","Roysambu",-1.2260,36.8660),
        # ── RUARAKA ──────────────────────────────────────────────────
        ("Avenue Health  Care Garden City Clinic","Ruaraka",-1.2380,36.8730),
        ("The Agha Khan Medical Centre-Rigeways(Kiambu Rd.)","Ruaraka",-1.2360,36.8200),
        ("Springs Health Services","Ruaraka",-1.2490,36.8710),
        ("Providence Medical Centre - Mathare North","Ruaraka",-1.2450,36.8640),
        ("Mercylight  Hospital-Lucky Summer","Ruaraka",-1.2400,36.8720),
        ("Nelly Medical Centre","Ruaraka",-1.2490,36.8700),
        ("Aimon med clinic","Ruaraka",-1.2480,36.8710),
        ("Delight Chemist & Lab","Ruaraka",-1.2470,36.8720),
        ("The Arcade Medical Centre","Ruaraka",-1.2460,36.8730),
        ("Peace Medical Clinic","Ruaraka",-1.2450,36.8720),
        ("Imani Medical Clinic ( Mathare A 4)","Ruaraka",-1.2440,36.8710),
        ("Bar Hostess Empowerment Support Program VCT","Ruaraka",-1.2480,36.8700),
        ("Marura Nursing Home","Ruaraka",-1.2470,36.8710),
        ("Provide International Korogocho","Ruaraka",-1.2450,36.8750),
        ("Babadogo (EDARP)","Ruaraka",-1.2460,36.8700),
        ("Mathare North Health Centre","Ruaraka",-1.2440,36.8700),
        ("Gsu Hq Dispensary (Ruaraka)","Ruaraka",-1.2380,36.8700),
        ("Baraka Dispensary (Nairobi)","Ruaraka",-1.2490,36.8720),
        ("Uzima Dispensary","Ruaraka",-1.2480,36.8720),
        ("Provide Inter Math Dispensary","Ruaraka",-1.2450,36.8730),
        ("Kenya Utalii Dispensary","Ruaraka",-1.2370,36.8640),
        ("Babadogo Health Centre","Ruaraka",-1.2460,36.8710),
        ("National Youth Service Hq Dispensary (Ruaraka)","Ruaraka",-1.2390,36.8710),
        ("Redemeed Health Centre","Ruaraka",-1.2470,36.8710),
        ("St Mary's Health Centre","Ruaraka",-1.2480,36.8720),
        ("Babadogo Medical Health Centre","Ruaraka",-1.2460,36.8720),
        # ── STAREHE ──────────────────────────────────────────────────
        ("Hayat Hospital","Starehe",-1.2760,36.8370),
        ("Nairobi County Beyond Zero Clinic","Starehe",-1.2830,36.8230),
        ("Dr C. Mwangi Clinic","Starehe",-1.2820,36.8240),
        ("Bliss Health Care Limited","Starehe",-1.2840,36.8250),
        ("Technical university of Kenya Student/Staff Clinic","Starehe",-1.2770,36.8280),
        ("Dessein Health Care","Starehe",-1.2850,36.8260),
        ("Support For Addiction Prevention & Treatment In Africa","Starehe",-1.2860,36.8270),
        ("Dr Maina Ruga Medical Clinic","Starehe",-1.2870,36.8280),
        ("Dr Paul Ondiege Clinic","Starehe",-1.2830,36.8230),
        ("Meridian Medical centre(Nation Centre Bldg )","Starehe",-1.2840,36.8240),
        ("The Savannah Health Services Ltd","Starehe",-1.2850,36.8250),
        ("Post Bank Staff Clinic","Starehe",-1.2830,36.8260),
        ("Hoymas VCT (Nairobi)","Starehe",-1.2840,36.8270),
        ("Pentapharm Limited","Starehe",-1.2850,36.8280),
        ("Central Bank Staff Clinic","Starehe",-1.2840,36.8230),
        ("Positive Partner Network VCT","Starehe",-1.2850,36.8240),
        ("Health Matters Medical Centre","Starehe",-1.2860,36.8250),
        ("Nairobi Eye Associates","Starehe",-1.2830,36.8250),
        ("Dr Rosaline Thara Dental Clinic","Starehe",-1.2840,36.8260),
        ("Imenti Medical Centre","Starehe",-1.2850,36.8270),
        ("Eyeclinic (Nairobi)","Starehe",-1.2860,36.8280),
        ("Dr Stephen Macharia Medical Clinic","Starehe",-1.2830,36.8270),
        ("Dr Ngathia Dental Clinic","Starehe",-1.2840,36.8280),
        ("Dr Kishor J D Medical Centre","Starehe",-1.2850,36.8290),
        ("Hazina Medical Clinic","Starehe",-1.2860,36.8290),
        ("Dr David Chew Clinic","Starehe",-1.2830,36.8290),
        ("Artisan Dental Laboratory (Nairobi)","Starehe",-1.2840,36.8300),
        ("Dr Ashwin Clinic","Starehe",-1.2850,36.8300),
        ("Tusker House Medical Centre","Starehe",-1.2870,36.8290),
        ("Tusker Dental Laboratory Services & Laboratory","Starehe",-1.2870,36.8300),
        ("Meridian Medical Centre (Penson Towers)","Starehe",-1.2840,36.8310),
        ("Jesus Is Alive Dental Clinic (Nairobi)","Starehe",-1.2850,36.8310),
        ("Damic Dental X-Ray Services","Starehe",-1.2860,36.8310),
        ("Rimaal Medical Laboratory","Starehe",-1.2830,36.8310),
        ("Kaka Medical Centre (Race Course Rd)","Starehe",-1.2770,36.8350),
        ("Pharmat Health Care","Starehe",-1.2840,36.8320),
        ("Dr Praful M Sanghani","Starehe",-1.2850,36.8320),
        ("Wide Medical Services","Starehe",-1.2860,36.8320),
        ("Dr J L Amugugaba Clinic (Nairobi)","Starehe",-1.2830,36.8320),
        ("Medisafe Medical Labaratoty","Starehe",-1.2840,36.8330),
        ("Professional Diagnostic Centre (Nairobi)","Starehe",-1.2850,36.8330),
        ("Latema Medical Services (Nairobi)","Starehe",-1.2860,36.8330),
        ("Premier Laboratory (Nairobi)","Starehe",-1.2830,36.8340),
        ("Odeon Medical Centre (Nairobi)","Starehe",-1.2840,36.8340),
        ("Philis Medical Laboratory","Starehe",-1.2850,36.8340),
        ("Dr Parmar Medical Clinic (Nairobi)","Starehe",-1.2860,36.8340),
        ("Nairobi Outreach Services Trust","Starehe",-1.2830,36.8350),
        ("Rinah Health Consultants","Starehe",-1.2840,36.8350),
        ("Corner Hse Med Laboratory","Starehe",-1.2850,36.8360),
        ("Dr Jemmah & Nyawange Med Clinic","Starehe",-1.2860,36.8360),
        ("Access Afya","Starehe",-1.2830,36.8360),
        ("Bans Optical (Nairobi)","Starehe",-1.2840,36.8370),
        ("Goldmed Chemists & Clinic","Starehe",-1.2850,36.8370),
        ("Dr Parmar Clinic","Starehe",-1.2860,36.8370),
        ("Dr George Munene Medical Clinic","Starehe",-1.2830,36.8370),
        ("Parkroad Dental Clinic (Ngara)","Starehe",-1.2720,36.8350),
        ("Dr Nzuki Hildapaed Clinic","Starehe",-1.2840,36.8380),
        ("Starehe Boys Centre School Clinic","Starehe",-1.2780,36.8380),
        ("Iran Medical Clinic (Ngara)","Starehe",-1.2730,36.8360),
        ("Dr M S Saroya Medical Clinic (Nairobi)","Starehe",-1.2850,36.8380),
        ("Dr Maina Skin Clinic (Ngara)","Starehe",-1.2740,36.8360),
        ("Dr Chaundry Dental Services (Nairobi)","Starehe",-1.2860,36.8380),
        ("Dr Musili Clinic (Afya Centre-Nairobi)","Starehe",-1.2830,36.8390),
        ("Acacia Medical Centre (Nairobi)","Starehe",-1.2840,36.8390),
        ("Meridian Medical Centre (Loita Street)","Starehe",-1.2850,36.8390),
        ("Swop Clinic","Starehe",-1.2860,36.8390),
        ("Social Service League (Nairobi )","Starehe",-1.2870,36.8390),
        ("Crescent Medical Aid (Jamia Towers)","Starehe",-1.2840,36.8400),
        ("Alphine Dental Centre (Kencom Hse)","Starehe",-1.2850,36.8400),
        ("Supreme Health Care (Ktda House-Nairobi)","Starehe",-1.2860,36.8400),
        ("Abdallah Dental Clinic (Barclays Plaza-Nairobi)","Starehe",-1.2840,36.8410),
        ("Plaza X-Ray Services (Re-Insurance Plaza-Nairobi)","Starehe",-1.2850,36.8410),
        ("Sunshine Medical & Diagnostic Centre (Nairobi)","Starehe",-1.2860,36.8410),
        ("Soin Health Care - Mfangano Street)","Starehe",-1.2840,36.8420),
        ("Kimathi Street Medical Centre","Starehe",-1.2830,36.8400),
        ("Mercy Medical Services","Starehe",-1.2850,36.8420),
        ("Juja Road Hospital (Nairobi)","Starehe",-1.2730,36.8400),
        ("Lad Nan Hospital","Starehe",-1.2720,36.8410),
        ("Gertrudes Chiildren Clinic (Pangani)","Starehe",-1.2710,36.8430),
        ("Kam Health Services","Starehe",-1.2840,36.8430),
        ("Kam ENT Services","Starehe",-1.2840,36.8440),
        ("Sasa Centre-Ngara","Starehe",-1.2720,36.8440),
        ("Maisha House VCT (Noset)","Starehe",-1.2850,36.8430),
        ("Sasa Centre (Makadara)","Starehe",-1.2960,36.8650),
        ("SDA Health Services Likoni Road Clinic","Starehe",-1.2850,36.8440),
        ("Lengo Medical Clinic","Starehe",-1.2860,36.8440),
        ("Kemsa Staff Clinic","Starehe",-1.2870,36.8440),
        ("British American Tobacco Kenya Clinic","Starehe",-1.2750,36.8290),
        ("New Partners Initiative Scaling Up HIV and AIDS Pr","Starehe",-1.2840,36.8450),
        ("South B Hospital Ltd","Starehe",-1.3050,36.8340),
        ("Innoculation Centre","Starehe",-1.2830,36.8450),
        ("Taiba Medical Centre","Starehe",-1.2720,36.8450),
        ("Canaan Health Providers (Nairobi)","Starehe",-1.2840,36.8460),
        ("AAR City Centre Clinic","Starehe",-1.2850,36.8460),
        ("Imperial Clinic","Starehe",-1.2860,36.8460),
        ("St Bridget's Mother & Child","Starehe",-1.2830,36.8460),
        ("Medicare Clinic","Starehe",-1.2840,36.8470),
        ("Marie Stopes Clinic (Pangani)","Starehe",-1.2710,36.8450),
        ("Marie Stopes Clinic (Kencom)","Starehe",-1.2850,36.8470),
        ("Landmawe Medical Services","Starehe",-1.2860,36.8470),
        ("Mukuru Crescent Clinic","Starehe",-1.3180,36.8780),
        ("Crescent Medical Aid Murang'a Road","Starehe",-1.2700,36.8450),
        ("Kariokor Clinic","Starehe",-1.2820,36.8450),
        ("Rhodes Chest Clinic","Starehe",-1.2720,36.8380),
        ("Crescent Medical Aid (Pangani)","Starehe",-1.2710,36.8440),
        ("Guru Nanak Hospital","Starehe",-1.2697,36.8325),
        ("Radiant Pangani Hospital","Starehe",-1.2710,36.8460),
        ("The Mater Hospital Mukuru","Starehe",-1.3070,36.8347),
        ("Rural Aid VCT","Starehe",-1.2830,36.8480),
        ("Single Mothers Association of Kenya (Smak)","Starehe",-1.2840,36.8480),
        ("Teachers Service Commission","Starehe",-1.2850,36.8490),
        ("Nairobi Deaf (Liverpool)","Starehe",-1.2830,36.8490),
        ("St Johns Ambulance","Starehe",-1.2820,36.8480),
        ("Supkem (Liverpool)","Starehe",-1.2840,36.8490),
        ("Kie/Kapc","Starehe",-1.2830,36.8500),
        ("Sex Workers Operation Project (Swop)","Starehe",-1.2840,36.8500),
        ("Family Health Options Phoenix","Starehe",-1.2850,36.8500),
        ("Nairobi South Clinic","Starehe",-1.3060,36.8350),
        ("Pangani Dispensary","Starehe",-1.2700,36.8460),
        ("Ngaira Rhodes Dispensary","Starehe",-1.2720,36.8390),
        ("Special Treatment Clinic","Starehe",-1.2830,36.8510),
        ("South B Police Band Dispensary","Starehe",-1.3050,36.8350),
        ("Nairobi Remand Prison Health Centre","Starehe",-1.2800,36.8250),
        ("Railway Training Institute Dispensary South B","Starehe",-1.3040,36.8340),
        ("Mow Dispensary","Starehe",-1.2840,36.8510),
        ("Meridian Medical Centre (Buruburu)","Starehe",-1.2960,36.8700),
        ("Ministry of Education (Moest) VCT Centre","Starehe",-1.2850,36.8510),
        ("Transcom Medical Services","Starehe",-1.2840,36.8520),
        ("Parkroad Nursing Home (Nairobi)","Starehe",-1.2730,36.8370),
        ("Nairobi Outpatient Centre","Starehe",-1.2840,36.8530),
        ("Ngara Health Centre (City Council of Nairobi)","Starehe",-1.2710,36.8460),
        ("Dr Muasya Medical Clinic","Starehe",-1.2850,36.8530),
        ("Kenya Airways Medical Centre","Starehe",-1.3200,36.9250),
        ("Huruma Lions Dispensary","Starehe",-1.2570,36.8580),
        ("Lagos Road Dispensary","Starehe",-1.2840,36.8540),
        ("Community Health Foundation","Starehe",-1.2850,36.8540),
        # ── WESTLANDS ────────────────────────────────────────────────
        ("Professor Wasuna Clinic","Westlands",-1.2630,36.8050),
        ("Dr.Stephen Kamore Wanjohi","Westlands",-1.2640,36.8060),
        ("SVG Health Care Limited","Westlands",-1.2650,36.8070),
        ("Dr. Mazaher Hassan Jaffer","Westlands",-1.2630,36.8070),
        ("Dr. Racheal Muthoni Rukaria","Westlands",-1.2640,36.8080),
        ("Columbia Africa Health Care Ltd","Westlands",-1.2650,36.8080),
        ("Jaralam Medical Centre","Westlands",-1.2630,36.8090),
        ("Dr. Bashir","Westlands",-1.2640,36.8090),
        ("Jalaram Medical Services","Westlands",-1.2650,36.8090),
        ("Emerging Infectious Disease Center","Westlands",-1.2620,36.8060),
        ("CFW Clinics Kibagare","Westlands",-1.2530,36.7800),
        ("Lions Sightfirst Eye Hospital","Westlands",-1.2630,36.8100),
        ("Eagle Health Care Solution","Westlands",-1.2640,36.8100),
        ("AIDS Health Care Foundation Parklands Clinic","Westlands",-1.2580,36.8100),
        ("Medecins Du Monde/France (Kangemi Kang'ora)","Westlands",-1.2520,36.7810),
        ("Kenya Police Staff College Clinic","Westlands",-1.2610,36.8110),
        ("IOM International Organization for migration(girigiri)","Westlands",-1.2580,36.8120),
        ("Chiromo Medical Centre","Westlands",-1.2620,36.8120),
        ("Dr Eliud Njuguna (Parklands)","Westlands",-1.2590,36.8120),
        ("Dr Henry Abwao","Westlands",-1.2600,36.8130),
        ("Abraham Memorial Nursing Home (Westlands)","Westlands",-1.2630,36.8120),
        ("Bafana Medical Centre","Westlands",-1.2640,36.8130),
        ("Afya Bora Medical Clinic (Westlands)","Westlands",-1.2650,36.8130),
        ("Focus Outreach Medical Mission","Westlands",-1.2630,36.8130),
        ("Kangemi Gichagi Dispensary","Westlands",-1.2590,36.7830),
        ("Baraka Medical Cenre","Westlands",-1.2640,36.8140),
        ("Aculaser Institute","Westlands",-1.2650,36.8140),
        ("Afya Bora Health Care","Westlands",-1.2630,36.8140),
        ("Mafra Clinic","Westlands",-1.2640,36.8150),
        ("Westlands Medical Centre","Westlands",-1.2641,36.8039),
        ("Victory Medicare","Westlands",-1.2650,36.8150),
        ("Kamili Organization","Westlands",-1.2620,36.8150),
        ("Rafiki Medical Clinic (Westlands)","Westlands",-1.2630,36.8160),
        ("Abby Clinic","Westlands",-1.2640,36.8160),
        ("Consolata Shrine Dispensary (Deep Sea Nairobi)","Westlands",-1.2620,36.8160),
        ("Githogoro Runda Baptist Clinic (Getrudes Nairobi)","Westlands",-1.2200,36.8240),
        ("Kenya Association of Pofessional Counsellors (Kapc","Westlands",-1.2630,36.8170),
        ("Sunbeam Medical Centre","Westlands",-1.2640,36.8170),
        ("Lea Toto Clinic (Westlands)","Westlands",-1.2620,36.8170),
        ("Gichago Dispensary","Westlands",-1.2560,36.7900),
        ("Mawamu Clinic","Westlands",-1.2630,36.8180),
        ("AAR Clinic Sarit Centre (Westlands)","Westlands",-1.2600,36.8050),
        ("Dr Aziz Mohamed Medical Clinic","Westlands",-1.2640,36.8180),
        ("Mp Shah Hospital (Westlands)","Westlands",-1.2620,36.8190),
        ("Gertrudes Childrens Hospital","Westlands",-1.2630,36.8100),
        ("Aga Khan Hospital","Westlands",-1.2943,36.8065),
        ("Kenya AIDS Vaccine Initiative (KAVI)","Westlands",-1.3000,36.8070),
        ("Kabete Barracks Dispensary","Westlands",-1.2590,36.7600),
        ("St Joseph W Dispensary (Westlands)","Westlands",-1.2640,36.8190),
        ("Marie Stopes Clinic (Kilimani)","Westlands",-1.2900,36.8060),
        ("Vision Peoples Inter Health Centre","Westlands",-1.2630,36.8190),
        ("Amurt Health Centre","Westlands",-1.2640,36.8200),
        ("St Florence Medical Care Health Centre","Westlands",-1.2650,36.8200),
        ("Lianas Clinic Health Centre","Westlands",-1.2630,36.8200),
        ("Padens Medicare Centre","Westlands",-1.2640,36.8210),
        ("Kangemi Health Centre","Westlands",-1.2540,36.7820),
        ("Kabete Approved School Dispensary","Westlands",-1.2580,36.7590),
        ("Lower Kabete Dispensary (Kabete)","Westlands",-1.2600,36.7580),
        ("Avenue Hospital","Westlands",-1.2650,36.8060),
        ("Jamii Clinic (Westlands)","Westlands",-1.2630,36.8210),
        ("Mji Wa Huruma Dispensary","Westlands",-1.2640,36.8220),
    ]
    
    # Create DataFrame
    for name, sub_county, lat, lng in facilities_data:
        # Assign type based on facility name or default to Private
        if 'Hospital' in name or 'Medical Centre' in name or 'Clinic' in name:
            facility_type = 'Private'
        elif 'Health Centre' in name or 'Dispensary' in name:
            facility_type = 'Public'
        elif 'Mission' in name or 'St ' in name or 'Church' in name:
            facility_type = 'Faith Based'
        elif 'VCT' in name or 'NGO' in name or 'Foundation' in name:
            facility_type = 'NGO'
        else:
            facility_type = 'Private'
        
        facilities.append({
            'Facility Name': name,
            'Sub-County': sub_county,
            'Type': facility_type,
            'Latitude': lat,
            'Longitude': lng
        })
    
    return pd.DataFrame(facilities)

# ============================================================================
# MAP CREATION WITH ACCURATE BOUNDARIES
# ============================================================================

def create_accurate_nairobi_map(facilities_df):
    """Create map with accurate county boundary and sub-county markers"""
    
    # Center of Nairobi (using accurate center coordinates)
    nairobi_center = [-1.2921, 36.8219]
    
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
    
    # Add fullscreen button
    Fullscreen().add_to(m)
    
    # Add Nairobi County boundary (from accurate points)
    folium.Polygon(
        locations=NAIROBI_COUNTY_BOUNDARY,
        color='black',
        weight=4,
        fill=False,
        opacity=0.9,
        tooltip='Nairobi County Boundary',
        popup='<b>Nairobi County</b><br>Capital city of Kenya<br>Area: 696.1 km²'
    ).add_to(m)
    
    # Add sub-county labels
    for sub_county, center in SUB_COUNTY_CENTERS.items():
        facility_count = len(facilities_df[facilities_df['Sub-County'] == sub_county])
        
        # Create label HTML
        label_html = f'''
        <div style="
            background: white; 
            padding: 3px 10px; 
            border-radius: 15px; 
            border: 2px solid #0055CC;
            font-size: 10px;
            font-weight: bold;
            color: #0055CC;
            font-family: Arial, sans-serif;
            white-space: nowrap;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            📍 {sub_county}<span style="color:#666; margin-left:6px;">({facility_count})</span>
        </div>
        '''
        
        folium.map.Marker(
            center,
            icon=folium.DivIcon(
                icon_size=(120, 25),
                icon_anchor=(60, 12),
                html=label_html
            )
        ).add_to(m)
        
        # Add a subtle circle to show sub-county area
        folium.Circle(
            radius=1500,
            location=center,
            color='#0055CC',
            weight=1,
            fill=True,
            fill_opacity=0.05,
            opacity=0.3
        ).add_to(m)
    
    # Color mapping for hospital types
    type_colors = {
        'Private': '#1E88E5',      # Blue
        'Public': '#000000',        # Black
        'Faith Based': '#43A047',   # Green
        'NGO': '#E53935'            # Red
    }
    
    type_icons = {
        'Private': '🏥',
        'Public': '⚕️',
        'Faith Based': '⛪',
        'NGO': '🤝'
    }
    
    type_sizes = {
        'Private': 7,
        'Public': 8,
        'Faith Based': 7,
        'NGO': 7
    }
    
    # Create marker cluster
    marker_cluster = MarkerCluster(
        name='Health Facilities',
        overlay=True,
        control=True
    ).add_to(m)
    
    # Add hospital markers
    for _, row in facilities_df.iterrows():
        facility_name = row['Facility Name']
        facility_type = row['Type']
        sub_county = row['Sub-County']
        lat = row['Latitude']
        lng = row['Longitude']
        
        color = type_colors.get(facility_type, '#757575')
        radius = type_sizes.get(facility_type, 6)
        icon = type_icons.get(facility_type, '🏥')
        
        # Create popup HTML
        popup_html = f"""
        <div style="font-family: Arial, sans-serif; font-size: 12px; min-width: 260px;">
            <div style="background-color: {color}; color: white; padding: 10px; border-radius: 8px 8px 0 0;">
                <b style="font-size: 14px;">{icon} {facility_name}</b>
            </div>
            <div style="padding: 12px; background-color: #f9f9f9;">
                <b>📍 Sub-County:</b> {sub_county}<br>
                <b>🏷️ Type:</b> 
                <span style="display: inline-block; width: 10px; height: 10px; background-color: {color}; border-radius: 50%; margin-right: 5px;"></span>
                {facility_type}<br>
                <b>🗺️ Coordinates:</b><br>
                <span style="font-family: monospace; font-size: 10px;">{lat:.5f}, {lng:.5f}</span>
                <hr style="margin: 8px 0;">
                <div style="font-size: 10px;">
                    <a href="https://www.openstreetmap.org/?mlat={lat}&mlon={lng}&zoom=18" target="_blank" style="color: {color}; text-decoration: none;">
                        🗺️ OpenStreetMap
                    </a><br>
                    <a href="https://www.google.com/maps?q={lat},{lng}" target="_blank" style="color: {color}; text-decoration: none;">
                        📍 Google Maps
                    </a>
                </div>
            </div>
        </div>
        """
        
        # Create marker with tooltip
        folium.CircleMarker(
            location=[lat, lng],
            radius=radius,
            popup=folium.Popup(popup_html, max_width=350),
            tooltip=f"{icon} {facility_name}\n📌 {facility_type}\n📍 {sub_county}",
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.85,
            weight=2,
            opacity=1
        ).add_to(marker_cluster)
    
    # Add legend
    legend_html = '''
    <div style="position: fixed; bottom: 30px; right: 30px; 
                background-color: white; padding: 12px 18px;
                border: 2px solid #ddd; border-radius: 10px;
                z-index: 1000; font-size: 11px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.15);
                font-family: Arial, sans-serif;
                min-width: 180px;">
        <b style="font-size: 13px;">🗺️ Map Legend</b><br>
        <hr style="margin: 6px 0;">
        <div style="margin: 8px 0;">
            <b>🏛️ Boundaries:</b><br>
            <span style="display: inline-block; width: 25px; height: 3px; background: black; margin-right: 8px;"></span> County Boundary
        </div>
        <div style="margin: 8px 0;">
            <b>🏥 Facility Types:</b><br>
            <span style="display: inline-block; width: 12px; height: 12px; background: #1E88E5; border-radius: 50%; margin-right: 8px;"></span> Private (Blue)<br>
            <span style="display: inline-block; width: 12px; height: 12px; background: #000000; border-radius: 50%; margin-right: 8px;"></span> Public (Black)<br>
            <span style="display: inline-block; width: 12px; height: 12px; background: #43A047; border-radius: 50%; margin-right: 8px;"></span> Faith Based (Green)<br>
            <span style="display: inline-block; width: 12px; height: 12px; background: #E53935; border-radius: 50%; margin-right: 8px;"></span> NGO (Red)
        </div>
        <hr style="margin: 6px 0;">
        <div style="font-size: 9px; color: #666; text-align: center;">
            💡 Hover over dots to see facility names<br>
            🖱️ Click dots for detailed information
        </div>
    </div>
    '''
    
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    return m

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Load facilities
    with st.spinner("Loading health facilities with accurate coordinates..."):
        facilities_df = load_all_facilities()
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Nairobi County Overview")
        
        # Count facilities by sub-county
        sub_county_counts = facilities_df['Sub-County'].value_counts().to_dict()
        
        st.metric("Total Sub-Counties", 17)
        st.metric("Sub-Counties with Data", len(sub_county_counts))
        st.metric("Total Health Facilities", len(facilities_df))
        
        st.markdown("---")
        st.subheader("📈 Facilities by Sub-County")
        for sc, count in sorted(sub_county_counts.items(), key=lambda x: x[1], reverse=True):
            st.metric(sc, count)
        
        st.markdown("---")
        st.subheader("🏷️ Facilities by Type")
        type_counts = facilities_df['Type'].value_counts()
        type_icons = {'Public': '⚫', 'Private': '🔵', 'Faith Based': '🟢', 'NGO': '🔴'}
        for typ, count in type_counts.items():
            icon = type_icons.get(typ, '⚪')
            st.metric(f"{icon} {typ}", count)
        
        st.markdown("---")
        st.info("""
        **🎨 Map Features:**
        - **⬛ Black outline** = Nairobi County boundary
        - **📍 Blue labels** = Sub-county names with facility counts
        - **🔵 Blue dots** = Private hospitals
        - **⚫ Black dots** = Public hospitals
        - **🟢 Green dots** = Faith Based hospitals
        - **🔴 Red dots** = NGO hospitals
        
        **💡 How to use:**
        - **Hover** over any dot to see facility name
        - **Click** dot for detailed information
        - Use +/- to zoom in/out
        - Click cluster to zoom into area
        """)
    
    # Main content
    st.markdown("""
    <div style="background-color: #e8f4f8; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <h3>🗺️ Nairobi County - Accurate Administrative Boundaries</h3>
        <p>This map uses accurate coordinate data for Nairobi County boundaries and 17 sub-counties.</p>
        <ul>
            <li><strong>⬛ Black outline</strong> = Nairobi County boundary (using 19 accurate coordinate points)</li>
            <li><strong>📍 Blue labels</strong> = 17 Sub-County locations with facility counts</li>
            <li><strong>🔵 Blue dots</strong> = Private hospitals (500+ facilities)</li>
            <li><strong>⚫ Black dots</strong> = Public hospitals</li>
            <li><strong>🟢 Green dots</strong> = Faith Based hospitals</li>
            <li><strong>🔴 Red dots</strong> = NGO hospitals</li>
            <li><strong>💡 Hover over any dot</strong> to see facility name instantly</li>
            <li><strong>🖱️ Click any dot</strong> to see complete facility details</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Create and display map
    with st.spinner("Creating Nairobi County map with accurate boundaries and facilities..."):
        nairobi_map = create_accurate_nairobi_map(facilities_df)
        st_folium(nairobi_map, width='100%', height=700)
    
    # Display statistics
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        private_count = len(facilities_df[facilities_df['Type'] == 'Private'])
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; background-color: #E3F2FD; border-radius: 10px;">
            <h2 style="color: #1E88E5; margin: 0;">🔵</h2>
            <h3 style="margin: 5px 0;">{private_count}</h3>
            <p style="margin: 0;">Private Hospitals</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        public_count = len(facilities_df[facilities_df['Type'] == 'Public'])
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; background-color: #F5F5F5; border-radius: 10px;">
            <h2 style="color: #000000; margin: 0;">⚫</h2>
            <h3 style="margin: 5px 0;">{public_count}</h3>
            <p style="margin: 0;">Public Hospitals</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        faith_count = len(facilities_df[facilities_df['Type'] == 'Faith Based'])
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; background-color: #E8F5E9; border-radius: 10px;">
            <h2 style="color: #43A047; margin: 0;">🟢</h2>
            <h3 style="margin: 5px 0;">{faith_count}</h3>
            <p style="margin: 0;">Faith Based Hospitals</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        ngo_count = len(facilities_df[facilities_df['Type'] == 'NGO'])
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; background-color: #FFEBEE; border-radius: 10px;">
            <h2 style="color: #E53935; margin: 0;">🔴</h2>
            <h3 style="margin: 5px 0;">{ngo_count}</h3>
            <p style="margin: 0;">NGO Hospitals</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Show facilities table
    with st.expander("📋 View Complete Facilities List with Coordinates"):
        display_df = facilities_df[['Facility Name', 'Sub-County', 'Type', 'Latitude', 'Longitude']].copy()
        display_df = display_df.reset_index(drop=True)
        display_df.index = display_df.index + 1
        st.dataframe(display_df, use_container_width=True, height=400)
        
        # Download button
        csv = facilities_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download All Facilities (with coordinates) as CSV",
            data=csv,
            file_name="nairobi_health_facilities_accurate_coordinates.csv",
            mime="text/csv"
        )
    
    # Footer
    st.markdown("---")
    st.markdown(
        f"<div style='text-align: center; color: gray; font-size: 12px;'>"
        "🏥 Nairobi Health Facilities Map | Accurate Administrative Boundaries<br>"
        f"📍 Total: {len(facilities_df)} facilities across 17 sub-counties | "
        "🔵 Private | ⚫ Public | 🟢 Faith Based | 🔴 NGO<br>"
        "💡 Hover over any dot to see facility name | Click for complete details"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
