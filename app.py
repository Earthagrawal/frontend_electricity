import streamlit as st
import requests

# Set page config
st.set_page_config(
    page_title="Urban Project Cost Predictor",
    page_icon="⚡",
    layout="wide"
)

# Use your deployed FastAPI URL
API_URL = "https://electricity-cost-prediction-regression.onrender.com/predict"

st.title("⚡ Urban Project Cost Predictor")
st.markdown("*Predict electricity costs for urban projects*")

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
        with st.spinner("🤖 Predicting..."):
            response = requests.post(API_URL, json=input_data)

        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) == 2:
                prediction_value = result[1]
                st.success(f"🎯 **Predicted Electricity Cost: ${prediction_value:,.2f}**")
            else:
                st.success(f"✅ {result}")
        else:
            st.error(f"❌ API Error {response.status_code}: {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("🚫 Could not connect to API server.")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

st.markdown("---")
st.markdown("*Powered by Machine Learning & FastAPI*")