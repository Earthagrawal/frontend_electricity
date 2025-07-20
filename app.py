import streamlit as st
import requests

# Set page config
st.set_page_config(
    page_title="Urban Project Cost Predictor",
    page_icon="⚡",
    layout="wide"
)

# Custom CSS - organized and cleaned up
st.markdown("""
<style>
    /* === BACKGROUND === */
    .stApp {
        background: linear-gradient(135deg, 
            #70328f 0%, 
            #613278 25%, 
            #4a275c 50%, 
            #622580 75%, 
            #70328f 100%);
        background-size: 300% 300%;
        animation: circularGradient 20s ease infinite;
    }
    
    @keyframes circularGradient {
        0% { background-position: 0% 50%; }
        25% { background-position: 50% 0%; }
        50% { background-position: 100% 50%; }
        75% { background-position: 50% 100%; }
        100% { background-position: 0% 50%; }
    }
    
    /* === TEXT COLORS === */
    .stMarkdown, .stText, h1, h2, h3, p, label {
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    /* === INPUT FIELDS === */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div,
    .stSlider > div > div > div {
        background-color: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Dropdown options */
    .stSelectbox > div > div > div > div {
        background-color: rgba(30, 30, 30, 0.95) !important;
        color: white !important;
    }
    
    /* === SLIDER STYLING === */
    .stSlider > div > div > div > div {
        background-color: #a17142 !important;
    }
    
    /* === CONTAINERS (removed glass effect) === */
    .element-container {
        background-color: transparent !important;
        border: none !important;
        backdrop-filter: none !important;
        padding: 10px !important;
        margin: 5px 0px !important;
    }
    
    /* === PREDICT BUTTON === */
    .stButton > button {
        background: #4a4a4a !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        background: #5a5a5a !important;
        transform: translateY(-1px) !important;
    }
    
    /* === MESSAGES === */
    .stSuccess {
        background-color: rgba(0, 200, 0, 0.15) !important;
        border: 1px solid rgba(0, 255, 0, 0.3) !important;
        border-radius: 8px !important;
    }
    
    .stError {
        background-color: rgba(255, 0, 0, 0.15) !important;
        border: 1px solid rgba(255, 0, 0, 0.3) !important;
        border-radius: 8px !important;
    }
    
    /* === TITLE === */
    h1 {
        text-align: center !important;
        font-size: 2.5rem !important;
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5) !important;
        margin-bottom: 20px !important;
    }
    
    /* === SUBTITLE === */
    .subtitle {
        text-align: center !important;
        font-size: 1.1rem !important;
        color: rgba(255, 255, 255, 0.8) !important;
        margin-bottom: 30px !important;
    }
    
    /* === METRICS === */
    .metric-container {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        padding: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

# API URL
API_URL = "https://electricity-cost-prediction-regression.onrender.com/predict"

# Header
st.title("⚡ Urban Project Cost Predictor")
st.markdown('<p class="subtitle">Predict electricity costs for urban projects with AI-powered precision</p>', unsafe_allow_html=True)

# Layout
col1, col2 = st.columns(2)

# INPUT SECTION
with col1:
    st.subheader("🏗️ Property Details")
    site_area = st.number_input("Site Area (sq ft)", min_value=1, value=1500)
    structure_type = st.selectbox("Structure Type", ["Commercial", "Industrial", "Mixed-use", "Residential"])
    resident_count = st.number_input("Resident Count", min_value=1, value=4)

with col2:
    st.subheader("📊 Usage Metrics")
    water_consumption = st.number_input("Water Consumption (gallons)", min_value=1, value=2500)
    recycling_rate = st.slider("Recycling Rate (%)", min_value=1, value=60)
    utilisation_rate = st.slider("Utilisation Rate (%)", min_value=1, value=75)

# Additional inputs in separate row
col3, col4 = st.columns(2)
with col3:
    air_qality_index = st.number_input("Air Quality Index", min_value=1, value=150)
with col4:
    issue_reolution_time = st.number_input("Issue Resolution Time (hours)", min_value=1, value=24)

st.markdown("<br>", unsafe_allow_html=True)

# PREDICTION SECTION
if st.button("🔮 Predict Cost", type="primary", use_container_width=True):
    input_data = {
        "site_area": site_area,
        "structure_type": structure_type,
        "water_consumption": water_consumption,
        "recycling_rate": recycling_rate,
        "utilisation_rate": utilisation_rate,
        "air_qality_index": air_qality_index,
        "issue_reolution_time": issue_reolution_time,
        "resident_count": resident_count
    }

    try:
        with st.spinner("🤖 AI is analyzing your project..."):
            response = requests.post(API_URL, json=input_data)

        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) == 2:
                prediction_value = result[1]
                st.success(f"🎯 **Predicted Electricity Cost: ${prediction_value:,.2f}**")
                
                # Cost breakdown with cleaner metrics
                st.markdown("### 📈 Cost Breakdown Analysis")
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("💡 Monthly Est.", f"${prediction_value/12:,.2f}")
                with col_b:
                    st.metric("⚡ Daily Est.", f"${prediction_value/365:,.2f}")
                with col_c:
                    efficiency_score = max(1, 100 - (prediction_value / site_area * 10))
                    st.metric("🌱 Efficiency Score", f"{efficiency_score:.0f}%")
                    
            else:
                st.success(f"✅ {result}")
        else:
            st.error(f"❌ API Error {response.status_code}: {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("🚫 Could not connect to API server. Please try again later.")
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")

# FOOTER
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <p style='font-size: 14px; color: rgba(255,255,255,0.6);'>
        🚀 Powered by Machine Learning & FastAPI | ⚡ Real-time AI Predictions
    </p>
</div>
""", unsafe_allow_html=True)
