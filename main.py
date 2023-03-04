import requests
from datetime import datetime
import os

GENDER = "male"
WEIGHT = 77
HEIGHT = 176
AGE = 26

NUTRITIONIX_APP_ID = os.environ.get("ENV_NIX_APP_ID")
NUTRITIONIX_API_KEY = os.environ.get("ENV_NIX_API_KEY")

sheety_endpoint = os.environ.get("ENV_SHEETY_ENDPOINT")
exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheety_auth = os.environ.get("ENV_SHEETY_TOKEN")

exercise_input = input("What exercises did you do today? ")

today_date = datetime.now().strftime("%d/%m/%Y")
today_time = datetime.now().strftime("%H:%M:%S")


nutritionix_headers = {
    "x-app-id": NUTRITIONIX_APP_ID,
    "x-app-key": NUTRITIONIX_API_KEY,
    "x-remote-user-id": "0",
}


exercise_parameters = {
    "query": exercise_input,
    "gender": GENDER,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE
}


exercise_response = requests.post(url=exercise_endpoint, json=exercise_parameters, headers=nutritionix_headers)
result = exercise_response.json()

sheety_headers = {
    "Authorization": sheety_auth
}

for item in result["exercises"]:
    exercise = item["name"].title()
    duration = item["duration_min"]
    calories = item["nf_calories"]
    sheety_parameters = {
        "workout": {
            "date": today_date,
            "time": today_time,
            "exercise": exercise,
            "duration": duration,
            "calories": calories,
        }
    }

    sheety_response = requests.post(url=sheety_endpoint, json=sheety_parameters, headers=sheety_headers)
