import math
import pickle
from datetime import date
from statistics import mean

import pandas as pd
import streamlit as st
from my_functions import load_dataset

import subprocess
subprocess.check_call(["python", "-m", "pip", "install", "click==7.1.2"])

st.title("Prediction orders Rotterdam")


@st.cache
def forecast_api(df):
    #   """Will return a frecast based on new opp data and your saved model"""
    with open("VAR_Prophet_Model.pkl", "rb") as f:
        loaded_model = pickle.load(f)
    predictions = loaded_model.predict(df)
    return predictions


def create_test(date, rainfall):
    df = pd.DataFrame({"ds": [date], "add1": [rainfall * 0.1]})
    return df


# create a Streamlit app
def main():
    min_date = date(2023, 1, 1)
    max_date = date(2023, 12, 31)

    future_date = st.date_input(
        "Select a date in 2023", min_value=min_date, max_value=max_date, value=min_date
    )

    rainfall = st.number_input("Expected rain in mm:", value=int(mean(load_dataset()["RH"])))

    if rainfall < -1:
        st.warning("Negative numbers are not allowed.")
    else:
        output = create_test(future_date, rainfall)

    prediction = forecast_api(output)

    st.write(
        "Prediction orders:", math.ceil(prediction.iloc[0, -1])
    )  # ik rond de orders naar boven af


# run the app
if __name__ == "__main__":
    main()
