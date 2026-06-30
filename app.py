import streamlit as st
import joblib
import pandas as pd

# Load the trained model and column structure
model = joblib.load('car_price_model.pkl')
model_columns = joblib.load('model_columns.pkl')

st.title("🚗 Used Car Price Predictor")
st.write("Enter the car details below to get an estimated price.")

# User inputs
brand = st.text_input("Brand (e.g. Maruti, Hyundai, Honda)")
model_name = st.text_input("Model (e.g. Alto, i20, City)")
vehicle_age = st.slider("Vehicle Age (years)", 0, 25, 5)
km_driven = st.number_input("Kilometers Driven", min_value=0, value=30000)
fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])
transmission_type = st.selectbox("Transmission", ["Manual", "Automatic"])
seller_type = st.selectbox("Seller Type", ["Individual", "Dealer", "Trustmark Dealer"])
mileage = st.number_input("Mileage (kmpl)", min_value=0.0, value=18.0)
engine = st.number_input("Engine (cc)", min_value=0, value=1200)
max_power = st.number_input("Max Power (bhp)", min_value=0.0, value=80.0)
seats = st.slider("Seats", 2, 10, 5)

if st.button("Predict Price"):
    # Build a single-row dataframe matching training format
    input_dict = {
        'vehicle_age': vehicle_age,
        'km_driven': km_driven,
        'mileage': mileage,
        'engine': engine,
        'max_power': max_power,
        'seats': seats,
    }

    input_df = pd.DataFrame([input_dict])

    # Add one-hot columns, all zero by default
    for col in model_columns:
        if col not in input_df.columns:
            input_df[col] = 0

    # Set the relevant one-hot columns to 1 based on user input
    fuel_col = f'fuel_type_{fuel_type}'
    trans_col = f'transmission_type_{transmission_type}'
    seller_col = f'seller_type_{seller_type}'
    brand_col = f'brand_{brand}'
    model_col = f'model_{model_name}'

    for col in [fuel_col, trans_col, seller_col, brand_col, model_col]:
        if col in input_df.columns:
            input_df[col] = 1

    # Match column order exactly to training
    input_df = input_df[model_columns]

    prediction = model.predict(input_df)[0]
    st.success(f"Estimated Price: ₹{prediction:,.0f}")