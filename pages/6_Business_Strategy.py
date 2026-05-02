import streamlit as st
import plotly.express as px
import pandas as pd
import pydeck as pdk
from utils import load_data

df = load_data()

st.title("Actionable Business Strategies")

# Executive Summary
st.markdown("### Executive Summary")

kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric(label="Actionable Strategies", value="3")
with kpi2:
    st.metric(label="Primary Growth Driver", value="Dynamic Pricing")
with kpi3:
    st.metric(label="Primary Cost Saver", value="Fleet Routing")

st.markdown("""
> **Tip:** Keep an eye out for targeted UberXL discounts if you're traveling with your family, or special flat rates if you're a solo commuter! The platform uses these analytical profiles to offer you the best possible deals based on exactly how you travel.
""")

st.divider()

st.markdown("### Strategic Implementation Plan")
st.markdown("<br>", unsafe_allow_html=True)

if 'cluster' in df.columns:
    # STRATEGY 1: Route & Fleet Optimization
    col_b1, col_b2 = st.columns([1, 1.5])
    with col_b1:
        st.markdown("""
        <div style="background-color: #F6F6F6; border-top: 6px solid #06C167; padding: 30px; border-radius: 8px; height: 100%;">
            <h3 style="color: #000000; font-size: 24px; margin-top: 0; margin-bottom: 20px;">1. Route & Fleet Optimization</h3>
            <p style="color: #333333; font-size: 18px; line-height: 1.6; margin-bottom: 20px;"><b>How to use the data:</b> How do we know the automated logic actually found the airports? <br><br>Compare the two maps on the right perfectly. The <b>Top Map</b> is a basic physical reference of where the NYC airports are. <br><br>The <b>Bottom Map</b> is the raw mathematical Cluster data (the green dots). Notice how the algorithm perfectly grew outward and autonomously mapped itself precisely to those three distinct airport zones without any human tags.</p>
            <div style="background-color: #E2E2E2; height: 2px; width: 100%; margin: 20px 0;"></div>
            <strong style="color: #000000; font-size: 16px; text-transform: uppercase; letter-spacing: 0.5px;">✓ Direct Impact</strong>
            <p style="color: #333333; font-size: 16px; line-height: 1.6; margin-top: 10px; margin-bottom: 0;">Dispatch algorithms can pre-position idle cars exactly at JFK <i>before</i> flights land to dramatically reduce empty driver miles.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_b2:
        icon_url = "https://img.icons8.com/m_sharp/200/000000/airport.png"
        airport_df = pd.DataFrame({
            'Name': ['JFK Airport', 'Newark Airport', 'LaGuardia'],
            'lat': [40.6413, 40.6895, 40.7769],
            'lon': [-73.7781, -74.1745, -73.8740]
        })
        icon_data = {
            "url": icon_url,
            "width": 200,
            "height": 200,
            "anchorY": 200,
        }
        airport_df['icon_data'] = [icon_data for _ in range(len(airport_df))]

        icon_layer = pdk.Layer(
            "IconLayer",
            data=airport_df,
            get_icon="icon_data",
            get_size=150,
            size_scale=1,
            get_position="[lon, lat]",
            pickable=True,
            get_color="[0, 0, 0, 255]"
        )

        view_state = pdk.ViewState(
            latitude=40.71,
            longitude=-73.97,
            zoom=8.5,
            pitch=0,
        )

        st.markdown("#### Reference: New York City Airports")
        st.pydeck_chart(pdk.Deck(
            layers=[icon_layer],
            initial_view_state=view_state,
            tooltip={"text": "{Name}"},
            map_style="light"
        ))
        
        c0_df = df[df['cluster'] == "0: Airport / Long-Distance"].copy()
        c0_df['Label'] = 'Automated Cluster 0 (The Green Dots)'
        fig_air = px.scatter_mapbox(
            c0_df, lat='pickup_latitude', lon='pickup_longitude', color='Label',
            title='Proof: Strategic Airport Runs', mapbox_style="carto-positron",
            color_discrete_sequence=["#06C167"], height=250, opacity=0.3
        )
        fig_air.update_layout(margin=dict(l=0, r=0, t=40, b=10))
        st.plotly_chart(fig_air, use_container_width=True)
        
    st.markdown("<br><hr style='border:1px solid #E2E2E2;'><br>", unsafe_allow_html=True)

    # STRATEGY 2: Dynamic Pricing
    col_b3, col_b4 = st.columns([1.5, 1])
    with col_b3:
        cnumber = "7: Late-Night Party"
        c7_df = df[df['cluster'] == cnumber].copy()
        c7_demand = c7_df.groupby(c7_df['pickup_datetime'].dt.hour)['fare_amount'].count().reset_index()
        c7_demand.columns = ['Hour of Day', 'Total Nightlife Trips']
        fig_price = px.bar(c7_demand, x='Hour of Day', y='Total Nightlife Trips', title="1. Time: The 'Nightclub Surge' Peak (2:00 AM)", color_discrete_sequence=["#000000"])
        fig_price.update_layout(height=250, margin=dict(l=0, r=0, t=40, b=0), xaxis=dict(tickmode='linear', tick0=0, dtick=1))
        st.plotly_chart(fig_price, use_container_width=True)

        c7_df['Label'] = 'Nightclubs / Entertainment Districts'
        fig_night_map = px.scatter_mapbox(
            c7_df, lat='pickup_latitude', lon='pickup_longitude', color='Label',
            title='2. Geography: Deep Urban Hotspots', mapbox_style="carto-positron",
            color_discrete_sequence=["#06C167"], height=350, opacity=0.8
        )
        fig_night_map.update_layout(margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig_night_map, use_container_width=True)
    with col_b4:
        st.markdown("""
        <div style="background-color: #F6F6F6; border-top: 6px solid #000000; padding: 30px; border-radius: 8px; height: 100%;">
            <h3 style="color: #000000; font-size: 24px; margin-top: 0; margin-bottom: 20px;">2. Surgical Dynamic Pricing</h3>
            <p style="color: #333333; font-size: 18px; line-height: 1.6; margin-bottom: 20px;"><b>How to use the data:</b> Look at the bar chart isolating the "Nightlife" cluster. There is an unmistakable, explosive spike right between 1:00 AM and 3:00 AM—this perfectly matches the time nightclubs close in Downtown Manhattan and Brooklyn.</p>
            <div style="background-color: #E2E2E2; height: 2px; width: 100%; margin: 20px 0;"></div>
            <strong style="color: #000000; font-size: 16px; text-transform: uppercase; letter-spacing: 0.5px;">✓ Direct Impact</strong>
            <p style="color: #333333; font-size: 16px; line-height: 1.6; margin-top: 10px; margin-bottom: 0;">Instead of turning practically all of NY into a "surge zone", we can literally geo-fence high prices instantly onto nightclub strips at 2:00 AM to capitalize on highly urgent, nightlife demand.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br><hr style='border:1px solid #E2E2E2;'><br>", unsafe_allow_html=True)

    # STRATEGY 3: Hyper-Targeted Marketing
    col_b5, col_b6 = st.columns([1, 1.5])
    with col_b5:
        st.markdown("""
        <div style="background-color: #F6F6F6; border-top: 6px solid #333333; padding: 30px; border-radius: 8px; height: 100%;">
            <h3 style="color: #000000; font-size: 24px; margin-top: 0; margin-bottom: 20px;">3. Target Marketing Demographics</h3>
            <p style="color: #333333; font-size: 18px; line-height: 1.6; margin-bottom: 20px;"><b>How to use the data:</b> When you compare the <b>Large Vehicle users</b> against <b>Solo Commuters</b>, the passenger counts are fundamentally different (almost 5-to-1). They require vastly different advertising approaches.</p>
            <div style="background-color: #E2E2E2; height: 2px; width: 100%; margin: 20px 0;"></div>
            <strong style="color: #000000; font-size: 16px; text-transform: uppercase; letter-spacing: 0.5px;">✓ Direct Impact</strong>
            <p style="color: #333333; font-size: 16px; line-height: 1.6; margin-top: 10px; margin-bottom: 0;">We can push 'UberXL' discounts purely to family demographic user IDs, while offering 'Business Commuter' flat rates specifically to the solo commuters.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_b6:
        c14_df = df[df['cluster'].isin(["1: Standard Weekday", "4: High Passenger / SUV"])].copy()
        c14_df['Profile'] = c14_df['cluster'].map({"1: Standard Weekday": 'Solo Commuters', "4: High Passenger / SUV": 'Families / Group SUV'})
        c14_avg = c14_df.groupby('Profile')['passenger_count'].mean().reset_index()
        fig_market = px.bar(c14_avg, x='Profile', y='passenger_count', title="Demographic Targeting by Avg. Passengers", color_discrete_sequence=["#06C167", "#333333"])
        fig_market.update_layout(height=500, margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig_market, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Deep Dive
    with st.expander("🔍 Advanced Analytics & Deep Dive", expanded=False):
        st.markdown("Understand the mathematical methodology behind the strategic implementations.")
        st.markdown("""
        <div style="background-color: #E8F5E9; border-left: 6px solid #06C167; padding: 25px; border-radius: 6px; margin-bottom: 35px;">
            <p style="color: #333333; font-size: 20px; line-height: 1.6; margin-bottom: 0;">
                <b style="font-size: 22px;">Wait, what is a "Smart Segment"?</b><br>
                A segment is simply a mathematically generated group of trips that share identical real-world behaviors (such as traveling extremely long distances, or happening exclusively late at night in specific neighborhoods). By isolating these specific groups, we can physically see exactly where and when our business strategies should be deployed.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
else:
    st.info("Cluster data is required to view these insights. Please ensure you are loading 'uber_with_clusters.csv'.")


from utils import render_footer
render_footer()
