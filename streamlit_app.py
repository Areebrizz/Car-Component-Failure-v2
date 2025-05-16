import streamlit as st

st.set_page_config(page_title="🚗 Car Component Failure Predictor", layout="centered")

# --- Styles for futuristic UI ---
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: #cbd5e1;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .title {
        font-size: 2.8rem;
        font-weight: 700;
        color: #00ffe7;
        text-align: center;
        margin-bottom: 0;
    }
    .subtitle {
        font-size: 1.25rem;
        color: #81a1c1;
        text-align: center;
        margin-top: 0;
        margin-bottom: 1.5rem;
    }
    .footer {
        text-align: center;
        font-size: 0.9rem;
        margin-top: 3rem;
        color: #5e81ac;
        border-top: 1px solid #3b4252;
        padding-top: 1rem;
    }
    a {
        color: #88c0d0;
        text-decoration: none;
        margin: 0 0.5rem;
        font-weight: 600;
    }
    a:hover {
        color: #00ffe7;
        text-decoration: underline;
    }
    .warning {
        background-color: #ff004d;
        padding: 0.8rem 1rem;
        border-radius: 8px;
        font-weight: 700;
        color: white;
        margin-top: 1rem;
        text-align: center;
        font-size: 1.1rem;
        box-shadow: 0 0 15px #ff004daa;
    }
    .input-label {
        font-weight: 600;
        color: #81a1c1;
        margin-bottom: 0.2rem;
    }
    .slider {
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown('<h1 class="title">🚗 Car Component Failure Predictor</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Made with ❤️ by Muhammad Areeb Rizwan • Mechanical Engineer & AI Enthusiast</p>', unsafe_allow_html=True)

# --- Input Section ---
component = st.selectbox("Select Component", ["Engine", "Transmission", "Brake Pad", "Exhaust", "Suspension"])

col1, col2 = st.columns(2)

with col1:
    st.markdown('<label class="input-label">Temperature (°C)</label>', unsafe_allow_html=True)
    temperature = st.slider("", 40.0, 160.0, 90.0, step=0.5, key="temp", help="Operating temperature of component")

    st.markdown('<label class="input-label">Vibration (units)</label>', unsafe_allow_html=True)
    vibration = st.slider("", 0.0, 100.0, 20.0, step=0.1, key="vib", help="Vibration level measured")

with col2:
    st.markdown('<label class="input-label">Usage (hours)</label>', unsafe_allow_html=True)
    usage = st.slider("", 0, 2500, 1000, step=10, key="usage", help="Total usage hours of the component")

    st.markdown('<label class="input-label">Maintenance Due?</label>', unsafe_allow_html=True)
    maintenance_due = st.radio("", ("Yes", "No"), index=0, key="maint", horizontal=True)

# --- Prediction Button ---
predict_button = st.button("Predict Failure Risk 🚦")

# --- Placeholder for result ---
if predict_button:
    # Dummy example — replace with your model prediction code:
    # pred_prob = model.predict_proba([[temperature, vibration, usage, maintenance_encoded]])[0][1]
    pred_prob = 0.67  # Replace with actual model prediction

    if pred_prob > 0.5:
        st.markdown(f'<div class="warning">⚠️ Warning: Failure predicted with probability {pred_prob:.2f}</div>', unsafe_allow_html=True)
    else:
        st.success(f"✅ No failure predicted (probability: {pred_prob:.2f})")

# --- Footer with credits and links ---
st.markdown("""
<div class="footer">
    <p>### 👨‍💻 Made By: M Areeb Rizwan</p>
    <p>
        🔗 <a href="https://www.linkedin.com/in/areebrizwan" target="_blank">LinkedIn</a> •
        🌐 <a href="https://sites.google.com/view/m-areeb-rizwan/home" target="_blank">Portfolio</a> •
        💻 <a href="https://github.com/Areebrizz" target="_blank">GitHub</a>
    </p>
</div>
""", unsafe_allow_html=True)
