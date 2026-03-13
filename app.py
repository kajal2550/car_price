import streamlit as st
import numpy as np
import pickle

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Car Price Prediction",
    page_icon="🚗",
    layout="wide"
)

# ================= LOAD MODEL =================
model = pickle.load(open("model.pkl", "rb"))

# ================= CSS =================
st.markdown("""
<style>

/* ===== DARK DEFAULT STREAMLIT NAVBAR ===== */
[data-testid="stHeader"] {
    background: linear-gradient(90deg, #0f172a, #1e293b) !important;
}

[data-testid="stHeader"] * {
    color: white !important;
}

/* Cinematic Background */
.stApp {
    background:
        linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)),
        url("https://st3.depositphotos.com/2572561/32163/i/450/depositphotos_321637190-stock-photo-automotive-engineer-uses-digital-tablet.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Header Only */
.glass-header {
    backdrop-filter: blur(18px);
    background: rgba(255, 255, 255, 0.15);
    padding: 20px;
    border-radius: 20px;
    width: 60%;
    margin: 30px auto;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
}

/* White Labels */
label, .stSlider label {
    color: white !important;
}

/* Section Titles */
.section {
    font-size: 22px;
    font-weight: 700;
    color: white;
    margin-top: 20px;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 30px;
    height: 55px;
    font-size: 18px;
    width: 100%;
    border: none;
    transition: 0.3s ease;
}

.stButton > button:hover {
    transform: scale(1.05);
}

/* Result */
.result {
    background: white;
    padding: 25px;
    border-radius: 20px;
    font-size: 26px;
    font-weight: bold;
    color: #0f172a;
    text-align: center;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("""
<div class="glass-header">
    <h1 style="margin:0; font-size:34px; color:white;">
        🚗 Car Price Prediction
    </h1>
    <p style="margin:6px 0 0 0; font-size:15px; color:#e2e8f0;">
        AI-powered used car price estimation
    </p>
</div>
""", unsafe_allow_html=True)

# ================= FORM =================
st.markdown('<div class="section">🚘 Car Details</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    brand = st.selectbox("Car Brand", ["Maruti", "Hyundai", "Honda", "Toyota", "Ford", "Tata"])
    year = st.slider("Manufactured Year", 2000, 2024, 2016)
    kms_driven = st.slider("Kilometers Driven", 0, 200000, 40000)

with col2:
    fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "Electric"])
    transmission = st.selectbox("Transmission Type", ["Manual", "Automatic"])
    seller_type = st.selectbox("Seller Type", ["Dealer", "Individual"])

st.markdown('<div class="section">⚙ Specifications</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    mileage = st.slider("Mileage (km/l)", 5.0, 35.0, 18.0)
    engine = st.slider("Engine Capacity (CC)", 800, 3000, 1200)

with col4:
    seats = st.slider("Number of Seats", 4, 7, 5)
    owner = st.selectbox("Owner Type", ["First Owner", "Second Owner", "Third Owner"])

# ================= ENCODING =================
brand_map = {"Maruti":0, "Hyundai":1, "Honda":2, "Toyota":3, "Ford":4, "Tata":5}
fuel_map = {"Petrol":0, "Diesel":1, "CNG":2, "Electric":3}
seller_map = {"Dealer":0, "Individual":1}
trans_map = {"Manual":0, "Automatic":1}
owner_map = {"First Owner":0, "Second Owner":1, "Third Owner":2}

# ================= PREDICTION =================
if st.button("🚀 Predict Car Price"):

    input_data = np.array([[ 
        brand_map[brand],
        year,
        kms_driven,
        fuel_map[fuel_type],
        seller_map[seller_type],
        trans_map[transmission],
        owner_map[owner],
        mileage,
        engine,
        seats
    ]])

    prediction = model.predict(input_data)[0]
    price_lakh = max(prediction / 100000, 0.5)

    st.markdown(
        f'<div class="result">💰 Estimated Price: ₹ {price_lakh:.2f} Lakhs</div>',
        unsafe_allow_html=True
    )