# app.py
"""Streamlit app to explore Uber fare data.

Loads the cleaned dataset (uber_cleaned.csv) and presents key statistics,
visualizations, and an interactive map. Designed for a non‑technical audience
and runs locally.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import plotly.express as px
import os

# Page configuration
st.set_page_config(
    page_title="Uber Fare Explorer",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for premium look (dark mode friendly)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* Hide Streamlit structural branding */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Remove padding around the main block */
    .block-container {
        padding-top: 80px !important;
        padding-bottom: 0rem !important;
    }
    
    /* Push sidebar down to make room for fixed navbar */
    section[data-testid="stSidebar"] {
        top: 64px !important;
        height: calc(100vh - 64px) !important;
    }
    
    /* Dedicated full-width Uber Website Navbar */
    .uber-navbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 64px;
        background-color: #000000;
        z-index: 999999;
        display: flex;
        align-items: center;
        padding: 0 32px;
    }
    .uber-navbar img {
        height: 24px;
        margin-right: 24px;
        filter: brightness(0) invert(1); /* Turns the black logo pure white */
    }
    .uber-navbar-title {
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    </style>
    
    <div class="uber-navbar">
        <img src="https://upload.wikimedia.org/wikipedia/commons/c/cc/Uber_logo_2018.png">
        <span class="uber-navbar-title">Fare Explorer</span>
    </div>
    """,
    unsafe_allow_html=True,
)

@st.cache_data
def load_data():
    df = pd.read_csv("uber_with_clusters.csv") if os.path.exists("uber_with_clusters.csv") else pd.read_csv("uber_cleaned.csv")
    # Ensure proper dtypes (already cleaned in the notebook)
    df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"], errors="coerce")
    if 'cluster' in df.columns:
        df['cluster'] = 'Cluster ' + df['cluster'].astype(str)
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
hour = st.sidebar.slider("Pickup hour", 0, 23, 12)
passenger_options = sorted(df["passenger_count"].unique())
passenger = st.sidebar.multiselect(
    "Passenger count", passenger_options, default=passenger_options
)
apply_map_filters = st.sidebar.checkbox("Apply filters to Maps?", value=True, help="Uncheck this to show ALL trips (all 8 clusters) on the interactive maps, regardless of the time and passenger sliders.")

filtered = df[(df["pickup_datetime"].dt.hour == hour) & (df["passenger_count"].isin(passenger))]
map_df = filtered if apply_map_filters else df

# Custom KPI HTML rendering
kpi_html = f"""
    <div style="display: flex; justify-content: space-between; gap: 20px; margin-bottom: 1.5rem;">
        <div style="flex: 1; background-color: #000000; border-radius: 8px; padding: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.15);">
            <div style="color: #A6A6A6; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">Total Trips</div>
            <div style="color: #FFFFFF; font-size: 30px; font-weight: bold;">{len(filtered):,}</div>
        </div>
        <div style="flex: 1; background-color: #000000; border-radius: 8px; padding: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.15);">
            <div style="color: #A6A6A6; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">Avg Fare</div>
            <div style="color: #FFFFFF; font-size: 30px; font-weight: bold;">${filtered['fare_amount'].mean():.2f}</div>
        </div>
        <div style="flex: 1; background-color: #000000; border-radius: 8px; padding: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.15);">
            <div style="color: #A6A6A6; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">Avg Distance</div>
            <div style="color: #FFFFFF; font-size: 30px; font-weight: bold;">{filtered['distance_km'].mean():.2f} <span style="font-size:18px;">km</span></div>
        </div>
        <div style="flex: 1; background-color: #000000; border-radius: 8px; padding: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.15);">
            <div style="color: #A6A6A6; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">Date Range</div>
            <div style="color: #FFFFFF; font-size: 16px; font-weight: bold; line-height: 1.3;">
                {filtered['pickup_datetime'].min().date()}<br>to {filtered['pickup_datetime'].max().date()}
            </div>
        </div>
    </div>
"""
st.markdown(kpi_html, unsafe_allow_html=True)

# Visualizations
tab1, tab2, tab3 = st.tabs(["Overview & Fares", "Geospatial & Clusters", "Temporal Analysis"])

with tab1:
    st.subheader("Fare & Passenger Analysis")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        fig_hist = px.histogram(filtered, x="fare_amount", nbins=30, title="Fare Distribution")
        st.plotly_chart(fig_hist, width="stretch")
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background-color: #F6F6F6; border-left: 4px solid #000000; padding: 20px; border-radius: 4px;">
            <h4 style="margin-top: 0; color: #000000;">💡 Key Insight</h4>
            <p style="color: #333333; font-size: 15px; line-height: 1.5; margin-bottom: 0;">Most rides are overwhelmingly short-distance trips under $20, with a steep drop-off for expensive fares. This clearly indicates the primary platform use-case is quick inner-city commuting rather than long rural hauls.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<hr style='border:1px solid #E2E2E2;'>", unsafe_allow_html=True)

    col3, col4 = st.columns([2, 1])
    with col3:
        fig_scatter = px.scatter(filtered, x="distance_km", y="fare_amount", opacity=0.5, title="Fare vs. Distance")
        st.plotly_chart(fig_scatter, width="stretch")
    with col4:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background-color: #F6F6F6; border-left: 4px solid #000000; padding: 20px; border-radius: 4px;">
            <h4 style="margin-top: 0; color: #000000;">💡 Key Insight</h4>
            <p style="color: #333333; font-size: 15px; line-height: 1.5; margin-bottom: 0;">While there is a clear linear relationship between distance and fare, striking vertical pricing anomalies exist at 0km. These represent edge-cases like flat-rate tolls, severe gridlocks, or GPS cutouts.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border:1px solid #E2E2E2;'>", unsafe_allow_html=True)
    
    col5, col6 = st.columns([2, 1])
    with col5:
        pass_counts = filtered["passenger_count"].value_counts().reset_index()
        pass_counts.columns = ["Passenger Count", "Trips"]
        fig_bar = px.bar(pass_counts, x="Passenger Count", y="Trips", title="Trips by Passenger Count")
        st.plotly_chart(fig_bar, width="stretch")
    with col6:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background-color: #F6F6F6; border-left: 4px solid #000000; padding: 20px; border-radius: 4px;">
            <h4 style="margin-top: 0; color: #000000;">💡 Key Insight</h4>
            <p style="color: #333333; font-size: 15px; line-height: 1.5; margin-bottom: 0;">Single-passenger trips completely dominate the dataset by raw volume, highlighting that solo point-to-point transportation is the absolute core lifeblood of the platform's revenue.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border:1px solid #E2E2E2;'>", unsafe_allow_html=True)
    
    col7, col8 = st.columns([2, 1])
    with col7:
        fig_box = px.box(filtered, x='passenger_count', y='fare_amount', title='Fare Distribution by Passenger Count')
        st.plotly_chart(fig_box, width="stretch")
    with col8:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background-color: #F6F6F6; border-left: 4px solid #000000; padding: 20px; border-radius: 4px;">
            <h4 style="margin-top: 0; color: #000000;">💡 Key Insight</h4>
            <p style="color: #333333; font-size: 15px; line-height: 1.5; margin-bottom: 0;">Surprisingly, the median fare does not drastically increase for larger passenger counts, implying larger vehicles are fundamentally booked for identical trip lengths as solo sedans.</p>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.subheader("Pickup Locations & Clusters")
    
    if 'cluster' in df.columns:
        with st.expander("Show Cluster Characteristics (Average Values)"):
            cluster_summary = df.groupby('cluster')[['distance_km', 'fare_amount', 'pickup_hour', 'passenger_count']].mean().round(2)
            st.dataframe(cluster_summary, use_container_width=True)
            st.markdown('''
            **What do these clusters actually mean?**
            By mathematically analyzing the multi-dimensional dataset (Distance, Fare, Passenger Count, Weekends, and Rush Hour flags), the K-Means algorithm effectively broke the trips into these profiles:
            
            - **Cluster 0: Long-Distance / Airport Runs.** Exceptionally high average distance (~16km) and high fares (~$42).
            - **Cluster 1: Standard Weekday Trips.** Typical daytime trips occurring entirely outside of peak traffic.
            - **Cluster 2: Weekend Rush-Hour.** Trips taking place strictly during busy weekend peak traffic hours. *(The calculated timeframe appears as mid-day because the algorithmic average simply splits the difference between the distinct morning and evening rush hour spikes).*
            - **Cluster 3: Standard Weekend Trips.** Normal trips reliably happening on weekends outside of rush hour.
            - **Cluster 4: High Passenger / SUV Trips.** Standard metrics, but strictly large groups (averaging 5 passengers).
            - **Cluster 5: GPS / Fare Anomalies.** Micro distances (~0.2km) but massive fares (~$47). The algorithm quarantined these mathematical edge-cases (likely GPS cut-outs, severe gridlock, or flat-rate tolls) into their own distinct group.
            - **Cluster 6: Weekday Rush-Hour Commutes.** Trips taking place strictly during weekday peak traffic. *(Similar to Cluster 2, the average time shows ~1:00 PM due solely to mathematically averaging morning and evening commutes together).*
            - **Cluster 7: Late-Night "Party" Trips.** Occurring almost exclusively incredibly late at night (averaging 2:00 AM).
            
            *Use the interactive tabs and maps below to visually explore these groups by filtering!*
            ''')
            
        col_c1, col_c2 = st.columns([2, 1])
        with col_c1:
            fig_cluster = px.scatter(
                map_df, x='pickup_longitude', y='pickup_latitude', color='cluster',
                title='Pickup locations colored by cluster', hover_data=['fare_amount', 'distance_km'],
                height=500
            )
            fig_cluster.update_layout(margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_cluster, width="stretch")
        with col_c2:
            st.markdown("<br><br><br><br>", unsafe_allow_html=True)
            st.markdown("""
            <div style="background-color: #F6F6F6; border-left: 4px solid #000000; padding: 20px; border-radius: 4px;">
                <h4 style="margin-top: 0; color: #000000;">💡 Key Insight</h4>
                <p style="color: #333333; font-size: 15px; line-height: 1.5; margin-bottom: 0;">The K-Means algorithm effectively carves harsh geographical segmentations purely based on pricing and time parameters. We can visibly see distinct "zones" corresponding to localized rider behaviors.</p>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<hr style='border:1px solid #E2E2E2;'>", unsafe_allow_html=True)
            
        col_m1, col_m2 = st.columns([2, 1])
        with col_m1:
            fig_map = px.scatter_mapbox(
                map_df, lat='pickup_latitude', lon='pickup_longitude', color='cluster',
                size='fare_amount', hover_data=['fare_amount', 'distance_km'], zoom=10,
                title='Pickup Location Density Map', mapbox_style="open-street-map",
                height=500
            )
            fig_map.update_layout(margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_map, width="stretch")
        with col_m2:
            st.markdown("<br><br><br><br>", unsafe_allow_html=True)
            st.markdown("""
            <div style="background-color: #F6F6F6; border-left: 4px solid #000000; padding: 20px; border-radius: 4px;">
                <h4 style="margin-top: 0; color: #000000;">💡 Key Insight</h4>
                <p style="color: #333333; font-size: 15px; line-height: 1.5; margin-bottom: 0;">This heatmap vividly underscores a massive structural volume concentration deeply centered around the business district hubs, which rapidly dissipates into nothingness moving toward the peripheral outer limits.</p>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.write('Cluster column not available in the data.')
        map_data = map_df[["pickup_latitude", "pickup_longitude"]].rename(
            columns={"pickup_latitude": "lat", "pickup_longitude": "lon"}
        )
        st.map(map_data)

with tab3:
    col_t1, col_t2 = st.columns([2, 1])
    with col_t1:
        # Trips per hour
        hour_counts = filtered['pickup_datetime'].dt.hour.value_counts().reset_index()
        hour_counts.columns = ["Hour of Day", "Number of Trips"]
        fig_hour = px.bar(hour_counts, x="Hour of Day", y="Number of Trips", title="Trips per Hour")
        st.plotly_chart(fig_hour, width="stretch")
    with col_t2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background-color: #F6F6F6; border-left: 4px solid #000000; padding: 20px; border-radius: 4px;">
            <h4 style="margin-top: 0; color: #000000;">💡 Key Insight</h4>
            <p style="color: #333333; font-size: 15px; line-height: 1.5; margin-bottom: 0;">The raw temporal throughput reveals a starkly bimodal demand curve. Volumes begin softly surging into the morning commute, steadily climb, and massively erupt into a dominant peak during the evening rush hour exits.</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Data source: cleaned Uber dataset generated in the notebook.")
