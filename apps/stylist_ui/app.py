import streamlit as st, requests, os

st.set_page_config(page_title="Essonify Stylist", page_icon="🧥")
st.title("Essonify — Stylist Demo")

API_URL = st.secrets.get("API_URL", os.environ.get("API_URL", "")) or st.text_input("Enter Stylist API URL (onrender.com)", "")

signature = st.selectbox("Signature", ["Classic Sophisticate","Bohemian Nomad","Classic Rebel"])
moment = st.selectbox("Style Moment", ["Boardroom Pitch","Weekend Market","Date Night"])
temp = st.slider("Temp (°F)", 35, 95, 68)
budget = st.selectbox("Budget Tier (optional)", ["","value","mid","premium","luxury"])

if st.button("Recommend") and API_URL:
    payload = {"signature": signature, "style_moment": moment, "temp_f": temp, "precip": False, "budget_tier": budget or None}
    r = requests.post(API_URL.rstrip("/") + "/recommend", json=payload, timeout=30)
    if r.ok:
        data = r.json()
        st.subheader("Top items (MVP)")
        for o in data.get("outfits", []):
            st.markdown(f"- **{o['type']}/{o['subtype']}** — {o['color']} {o['fabric']} (score {o['score']})")
    else:
        st.error(f"{r.status_code}: {r.text}")
