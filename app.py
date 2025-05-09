import streamlit as st
import sqlite3
import requests
import numpy as np
import pickle
from irrigation import get_irrigation_recommendation
from PIL import Image
import streamlit.components.v1 as components
# Load trained crop model
with open("xgb_crop_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("label_encoder.pkl", "rb") as le_file:
    le = pickle.load(le_file)

# Descriptive mappings
SOIL_MOISTURE_MAP = {
    "Very Dry": (0, 20),
    "Dry": (21, 40),
    "Moist": (41, 70),
    "Wet": (71, 100)
}

TEMPERATURE_MAP = {
    "Cold": (0, 15),
    "Warm": (16, 30),
    "Hot": (31, 50)
}

HUMIDITY_MAP = {
    "Low": (0, 40),
    "Medium": (41, 70),
    "High": (71, 100)
}

# Convert descriptive input to numerical
def to_mid(value):
    if isinstance(value, int):
        return value
    if value in SOIL_MOISTURE_MAP:
        return sum(SOIL_MOISTURE_MAP[value]) // 2
    if value in TEMPERATURE_MAP:
        return sum(TEMPERATURE_MAP[value]) // 2
    if value in HUMIDITY_MAP:
        return sum(HUMIDITY_MAP[value]) // 2
    try:
        return int(value)
    except:
        return None

# FAQ chatbot
def get_farming_info(query):
    conn = sqlite3.connect("farming_data.db")
    cursor = conn.cursor()
    
    query = query.lower()
    cursor.execute("SELECT question, response FROM farming_info")
    data = cursor.fetchall()
    
    best_match = None
    highest_score = 0

    for question, response in data:
        score = sum(1 for word in query.split() if word in question.lower() or word in response.lower())
        if score > highest_score:
            highest_score = score
            best_match = response

    conn.close()
    return best_match if best_match else "⚠️ No relevant farming info found."

# Crop prediction logic
def predict_crop(input_features):
    input_array = np.array([input_features]).reshape(1, -1)
    predicted_label = model.predict(input_array)[0]
    predicted_crop = le.inverse_transform([predicted_label])[0]
    return predicted_crop

# UI
st.set_page_config(page_title="AgriAssistant", layout="wide")
st.title("🌾 AgriAssistant Dashboard")

tabs = st.tabs(["🏡 Home", "🌱 Crop Recommendation", "💧 Irrigation", "Chat with AgriBot 🤖", "🤖 FAQ Chatbot"])


# Home Tab content inside the first tab
with tabs[0]:
    st.markdown("# Welcome to AgriAssistant! 🌱")
    st.markdown("### Empowering Farmers with AI-driven Insights")

    st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <img src="https://i.pinimg.com/736x/9e/04/c9/9e04c9ddf8b801ff8ec074a8c3865ef8.jpg" 
                alt="Farmers at work in the field" 
                style="width: 500px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            <p style="font-style: italic; color: gray; margin-top: 8px;">Farmers at work in the field</p>
        </div>
    """, unsafe_allow_html=True)

    st.write("""
        **AgriAssistant** uses artificial intelligence to provide personalized insights for farmers, helping them make informed decisions for efficient farming. 
        From crop recommendations to smart irrigation solutions, we aim to support farmers in maximizing yields and sustainability. 🌾
    """)

    st.markdown("### Key Features:")
    st.write("""
        - **Crop Recommendations**: AI-powered suggestions for the best crops based on weather, soil, and environmental conditions.
        - **Irrigation Management**: Get irrigation recommendations tailored to your farm's needs.
        - **AI Chatbot**: Instant answers to your farming-related questions.
    """)

    st.markdown("### Get Started Now!")
    st.button("Start Exploring")

    st.markdown("### Watch our Introduction Video 🎥")
    components.html(
        """
        <iframe width="560" height="315" src="https://www.youtube.com/embed/NMhoUELo3Cc" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        """,
        height=350
    )

# Crop Recommendation tab
with tabs[1]:
    st.subheader("🌱 Enter Soil & Climate Data")

    # Explanation section to explain ML model
    st.markdown("""
    ## How the Crop Recommendation System Works 🧠
    
    Our system is powered by a machine learning model trained on a large dataset that includes various environmental factors such as soil composition, temperature, humidity, and rainfall. This model is not hard-coded but uses data-driven predictions to recommend the best crop for your farm's unique conditions. 🌾

    **Key Features of the Model**:
    - The model has been trained on **thousands of data points** from real-world farms across different climates and regions.
    - It uses **multiple environmental factors**, including soil nutrients (N, P, K), pH levels, temperature, humidity, and rainfall, to predict the ideal crops for the specific conditions.
    - The model is continuously refined with new data to improve accuracy and recommendations.
    
    This approach ensures that the crop suggestions are relevant, based on actual data and scientific principles, helping you make informed decisions for optimal crop yield.
    """)

    st.markdown("""
    ## Why Trust the Recommendations? 📊
    
    The system was trained using **large-scale agricultural datasets** with data from **global farming regions**. It considers multiple environmental variables and uses advanced machine learning techniques to make predictions that are reliable and backed by real-world data. So you can trust the recommendations based on solid scientific research, not random guesses.
    
    """)

    # Input form for soil and climate data
    col1, col2 = st.columns(2)
    with col1:
        N = st.number_input("Nitrogen (N)", 0, 200)
        P = st.number_input("Phosphorus (P)", 0, 200)
        K = st.number_input("Potassium (K)", 0, 200)
        pH = st.number_input("Soil pH", 0.0, 14.0)

    with col2:
        temp = st.number_input("Temperature (°C)", 0.0, 50.0)
        hum = st.number_input("Humidity (%)", 0.0, 100.0)
        rainfall = st.number_input("Rainfall (mm)", 0.0, 500.0)

    # Button to trigger crop prediction
    if st.button("🚀 Predict Crop"):
        features = [N, P, K, temp, hum, pH, rainfall]
        try:
            crop = predict_crop(features)
            st.success(f"🌾 Recommended Crop: **{crop}**")
        except Exception as e:
            st.error(f"Error: {e}")



# Irrigation tab
with tabs[2]:
    st.subheader("💧 Get Irrigation Advice")

    crop_categories = {
    "Cereal Crops": ["Maize", "Wheat"],
    "Vegetables": ["Tomato", "Potato"],
    "Fruits": ["Strawberry", "Mango"],
    "Legumes": ["Beans", "Peas"],
    "Root Crops": ["Carrot", "Cassava"]
}

category = st.selectbox("Select Crop Category", list(crop_categories.keys()))
# Grouped crop categories
crop_categories = {
    "Cereal Crops": ["Maize", "Wheat", "Barley"],
    "Vegetables": ["Tomato", "Potato", "Cabbage"],
    "Fruits": ["Strawberry", "Mango", "Banana"],
    "Legumes": ["Beans", "Peas"],
    "Root Crops": ["Carrot", "Cassava", "Beetroot"]
}

# Let user first select category, then specific crop
category = st.selectbox("🌾 Select Crop Category", list(crop_categories.keys()))
crop = st.selectbox("🌱 Select Specific Crop", crop_categories[category])

    soil = st.selectbox("Soil Moisture", list(SOIL_MOISTURE_MAP.keys()) + [10, 30, 50, 70])
    temp = st.selectbox("Temperature", list(TEMPERATURE_MAP.keys()) + [10, 25, 40])
    hum = st.selectbox("Humidity", list(HUMIDITY_MAP.keys()) + [20, 60, 80])

    if st.button("💧 Recommend Irrigation"):
        soil_val = to_mid(soil)
        temp_val = to_mid(temp)
        hum_val = to_mid(hum)

        if None in (soil_val, temp_val, hum_val):
            st.warning("⚠️ Please enter valid values.")
        else:
            recommendation = get_irrigation_recommendation(soil_val, temp_val, hum_val, crop)
            st.success(recommendation)

with tabs[3]:
    st.markdown("## 💬 Chat with AgriBot")

    col1, col2 = st.columns([1.2, 1])  # Adjust proportions: chatbot wider

    with col1:
        st.markdown("### 🤖 Your Farming Assistant")
        components.html(
            """
            <div id="chatbot-container" style="height: 600px; width: 100%;"></div>
            <script>
            window.chatbaseConfig = {
                chatbotId: "DOD8oYHsTQh1lEvpqMZdd",
                selector: "#chatbot-container",
                welcomeMessage: "👋 Hello! How can I help with your farming today?",
            };
            (function() {
                var script = document.createElement("script");
                script.src = "https://www.chatbase.co/embed.min.js";
                script.defer = true;
                document.body.appendChild(script);
            })();
            </script>
            """,
            height=600
        )

    with col2:
        st.markdown("### 📋 How to Use AgriBot")
        st.write("""
        You can ask questions like:
        - *“What’s the best crop to grow this month in Tigray?”*
        - *“How do I deal with tomato pests naturally?”*
        - *“What irrigation system is ideal for small farms?”*

        AgriBot will give instant, AI-powered answers to help you farm smarter 🌿
        """)
        st.success("💡 Click the chat window below and 👈 start chatting with AgriBot on the left!")





# FAQ tab
with tabs[4]:
    st.subheader("📋 Ask a Farming Question")

    question = st.text_input("Ask your question:")
    if st.button("🔍 Search FAQ"):
        if question.strip() != "":
            reply = get_farming_info(question)
            st.info(reply)
        else:
            st.warning("Please enter a question.")

st.markdown("""
<style>
.footer {
    position: fixed;
    bottom: 10px;
    left: 0;
    right: 0;
    text-align: center;
    color: gray;
    font-size: 14px;
    padding: 10px;
}
</style>
<div class="footer">
    © 2024 Yanet Niguse Tesfay. All rights reserved.
</div>
""", unsafe_allow_html=True)
