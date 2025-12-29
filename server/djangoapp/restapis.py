import os
import requests
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("backend_url", default="http://localhost:3030")
SENTIMENT_ANALYZER_URL = os.getenv(
    "sentiment_analyzer_url", default="http://localhost:5050/"
)


def get_request(endpoint, **kwargs):
    """
    Perform a GET request to the backend with optional query parameters.
    """
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"

    request_url = f"{BACKEND_URL}{endpoint}?{params}"
    print(f"GET from {request_url}")

    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as err:
        print(f"Network exception occurred: {err}")
        return None


def analyze_review_sentiments(text):
    """
    Analyze sentiment of a given text using the sentiment analyzer service.
    """
    request_url = f"{SENTIMENT_ANALYZER_URL}analyze/{text}"

    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as err:
        print(f"Network exception occurred: {err}")
        return None
    except Exception as err:
        print(f"Unexpected error: {err}")
        return None


def post_review(data_dict):
    """Post a review dictionary to the backend API."""
    request_url = f"{BACKEND_URL}/insert_review"

    try:
        response = requests.post(request_url, json=data_dict)
        response.raise_for_status()
        print(response.json())
        return response.json()
    except requests.RequestException as err:
        print(f"Network exception occurred: {err}")
        return None
    except Exception as err:
        print(f"Unexpected error: {err}")
        return None
