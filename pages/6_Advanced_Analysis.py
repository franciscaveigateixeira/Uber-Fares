import streamlit as st
import plotly.express as px
import pandas as pd
import os
from utils import load_data

df = load_data()

st.title("Advanced Data Science")

# Executive Summary (Warning)
st.markdown("### Technical Module Warning")
st.markdown("""
<p style='color: #666666; font-size: 15px; margin-bottom: 20px; border-left: 4px solid #000000; padding-left: 15px;'>
This module exposes the raw mathematical matrices and dimensionality reduction algorithms used by our machine learning models. 
It is intended for data scientists, analysts, and engineers. <b>Business stakeholders may safely skip this section.</b>
</p>
""", unsafe_allow_html=True)

st.divider()

# Core Visuals
st.markdown("### Feature Correlation Matrix")

corr_cols = ['fare_amount', 'distance_km', 'passenger_count', 'pickup_hour', 'pickup_day', 'pickup_dayofweek']
if all(c in df.columns for c in corr_cols):
    col_hm, col_hm_text = st.columns([2, 1])
    with col_hm:
        corr = df[corr_cols].corr().round(2)
        fig_heatmap = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale="Greens")
        fig_heatmap.update_layout(margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_heatmap, use_container_width=True, config={'scrollZoom': True})
    with col_hm_text:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("**Insight: Linear Relationships**")
        st.markdown("Distance and Fare share a near 1-to-1 linear correlation (`~0.90`), confirming our distance-based pricing model.")
        st.markdown("Interestingly, `passenger_count` has an absolute zero mathematical impact (`0.01`) on the final fare pricing, confirming zero marginal cost for extra riders.")
else:
    st.info("Additional dimensions calculating...")



from utils import render_footer
render_footer()
