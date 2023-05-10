# %%

import math
import pickle
import subprocess
from datetime import date

import pandas as pd
import streamlit as st
from my_functions import load_dataset

subprocess.check_call(["python", "-m", "pip", "install", "click==7.1.2"])

st.title("Order Predictions Rotterdam")


@st.cache_data
def forecast_api(df):
    #   """Will return a frecast based on new opp data and your saved model"""
    with open("rain_prophet_model.pkl", "rb") as f:
        loaded_model = pickle.load(f)
    predictions = loaded_model.predict(df)
    return predictions


def create_test(date, rainfall):
    df = pd.DataFrame({"ds": [date], "add1": [rainfall * 0.1]})
    return df


def predict_rain(date_obj):
    df = load_dataset()
    month_number = date_obj.month
    maand_gemiddelde = df[df["date"].dt.month == month_number]["RH"].mean()
    return maand_gemiddelde


# create a Streamlit app
def main():
    min_date = date(2023, 1, 1)
    max_date = date(2023, 12, 31)

    future_date = st.date_input(
        "**Select a date in 2023**", min_value=min_date, max_value=max_date, value=min_date
    )

    st.write(
        "**If you do not enter any rainfall data, our model will make a rainfall prediction based on historic data*"
    )

    rainfall = st.number_input(
        "**Expected rain in mm:**", value=int(predict_rain(future_date))
    )  # int(mean(load_dataset()["RH"])))

    try:
        if rainfall < 0:
            raise ValueError("Rainfall can not be a negative number.")
        else:
            input = create_test(future_date, rainfall)
    except ValueError as e:
        st.warning("Error: " + str(e) + ". Please enter a non-negative number.")
        st.stop()

    prediction = forecast_api(input)

    st.write(
        "**The predicted number of orders:**", math.ceil(prediction.iloc[0, -1]), "orders"
    )  # ik rond de orders naar boven af


# run the app on streamlit
if __name__ == "__main__":
    main()

# %%
