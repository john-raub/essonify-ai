import streamlit as st, requests, os

st.set_page_config(page_title="Essonify Avatar", page_icon="🧍")
st.title("Essonify — Avatar Demo")

API_URL = st.secrets.get("API_URL", os.environ.get("API_URL", "")) or st.text_input("Enter Avatar API URL (onrender.com)", "")

signature = st.selectbox("Signature", ["Classic Sophisticate","Bohemian Nomad","Classic Rebel"])
moment = st.selectbox("Style Moment", ["Boardroom Pitch","Weekend Market","Date Night"])
presentation = st.selectbox("Presentation", ["Femme","Masc"])
season = st.selectbox("Season", ["Spring","Summer","Fall","Winter"])
palette = st.text_input("Palette (optional)", "Latte Warm")

if st.button("Build Avatar State") and API_URL:
    payload = {"signature": signature, "style_moment": moment, "presentation": presentation, "season": season, "palette": palette}
    r = requests.post(API_URL.rstrip("/") + "/state", json=payload, timeout=30)
    if r.ok:
        data = r.json().get("avatar", {})
        st.json(data)
    else:
        st.error(f"{r.status_code}: {r.text}")
