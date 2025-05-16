import streamlit as st
import numpy as np
import joblib
import pandas as pd

# ---- Load model and encoders once ----
@st.cache_resource(show_spinner=False)
def load_model_and_encoders():
    model = joblib.load('component_failure_model.pkl')
    le_component = joblib.load('le_component.pkl')
    le_maintenance = joblib.load('le_maintenance.pkl')
    return model, le_component, le_maintenance

model, le_component, le_maintenance = load_model_and_encoders()

# ---- Page config & styles ----
st.set_page_config(page_title="🚗 Car Component Failure Predictor", layout="wide")

st.markdown(
    """
    <style>
    body {background-color: #121212; color: #E0E0E0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;}
    h1,h2,h3 {color: #00ffcc; font-weight: 700;}
    .stButton>button {background-color: #00ffcc; color: #000; font-weight: 700; border-radius: 10px; padding: 10px 0;}
    .stButton>button:hover {background-color: #00cc99; color: #fff;}
    .failure-warning {background-color: #ff3333; color: white; padding: 10px; border-radius: 12px; font-weight: 700; box-shadow: 0 0 15px #ff3333aa; text-align: center;}
    .success-msg {background-color: #33cc33; color: white; padding: 10px; border-radius: 12px; font-weight: 700; text-align: center;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---- Sidebar Inputs ----
st.sidebar.header("Input Parameters")

component = st.sidebar.selectbox("Choose Component", le_component.classes_)
temperature = st.sidebar.slider("Temperature (°C)", 40.0, 160.0, 90.0, 0.5)
vibration = st.sidebar.slider("Vibration Level", 0.0, 100.0, 20.0, 0.1)
usage = st.sidebar.slider("Usage (hours)", 0, 2500, 1000, 10)
maintenance_due = st.sidebar.radio("Maintenance Due?", options=le_maintenance.classes_)

enable_predict = usage > 0

# ---- Main UI ----
st.title("🚗 Car Component Failure Predictor")

st.markdown(f"### 🔍 Component Selected: **{component}**")

col1, col2 = st.columns(2)
with col1:
    st.write(f"- Temperature: **{temperature:.1f} °C**")
    st.write(f"- Usage Hours: **{usage}**")
with col2:
    st.write(f"- Vibration Level: **{vibration:.1f}**")
    st.write(f"- Maintenance Due: **{maintenance_due}**")

st.markdown("---")

if enable_predict:
    if st.button("🚦 Predict Failure Risk"):
        # Prepare input vector
        component_enc = le_component.transform([component])[0]
        maintenance_enc = le_maintenance.transform([maintenance_due])[0]
        
        X_input = np.array([[component_enc, temperature, vibration, usage, maintenance_enc]])
        
        # Predict failure probability
        pred_proba = model.predict_proba(X_input)[0][1]  # Probability of class 1 (failure)
        
        progress_bar = st.progress(0)
        for i in range(0, int(pred_proba * 100) + 1):
            progress_bar.progress(i)
        
        if pred_proba > 0.5:
            st.markdown(f'<div class="failure-warning">⚠️ Failure predicted with probability: {pred_proba:.2f}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="success-msg">✅ No failure predicted (probability: {pred_proba:.2f})</div>', unsafe_allow_html=True)
        
        # Download summary
        result_text = (
            f"Component: {component}\n"
            f"Temperature: {temperature} °C\n"
            f"Vibration: {vibration}\n"
            f"Usage: {usage} hours\n"
            f"Maintenance Due: {maintenance_due}\n"
            f"Failure Probability: {pred_proba:.2f}"
        )
        st.download_button("💾 Download Prediction Summary", data=result_text, file_name="prediction.txt", mime="text/plain")
else:
    st.warning("Please increase Usage hours above zero to enable prediction.")

# Optional: show failure history or any other info here
with st.expander("📈 View Component Failure History (Sample)"):
    data = {
        "Component": ["Engine", "Transmission", "Brake Pad", "Exhaust", "Suspension"],
        "Failure Rate (%)": [12, 18, 28, 8, 15],
        "Last 30 days failures": [5, 7, 11, 2, 6],
    }
    df_history = pd.DataFrame(data)
    st.dataframe(df_history)

# Footer
st.markdown(
    """
    <hr>
    <p style="text-align:center; font-size:0.85rem; color:#888;">
    Made with ❤️ by <b>Muhammad Areeb Rizwan</b> — 
    <a href="https://linkedin.com/in/areebrizwan" target="_blank" style="color:#00ffcc;">LinkedIn</a> • 
    <a href="https://github.com/Areebrizz" target="_blank" style="color:#00ffcc;">GitHub</a>
    </p>
    """,
    unsafe_allow_html=True,
)
