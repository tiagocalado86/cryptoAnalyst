from time import sleep
import requests

while True:
    try:
        response = requests.get("http://localhost:8000/fetch-data")
        if response.status_code == 200:
            print("Data fetched successfully.")
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    sleep(300)