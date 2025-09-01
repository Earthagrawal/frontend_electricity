
# Electricity Cost Predictor — Frontend

> Streamlit frontend providing interactive UI for electricity cost predictions.

---

## Features
- Clean user interface built with Streamlit.
- Connects to backend FastAPI service for real-time predictions.
- Input fields for consumption, site type, and temperature.
- Visualizes predictions in a structured layout.

---

## Quickstart
```bash
git clone <frontend-repo-url>
cd frontend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

streamlit run app.py
```

Set Backend URL in the UI (e.g., `http://localhost:8000`).

---

## Deployment (Render)
- Create a Web Service running:  
  `streamlit run app.py`  
- Ensure backend service is running and accessible.


Frontend for my Render Web-service : https://frontend-for-electricity-cost.onrender.com/
