import requests
from django.conf import settings

def categorize_file(file_path):
    api_key = settings.ONDEMAND_IO_API_KEY
    url = "https://api.ondemand.io/v1/categorize"  # Replace with the actual API endpoint

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "file_path": file_path
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("category", "Uncategorized")
    except requests.exceptions.RequestException as e:
        print(f"Error calling OnDemand.io API: {e}")
        return "Uncategorized"
