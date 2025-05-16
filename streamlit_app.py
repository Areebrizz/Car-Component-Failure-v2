import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load model and encoders
model = joblib.load('component_failure_model.pkl')
le_component = joblib.load('le_component.pkl')
le_maintenance = joblib.load('le_maintenance.pkl')

# Components for dropdown (get from label encoder classes)
components = list(le_component.classes_)

st.title("🚗 Car Component Failure Predictor")
st.markdown("Made with ❤️ by Muhammad Areeb Rizwan • Mechanical Engineer & AI Enthusiast")

# 1. Select component
component = st.selectbox("Select Component", components)

# 2. Input parameters based on dataset columns
temperature = st.slider("Temperature (°C)", 40.0, 160.0, 100.0)
vibration = st.slider("Vibration (units)", 0.0, 100.0, 30.0)
usage = st.slider("Usage (hours)", 0, 2500, 800)
maintenance_due = st.radio("Maintenance Due?", ['Yes', 'No'])

# Convert inputs to model features
component_enc = le_component.transform([component])[0]
maintenance_enc = le_maintenance.transform([maintenance_due])[0]

input_data = pd.DataFrame({
    'Component_enc': [component_enc],
    'Temperature': [temperature],
    'Vibration': [vibration],
    'Usage': [usage],
    'Maintenance_Due_enc': [maintenance_enc]
})

if st.button("Predict Failure Risk 🚦"):
    # Predict failure & probability
    pred = model.predict(input_data)[0]
    pred_proba = model.predict_proba(input_data)[0][1]

    if pred == 1:
        st.error(f"⚠️ Warning: Failure predicted with probability {pred_proba:.2f}")
    else:
        st.success(f"✅ No failure predicted (probability of failure: {pred_proba:.2f})")
