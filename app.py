import streamlit as st
import joblib
import pandas as pd
import requests

# Load the trained model and column structure
model = joblib.load('car_price_model.pkl')
model_columns = joblib.load('model_columns.pkl')

st.title("🚗 carIQ — Used Car Price Predictor")
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

# Currency selector
currency = st.selectbox("Show price in:", ["INR (₹)", "USD ($)", "EUR (€)", "GBP (£)"])

if st.button("Predict Price"):
    input_dict = {
        'vehicle_age': vehicle_age,
        'km_driven': km_driven,
        'mileage': mileage,
        'engine': engine,
        'max_power': max_power,
        'seats': seats,
    }

    input_df = pd.DataFrame([input_dict])

    for col in model_columns:
        if col not in input_df.columns:
            input_df[col] = 0

    fuel_col = f'fuel_type_{fuel_type}'
    trans_col = f'transmission_type_{transmission_type}'
    seller_col = f'seller_type_{seller_type}'
    brand_col = f'brand_{brand}'
    model_col = f'model_{model_name}'

    for col in [fuel_col, trans_col, seller_col, brand_col, model_col]:
        if col in input_df.columns:
            input_df[col] = 1

    input_df = input_df[model_columns]

    prediction = model.predict(input_df)[0]

    # Always show INR first
    st.success(f"Estimated Price: ₹{prediction:,.0f}")

    # Live currency conversion via external API
    if currency != "INR (₹)":
        try:
            response = requests.get(
                "https://api.exchangerate-api.com/v4/latest/INR",
                timeout=5
            )
            rates = response.json()['rates']

            currency_map = {
                "USD ($)": ("USD", "$"),
                "EUR (€)": ("EUR", "€"),
                "GBP (£)": ("GBP", "£")
            }

            code, symbol = currency_map[currency]
            converted = prediction * rates[code]
            st.info(f"≈ {symbol}{converted:,.2f} {code} (live exchange rate 🌐)")

        except Exception:
            st.warning("Live currency conversion unavailable right now. Showing INR only.")