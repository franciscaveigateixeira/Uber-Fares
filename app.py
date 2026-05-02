import streamlit as st
from utils import inject_custom_css

# This must be the very first Streamlit command
st.set_page_config(
    page_title="Uber Fare Explorer",
    page_icon="uber_logo.jpg",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Inject the global CSS and Top Navbar onto every page
inject_custom_css()

# Explicitly define the pages and their exact URL paths
p_home = st.Page("pages/0_Home.py", title="Home", url_path="home", default=True)
p1 = st.Page("pages/1_Distributions.py", title="Distributions", url_path="distributions")
p2 = st.Page("pages/2_Temporal_Analysis.py", title="Temporal Analysis", url_path="temporal-analysis")
p3 = st.Page("pages/3_Segment_Encyclopedia.py", title="Segment Encyclopedia", url_path="segment-encyclopedia")
p4 = st.Page("pages/4_Geospatial_Hub.py", title="Geospatial Hub", url_path="geospatial-hub")
p5 = st.Page("pages/5_Advanced_Analysis.py", title="Advanced Analysis", url_path="advanced-analysis")
p6 = st.Page("pages/6_Business_Strategy.py", title="Business Strategy", url_path="business-strategy")
p7 = st.Page("pages/7_Ride_Simulator.py", title="Ride Simulator", url_path="ride-simulator")

# Run the router and completely hide the default sidebar menu
pg = st.navigation([p_home, p1, p2, p3, p4, p5, p6, p7], position="hidden")
pg.run()
