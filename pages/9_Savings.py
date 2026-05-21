import streamlit as st
from utils import render_footer

st.set_page_config(
    page_title="Passenger Savings & Hacks",
    page_icon="uber_logo.jpg",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<div style="padding: 10px;">
<h1 style="margin-top: 0; color: #000000; font-size: 48px; font-weight: 800; letter-spacing: -1.5px; margin-bottom: 10px;">Passenger Savings & Smart Hacks</h1>
<p style="color: #666666; font-size: 20px; line-height: 1.5; margin-bottom: 40px;">
Exclusive analytical insights designed specifically for Uber passengers to avoid dynamic multipliers, optimize commute times, and unlock maximum direct savings across New York City.
</p>
</div>
""", unsafe_allow_html=True)

# Check if the user just registered as an Uber User to unlock their premium first-time discount!
if st.session_state.get('just_registered', False) and st.session_state.get('user_type', '') == 'Uber User':
    import base64
    import os
    voucher_b64 = ""
    for ext in ['jpg', 'png', 'jpeg']:
        if os.path.exists(f"voucher.{ext}"):
            with open(f"voucher.{ext}", "rb") as img_file:
                voucher_b64 = base64.b64encode(img_file.read()).decode()
            break
            
    st.balloons() # Celebrating their welcome gift!
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #06C167, #048648); color: #ffffff; border-radius: 16px; padding: 35px; box-shadow: 0 10px 30px rgba(6,193,103,0.15); margin-bottom: 40px; text-align: center; font-family: sans-serif;">
        <h2 style="margin-top:0; font-size:32px; font-weight:800; letter-spacing:-1px; color:#ffffff;">Exclusive Welcome Gift Unlocked!</h2>
        <p style="font-size:18px; opacity:0.95; margin-bottom:25px; color:#ffffff;">Since this is your first time registering as a passenger, you have received a <b>10% OFF Voucher</b>! Check your email inbox or use the promo code below:</p>
        <div style="display:inline-block; background:#ffffff; color:#000000; font-size:24px; font-weight:800; padding:12px 30px; border-radius:8px; letter-spacing:2px; margin-bottom:25px; box-shadow:0 4px 10px rgba(0,0,0,0.1); text-transform:uppercase;">
            kikacarlota10
        </div>
        {"<div style='margin: 0 auto; max-width: 450px; border-radius: 12px; overflow: hidden; box-shadow: 0 8px 24px rgba(0,0,0,0.25);'><img src='data:image/jpeg;base64," + voucher_b64 + "' style='width: 100%; display: block;' /></div>" if voucher_b64 else ""}
    </div>
    """, unsafe_allow_html=True)

# 3 Beautiful Glassmorphism Cards for the Savings Hacks
st.markdown("""
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 30px; padding: 10px; margin-bottom: 60px;">

<div style="background: #ffffff; border: 1px solid #E2E8F0; border-radius: 16px; padding: 32px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); border-top: 6px solid #0ea5e9;">
<div style="font-size: 14px; font-weight: 800; text-transform: uppercase; color: #0ea5e9; letter-spacing: 1.5px; margin-bottom: 12px;">Timing Hack</div>
<h3 style="font-size: 24px; font-weight: 700; color: #0f172a; margin-top: 0; margin-bottom: 16px;">The 15-Minute Golden Window</h3>
<p style="color: #475569; font-size: 16px; line-height: 1.7; margin-bottom: 24px;">
Requesting a ride just <b>15 minutes before</b> standard rush hour peaks (e.g. 4:45 PM instead of 5:00 PM) or waiting 20 minutes after late-night venues close drops average fare multipliers significantly.
</p>
<div style="background: #f8fafc; padding: 16px 20px; border-radius: 10px; border-left: 4px solid #0ea5e9;">
<div style="font-size: 28px; font-weight: 800; color: #0ea5e9;">22% – 35%</div>
<div style="font-size: 13px; color: #64748b; font-weight: 600; text-transform: uppercase;">Average Direct Fare Reduction</div>
</div>
</div>

<div style="background: #ffffff; border: 1px solid #E2E8F0; border-radius: 16px; padding: 32px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); border-top: 6px solid #0ea5e9;">
<div style="font-size: 14px; font-weight: 800; text-transform: uppercase; color: #0ea5e9; letter-spacing: 1.5px; margin-bottom: 12px;">Airport Commute</div>
<h3 style="font-size: 24px; font-weight: 700; color: #0f172a; margin-top: 0; margin-bottom: 16px;">JFK & LaGuardia Parity Strategy</h3>
<p style="color: #475569; font-size: 16px; line-height: 1.7; margin-bottom: 24px;">
Fixed upfront pricing shields passengers from unpredictable bridge and tunnel traffic congestion compared to traditional metered cabs. For groups of 3 to 4 passengers, splitting an <b>UberXL</b> provides the lowest per-person cost.
</p>
<div style="background: #f8fafc; padding: 16px 20px; border-radius: 10px; border-left: 4px solid #0ea5e9;">
<div style="font-size: 28px; font-weight: 800; color: #0ea5e9;">Upfront Lock</div>
<div style="font-size: 13px; color: #64748b; font-weight: 600; text-transform: uppercase;">100% Protection from Meter Inflation</div>
</div>
</div>

<div style="background: #ffffff; border: 1px solid #E2E8F0; border-radius: 16px; padding: 32px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); border-top: 6px solid #0ea5e9;">
<div style="font-size: 14px; font-weight: 800; text-transform: uppercase; color: #0ea5e9; letter-spacing: 1.5px; margin-bottom: 12px;">Weather Surge Predictor</div>
<h3 style="font-size: 24px; font-weight: 700; color: #0f172a; margin-top: 0; margin-bottom: 16px;">The 2-Block Rain Rule</h3>
<p style="color: #475569; font-size: 16px; line-height: 1.7; margin-bottom: 24px;">
Sudden rain triggers localized dynamic pricing spikes directly outside major transit hubs like Penn Station and Grand Central. Walking just <b>two blocks away</b> from primary avenues bypasses the localized surge geofence entirely.
</p>
<div style="background: #f8fafc; padding: 16px 20px; border-radius: 10px; border-left: 4px solid #0ea5e9;">
<div style="font-size: 28px; font-weight: 800; color: #0ea5e9;">€8 – €15</div>
<div style="font-size: 13px; color: #64748b; font-weight: 600; text-transform: uppercase;">Savings per Trip during Rain</div>
</div>
</div>

</div>
""", unsafe_allow_html=True)

render_footer()
