import streamlit as st
import pandas as pd
from joblib import load


model = load("models/XGBoost_best_model.joblib") 
st.set_page_config(page_title="Flight Price Predictor", page_icon="✈️", layout="wide")


st.set_page_config(page_title="Flight Price Predictor", page_icon="✈️", layout="centered")
st.title("✈️ Flight Price Predictor")
st.write("Predict the flight price based on your flight details!")


st.subheader("Enter Flight Details")


airline_options = ["Air India", "GoAir", "IndiGo", "Jet Airways", 
                                            "Jet Airways Business", "Multiple carriers", 
                                            "Multiple carriers Premium economy", "SpiceJet",
                                            "Trujet", "Vistara", "Vistara Premium economy"]  
source_options = ["Chennai", "Kolkata", "Delhi", "Mumbai", "Bangalore"]
destination_options = ["Cochin", "Delhi", "Hyderabad", "Kolkata", "New Delhi"]

airline = st.selectbox("Airline (encoded)", airline_options)
source = st.selectbox("Source (encoded)", source_options)
destination = st.selectbox("Destination (encoded)", destination_options)


journey_day = st.slider("Journey Day", 1, 31, 15)
journey_month = st.slider("Journey Month", 1, 12, 6)
journey_dow = st.slider("Day of Week (0=Mon,6=Sun)", 0, 6, 2)

dep_hour = st.slider("Departure Hour", 0, 23, 10)
dep_minute = st.slider("Departure Minute", 0, 59, 30)
arrival_hour = st.slider("Arrival Hour", 0, 23, 12)
arrival_minute = st.slider("Arrival Minute", 0, 59, 0)


duration = st.slider("Duration (minutes)", 30, 1440, 120)
total_stops = st.slider("Total Stops", 0, 4, 1)

if st.button("Predict Price"):
    input_df = pd.DataFrame({
        'Airline':[airline],
        'Source':[source],
        'Destination':[destination],
        'Duration':[duration],
        'Total_Stops':[total_stops],
        'Journey_Day':[journey_day],
        'Journey_Month':[journey_month],
        'Journey_DOW':[journey_dow],
        'Dep_Hour':[dep_hour],
        'Dep_Minute':[dep_minute],
        'Arrival_Hour':[arrival_hour],
        'Arrival_Minute':[arrival_minute]
    })

    predicted_price = model.predict(input_df)[0]

    st.subheader("Predicted Flight Price")
    st.metric(label="Price ", value=f"{predicted_price:,.2f}")