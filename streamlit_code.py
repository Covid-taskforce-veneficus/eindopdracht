
import math
import pickle
from datetime import date
from fbprophet import Prophet

import pandas as pd
import streamlit as st

st.title("Prediction orders Rotterdam")


@st.cache_data
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

    future_date = st.sidebar.date_input(
        "Select a date in 2023", min_value=min_date, max_value=max_date, value=min_date
    )

    rainfall = st.sidebar.number_input("Expected rain in mm:", value=0)

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
