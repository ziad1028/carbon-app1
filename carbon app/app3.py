# app.py
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import pickle
import plotly.graph_objects as go
from datetime import datetime

# --- Model Loading ---
def load_model():
    try:
        with open('carbon_model.pkl', 'rb') as file:
            return pickle.load(file)
    except:
        # Create a simple default model if none exists
        X = np.random.rand(100, 4)
        y = X.sum(axis=1) * 2.5  # Dummy target
        model = RandomForestRegressor(n_estimators=100)
        model.fit(X, y)
        return model

# --- User Progress System ---
class UserProgress:
    def __init__(self):
        if 'points' not in st.session_state:
            st.session_state.points = 0
        if 'achievements' not in st.session_state:
            st.session_state.achievements = set()
        if 'history' not in st.session_state:
            st.session_state.history = []

    def add_points(self, points):
        st.session_state.points += points
        self.check_achievements()
    
    def check_achievements(self):
        points = st.session_state.points
        achievements = {
            'Beginner': 100,
            'Intermediate': 500,
            'Expert': 1000,
            'Master': 5000
        }
        for achievement, threshold in achievements.items():
            if points >= threshold and achievement not in st.session_state.achievements:
                st.session_state.achievements.add(achievement)
                st.success(f"🎉 New Achievement Unlocked: {achievement}!")

    def log_footprint(self, footprint):
        st.session_state.history.append({
            'date': datetime.now().strftime("%Y-%m-%d"),
            'footprint': footprint
        })

# --- Gauge Chart ---
def create_gauge_chart(value, max_value=20):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Carbon Footprint (tons CO2/year)"},
        gauge = {
            'axis': {'range': [None, max_value]},
            'bar': {'color': "darkgreen"},
            'steps': [
                {'range': [0, max_value/3], 'color': "lightgreen"},
                {'range': [max_value/3, 2*max_value/3], 'color': "yellow"},
                {'range': [2*max_value/3, max_value], 'color': "red"}
            ]
        }
    ))
    return fig

# --- Main App ---
def main():
    st.title("🌍 Carbon Footprint Calculator")
    st.sidebar.header("User Progress")
    
    # Initialize user progress
    progress = UserProgress()
    
    # Display user stats in sidebar
    st.sidebar.metric("Points", st.session_state.points)
    st.sidebar.subheader("Achievements")
    for achievement in st.session_state.achievements:
        st.sidebar.success(achievement)

    # Load model
    model = load_model()

    # Input form
    with st.form("carbon_calculator"):
        st.subheader("Enter Your Details")
        
        electricity = st.number_input("Monthly Electricity Usage (kWh)", min_value=0.0, max_value=10000.0, value=500.0)
        transport = st.number_input("Weekly Transport Distance (km)", min_value=0.0, max_value=1000.0, value=100.0)
        waste = st.number_input("Weekly Waste Production (kg)", min_value=0.0, max_value=100.0, value=10.0)
        diet_type = st.selectbox("Diet Type", 
                               ["Vegan", "Vegetarian", "Pescatarian", "Regular"],
                               index=3)
        
        # Diet type encoding
        diet_mapping = {"Vegan": 0, "Vegetarian": 1, "Pescatarian": 2, "Regular": 3}
        diet_encoded = diet_mapping[diet_type]
        
        submitted = st.form_submit_button("Calculate Footprint")
        
        if submitted:
            # Prepare input for model
            input_data = np.array([[electricity, transport, waste, diet_encoded]])
            
            # Get prediction
            footprint = model.predict(input_data)[0]
            
            # Add points based on footprint reduction
            baseline = 15  # Average carbon footprint
            if footprint < baseline:
                points_earned = int((baseline - footprint) * 100)
                progress.add_points(points_earned)
                st.success(f"You earned {points_earned} points for being below average!")
            
            # Log footprint
            progress.log_footprint(footprint)
            
            # Display gauge chart
            st.plotly_chart(create_gauge_chart(footprint))
            
            # Display recommendations
            st.subheader("Recommendations")
            recommendations = []
            if electricity > 400:
                recommendations.append("Consider using energy-efficient appliances and LED bulbs")
            if transport > 150:
                recommendations.append("Try carpooling or using public transport more often")
            if waste > 15:
                recommendations.append("Implement recycling and composting to reduce waste")
            if diet_encoded > 1:
                recommendations.append("Consider reducing meat consumption for a lower carbon footprint")
            
            for rec in recommendations:
                st.info(rec)
    
    # Historical tracking
    if st.session_state.history:
        st.subheader("Your Progress")
        history_df = pd.DataFrame(st.session_state.history)
        st.line_chart(history_df.set_index('date')['footprint'])

if __name__ == "__main__":
    main()