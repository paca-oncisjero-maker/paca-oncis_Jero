import requests
import json

# Replace this URL with your classmate's Render endpoint
url = "https://flask-miranda-act4-1.onrender.com/campus"

try:
    response = requests.get(url, timeout=30)

    # Check HTTP status code
    print("Status Code:", response.status_code)

    if response.status_code == 200:
        data = response.json()

        print("\nJSON Response:")
        print(json.dumps(data, indent=4))

        print("\nMeaningful Data:")

        if isinstance(data, dict):
            for key, value in list(data.items())[:3]:
                print(f"{key}: {value}")

        elif isinstance(data, list):
            for item in data[:3]:
                print(item)

        else:
            print(data)

    else:
        print("Request failed.")
        print("Response:", response.text)

except requests.exceptions.RequestException as e:
    print("Connection error:", e)

except ValueError:
    print("Invalid JSON response.")
