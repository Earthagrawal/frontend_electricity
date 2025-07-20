import streamlit as st
import requests

# Set page config
st.set_page_config(
    page_title="Urban Project Cost Predictor",
    page_icon="⚡",
    layout="wide"
)

# Custom CSS for vibrant background
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, 
            #667eea 0%, 
            #764ba2 25%, 
            #f093fb 50%, 
            #f5576c 75%, 
            #4facfe 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Make text more readable on vibrant background */
    .stMarkdown, .stText, h1, h2, h3, p {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    /* Style input containers */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div,
    .stSlider > div > div > div {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 10px !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Style the main containers */
    .element-container {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        margin: 10px 0px !important;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background-color: rgba(0, 255, 0, 0.2) !important;
        border: 2px solid #00ff00 !important;
        border-radius: 10px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stError {
        background-color: rgba(255, 0, 0, 0.2) !important;
        border: 2px solid #ff0000 !important;
        border-radius: 10px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 15px 30px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 35px rgba(0,0,0,0.4) !important;
        background: linear-gradient(45deg, #4ecdc4, #ff6b6b) !important;
    }
    
    /* Title styling */
    h1 {
        text-align: center !important;
        font-size: 3rem !important;
        background: linear-gradient(45deg, #fff, #f0f0f0) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        text-shadow: none !important;
        margin-bottom: 30px !important;
    }
    
    /* Subtitle styling */
    .subtitle {
        text-align: center !important;
        font-size: 1.2rem !important;
        color: rgba(255, 255, 255, 0.8) !important;
        margin-bottom: 40px !important;
    }
</style>
""", unsafe_allow_html=True)

# Use your deployed FastAPI URL
API_URL = "https://electricity-cost-prediction-regression.onrender.com/predict"

st.title("⚡ Urban Project Cost Predictor")
st.markdown('<p class="subtitle">Predict electricity costs for urban projects with AI-powered precision</p>', unsafe_allow_html=True)

# Create columns for better layout
col1, col2 = st.columns(2)

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

col3, col4 = st.columns(2)
with col3:
    air_qality_index = st.number_input("Air Quality Index", min_value=1, value=150)
with col4:
    issue_reolution_time = st.number_input("Issue Resolution Time (hours)", min_value=1, value=24)

# Add some spacing
st.markdown("<br>", unsafe_allow_html=True)

# Predict button
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
                
                # Add some fun metrics
                st.markdown("### 📈 Cost Breakdown Analysis")
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("💡 Monthly Est.", f"${prediction_value/12:,.2f}", delta="per month")
                with col_b:
                    st.metric("⚡ Daily Est.", f"${prediction_value/365:,.2f}", delta="per day")
                with col_c:
                    efficiency_score = max(1, 100 - (prediction_value / site_area * 10))
                    st.metric("🌱 Efficiency Score", f"{efficiency_score:.0f}%", delta="energy rating")
                    
            else:
                st.success(f"✅ {result}")
        else:
            st.error(f"❌ API Error {response.status_code}: {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("🚫 Could not connect to API server. Please try again later.")
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")

# Footer with animated elements
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <p style='font-size: 16px; color: rgba(255,255,255,0.8);'>
        🚀 Powered by Machine Learning & FastAPI | 
        🎨 Enhanced with Dynamic Gradients | 
        ⚡ Real-time AI Predictions
    </p>
</div>
""", unsafe_allow_html=True)
