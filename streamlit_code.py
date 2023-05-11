# %%

import json
import math
import subprocess
from datetime import date, datetime

import requests
import streamlit as st
from my_functions import load_dataset

subprocess.check_call(["python", "-m", "pip", "install", "click==7.1.2"])

st.title("Order Predictions Rotterdam")


def getpred(data):
    #   """Will return a frecast based on new opp data and your saved model"""
    url = "http://a99039b5-4106-4fed-99b9-9f6523e66d05.westeurope.azurecontainer.io/score"
    response = requests.post(url, json=data)
    return response.json()["Prediction"]


def date_converter(o):
    if isinstance(o, datetime):
        return o.__str__()


def create_test(date_str, rainfall):
    data = {"ds": [date_str], "add1": [rainfall * 0.1]}
    return json.dumps(data, default=date_converter)


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
        "**Select a date in 2023:**", min_value=min_date, max_value=max_date, value=min_date
    )

    st.write(
        "**If you do not enter any rainfall data, our model will make a rainfall prediction based on historic data*"
    )

    rainfall = st.number_input("**Expected rain in mm:**", value=int(predict_rain(future_date)))

    try:
        if rainfall < 0:
            raise ValueError("Rainfall can not be a negative number.")
        else:
            input = create_test(str(future_date), rainfall)
    except ValueError as e:
        st.warning("Error: " + str(e) + ". Please enter a non-negative number.")
        st.stop()

    input_json = json.loads(input)

    prediction = getpred(input_json)

    st.write(
        "**The predicted number of orders:**", st.write(math.floor(prediction), style={'font-size': '100px'})
    )  # ik rond de orders naar boven af


# run the app on streamlit
if __name__ == "__main__":
    main()

# %%
