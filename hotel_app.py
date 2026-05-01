import streamlit as st
import pandas as pd
import pickle

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Hotel Cancellation Predictor",
    page_icon="🏨",
    layout="wide"
)

# ─── Custom CSS (hotel image palette: teal/sage walls, cream ceiling, gold frame) ─
st.markdown("""
<style>
  /* Import elegant font */
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500&display=swap');

  /* Root palette — dark version of the hotel image */
  :root {
    --bg:      #0E1A1B;
    --surface: #152324;
    --card:    #1C2F30;
    --teal:    #4A7C7E;
    --teal-dk: #2F5657;
    --teal-lt: #6FA3A5;
    --gold:    #C9A84C;
    --gold-lt: #E8C96A;
    --text:    #EDE8DC;
    --muted:   #8FAAAB;
    --border:  #2A4142;
  }

  /* Background */
  .stApp {
    background-color: var(--bg) !important;
  }
  section[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
  }

  /* Remove default streamlit padding */
  .block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
  }

  /* Typography */
  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: var(--text);
  }

  /* All labels and text bright */
  p, span, div, label {
    color: var(--text) !important;
  }

  /* ── Header sign ── */
  .hotel-sign {
    background: #F5F0E8;
    border: 4px solid var(--gold);
    border-radius: 8px;
    text-align: center;
    padding: 18px 40px 14px;
    margin: 0 auto 32px;
    display: inline-block;
    width: 100%;
    box-shadow: 0 4px 32px rgba(201,168,76,0.25), 0 2px 8px rgba(0,0,0,0.4);
    position: relative;
  }
  .hotel-sign::before, .hotel-sign::after {
    content: '';
    position: absolute;
    top: -18px;
    width: 8px;
    height: 18px;
    background: var(--gold);
    border-radius: 2px 2px 0 0;
  }
  .hotel-sign::before { left: 28%; }
  .hotel-sign::after  { right: 28%; }

  .hotel-sign h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.4rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.18em !important;
    color: #1E2D2F !important;
    margin: 0 !important;
    padding: 0 !important;
  }
  .hotel-sign p {
    font-size: 0.85rem;
    color: #607D7E !important;
    margin: 4px 0 0;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }

  /* ── Section headers ── */
  .section-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--gold-lt) !important;
    border-left: 4px solid var(--gold);
    padding-left: 12px;
    margin: 28px 0 16px;
    letter-spacing: 0.03em;
  }

  /* ── Form inputs ── */
  .stSelectbox label, .stNumberInput label, .stSlider label {
    font-weight: 500;
    font-size: 0.85rem;
    color: var(--teal-lt) !important;
    letter-spacing: 0.02em;
    text-transform: uppercase;
  }
  div[data-baseweb="select"] > div {
    background-color: var(--card) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
  }
  div[data-baseweb="select"] > div:focus-within {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 2px rgba(201,168,76,0.2) !important;
  }
  div[data-baseweb="select"] span {
    color: var(--text) !important;
  }
  input[type="number"] {
    background-color: var(--card) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
  }
  /* Dropdown menu */
  ul[data-baseweb="menu"] {
    background-color: var(--card) !important;
  }
  li[role="option"] {
    background-color: var(--card) !important;
    color: var(--text) !important;
  }
  li[role="option"]:hover {
    background-color: var(--teal-dk) !important;
  }

  /* ── Predict button ── */
  div.stButton > button {
    background: linear-gradient(135deg, var(--teal) 0%, var(--teal-dk) 100%) !important;
    color: white !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px 0 !important;
    width: 100% !important;
    box-shadow: 0 4px 16px rgba(47,86,87,0.35) !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
    margin-top: 8px !important;
  }
  div.stButton > button:hover {
    background: linear-gradient(135deg, var(--gold) 0%, var(--gold-lt) 100%) !important;
    color: var(--text) !important;
    box-shadow: 0 6px 20px rgba(201,168,76,0.4) !important;
    transform: translateY(-1px) !important;
  }

  /* ── Result cards ── */
  .result-card {
    border-radius: 14px;
    padding: 28px 32px;
    text-align: center;
    margin-top: 28px;
    box-shadow: 0 6px 28px rgba(0,0,0,0.10);
  }
  .result-will-cancel {
    background: linear-gradient(135deg, #8B2E2E 0%, #B03A3A 100%);
    color: white;
  }
  .result-will-stay {
    background: linear-gradient(135deg, var(--teal-dk) 0%, var(--teal) 100%);
    color: white;
  }
  .result-card .result-icon { font-size: 3rem; margin-bottom: 6px; }
  .result-card .result-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    margin: 8px 0 4px;
  }
  .result-card .result-prob {
    font-size: 1rem;
    opacity: 0.85;
  }
  .result-card .result-advice {
    font-size: 0.82rem;
    opacity: 0.75;
    margin-top: 10px;
    font-style: italic;
  }

  /* ── Metrics ── */
  div[data-testid="metric-container"] {
    background-color: var(--card) !important;
    border: 1px solid var(--gold) !important;
    border-radius: 10px !important;
    padding: 12px 16px !important;
  }
  div[data-testid="metric-container"] label {
    color: var(--gold-lt) !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    color: var(--text) !important;
    font-size: 1.8rem !important;
    font-family: 'Playfair Display', serif !important;
  }

  /* ── Divider ── */
  hr { border-color: var(--border); }

  /* ── Expander ── */
  details > summary {
    color: var(--gold-lt) !important;
    font-weight: 500;
  }
  details {
    background-color: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
  }
</style>
""", unsafe_allow_html=True)

# ─── Load Model ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    with open("hotel_model.pkl", "rb") as f:
        return pickle.load(f)

try:
    data = load_model()
    model = data["model"]
    MODEL_LOADED = True
except Exception as e:
    MODEL_LOADED = False
    st.error(f"⚠️ Could not load model: {e}")

# ─── Header Sign ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hotel-sign">
  <h1>HOTEL</h1>
  <p>Booking Cancellation Predictor</p>
</div>
""", unsafe_allow_html=True)

# ─── Form — 3 equal columns ────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="section-header">🏨 Booking Info</div>', unsafe_allow_html=True)
    hotel          = st.selectbox("Hotel Type",     ["City Hotel", "Resort Hotel"])
    arrival_month  = st.selectbox("Arrival Month",  [
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ])
    arrival_day    = st.number_input("Arrival Day",       min_value=1,   max_value=31,  value=15)
    lead_time      = st.number_input("Lead Time (days)",  min_value=0,   max_value=730, value=30)
    deposit_type   = st.selectbox("Deposit Type",   ["No Deposit", "Non Refund", "Refundable"])
    market_segment = st.selectbox("Market Segment", [
        "Online TA","Offline TA/TO","Direct","Corporate","Groups","Complementary","Aviation"
    ])
    customer_type  = st.selectbox("Customer Type",  ["Transient","Transient-Party","Contract","Group"])

with col2:
    st.markdown('<div class="section-header">👥 Guests & Stay</div>', unsafe_allow_html=True)
    adults         = st.number_input("Adults",          min_value=0, max_value=10, value=2)
    children       = st.number_input("Children",        min_value=0, max_value=10, value=0)
    babies         = st.number_input("Babies",          min_value=0, max_value=10, value=0)
    weekend_nights = st.number_input("Weekend Nights",  min_value=0, max_value=20, value=1)
    week_nights    = st.number_input("Week Nights",     min_value=0, max_value=30, value=3)
    adr            = st.number_input("ADR (€/night)",   min_value=0.0, max_value=1000.0, value=100.0, step=5.0)

    # ── Live summary metrics ──
    total_guests_live = adults + children + babies
    total_stay_live   = weekend_nights + week_nights
    st.markdown("<br>", unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    m1.metric("👥 Total Guests",     total_guests_live)
    m2.metric("🌙 Total Stay Nights", total_stay_live)

with col3:
    st.markdown('<div class="section-header">📋 Room & History</div>', unsafe_allow_html=True)
    meal                      = st.selectbox("Meal Plan",   ["BB","HB","FB","SC"])
    reserved_room_type        = st.selectbox("Room Type",   ["A","B","C","D","E","F","G","H","L","P"])
    country                   = st.selectbox("Country",     ["PRT","GBR","FRA","ESP","DEU","IRL","ITA","NLD","BEL","BRA","Other"])
    booking_changes           = st.number_input("Booking Changes",      min_value=0, max_value=20,  value=0)
    special_requests          = st.number_input("Special Requests",     min_value=0, max_value=10,  value=0)
    days_in_waiting_list      = st.number_input("Days in Waiting List", min_value=0, max_value=400, value=0)
    is_repeated_guest         = st.selectbox("Repeated Guest?",             ["No","Yes"])
    had_previous_cancellation = st.selectbox("Had Previous Cancellation?",  ["No","Yes"])
    room_class_changed        = st.selectbox("Room Class Changed?",         ["No","Yes"])

# ─── Predict Button ────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
predict_clicked = st.button("✦  Predict Cancellation  ✦")

# ─── Prediction Logic ──────────────────────────────────────────────────────────
if predict_clicked:
    if not MODEL_LOADED:
        st.error("Model not loaded. Please check the model file.")
    else:
        total_stay   = total_stay_live
        total_guests = total_guests_live

        input_df = pd.DataFrame([{
            "hotel":                     hotel,
            "lead_time":                 lead_time,
            "arrival_date_month":        arrival_month,
            "arrival_date_day_of_month": arrival_day,
            "stays_in_weekend_nights":   weekend_nights,
            "stays_in_week_nights":      week_nights,
            "adults":                    adults,
            "children":                  children,
            "babies":                    babies,
            "meal":                      meal,
            "country":                   country,
            "market_segment":            market_segment,
            "is_repeated_guest":         1 if is_repeated_guest == "Yes" else 0,
            "reserved_room_type":        reserved_room_type,
            "booking_changes":           booking_changes,
            "deposit_type":              deposit_type,
            "days_in_waiting_list":      days_in_waiting_list,
            "customer_type":             customer_type,
            "adr":                       adr,
            "total_of_special_requests": special_requests,
            "total_stay":                total_stay,
            "total_guests":              total_guests,
            "had_previous_cancellation": 1 if had_previous_cancellation == "Yes" else 0,
            "room_class_changed":        1 if room_class_changed == "Yes" else 0,
        }])

        prediction = model.predict(input_df)[0]
        proba      = model.predict_proba(input_df)[0]
        cancel_pct = round(proba[1] * 100, 1)
        stay_pct   = round(proba[0] * 100, 1)

        if prediction == 1:
            st.markdown(f"""
            <div class="result-card result-will-cancel">
              <div class="result-icon">⚠️</div>
              <div class="result-title">Likely to Cancel</div>
              <div class="result-prob">Cancellation probability: <strong>{cancel_pct}%</strong></div>
              <div class="result-advice">Consider sending a pre-arrival confirmation or offering a flexible upgrade to reduce cancellation risk.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-card result-will-stay">
              <div class="result-icon">✅</div>
              <div class="result-title">Likely to Stay</div>
              <div class="result-prob">Stay probability: <strong>{stay_pct}%</strong></div>
              <div class="result-advice">Low cancellation risk. A welcome message or upsell offer could enhance the guest experience.</div>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("📊 See probability breakdown"):
            st.markdown(f"""
            | Outcome | Probability |
            |---------|-------------|
            | ✅ Will Stay    | **{stay_pct}%** |
            | ⚠️ Will Cancel | **{cancel_pct}%** |
            """)

# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
<p style='text-align:center; color:#6FA3A5; font-size:0.78rem; letter-spacing:0.05em;'>
  HOTEL ANALYTICS · Powered by XGBoost · Internal Use Only
</p>
""", unsafe_allow_html=True)
