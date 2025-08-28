from datetime import date
import streamlit as st
import pandas as pd
from joblib import load


model = load("models/XGBoost_best_model.joblib") 
st.set_page_config(page_title="Flight Price Predictor", page_icon="✈️", layout="wide")


st.set_page_config(page_title="Flight Price Prediction", layout="centered")
st.title("✈️ Flight Price Prediction App")

st.write("Enter flight details to predict the price:")

# --- User Inputs ---
airline = st.selectbox("Airline", ["IndiGo", "Air India", "Jet Airways", "SpiceJet", "GoAir"])
source = st.selectbox("Source", ["Delhi", "Kolkata", "Mumbai", "Chennai"])
destination = st.selectbox("Destination", ["Cochin", "Delhi", "New Delhi", "Hyderabad", "Kolkata"])
total_stops = st.selectbox("Total Stops", ["non-stop", "1 stop", "2 stops", "3 stops", "4 stops"])

journey_day = st.number_input("Journey Day", min_value=1, max_value=31, value=1)
journey_month = st.number_input("Journey Month", min_value=1, max_value=12, value=1)
journey_year = st.number_input("Journey Year", min_value=2019, max_value=2030, value=2019)

dep_hour = st.number_input("Departure Hour", min_value=0, max_value=23, value=10)
dep_minute = st.number_input("Departure Minute", min_value=0, max_value=59, value=30)
arrival_hour = st.number_input("Arrival Hour", min_value=0, max_value=23, value=14)
arrival_minute = st.number_input("Arrival Minute", min_value=0, max_value=59, value=45)

airline_map = {"IndiGo": 0, "Air India": 1, "Jet Airways": 2, "SpiceJet": 3, "GoAir": 4}
source_map = {"Delhi": 0, "Kolkata": 1, "Mumbai": 2, "Chennai": 3}
destination_map = {"Cochin": 0, "Delhi": 1, "New Delhi": 2, "Hyderabad": 3, "Kolkata": 4}
stops_map = {"non-stop": 0, "1 stop": 1, "2 stops": 2, "3 stops": 3, "4 stops": 4}


duration = (arrival_hour * 60 + arrival_minute) - (dep_hour * 60 + dep_minute)
if duration < 0:  
    duration += 24 * 60
duration_hours = duration / 60.0

# Day of Week
journey_date = date(journey_year, journey_month, journey_day)
journey_dow = journey_date.weekday()  

input_data = pd.DataFrame([{
    "Airline": int(airline_map[airline]),
    "Source": int(source_map[source]),
    "Destination": int(destination_map[destination]),
    "Duration": float(duration_hours),
    "Total_Stops": int(stops_map[total_stops]),
    "Journey_Day": int(journey_day),
    "Journey_Month": int(journey_month),
    "Journey_DOW": int(journey_dow),
    "Dep_Hour": int(dep_hour),
    "Dep_Minute": int(dep_minute),
    "Arrival_Hour": int(arrival_hour),
    "Arrival_Minute": int(arrival_minute),
}])

input_data = input_data.astype(float)


if st.button("Predict Price"):
    try:
        prediction = model.predict(input_data)[0]
        st.success(f"💰 Predicted Flight Price: {prediction:.2f}")
    except Exception as e:
        st.error(f"Error during prediction: {e}")