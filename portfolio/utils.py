import requests

def fetch_share_names():
    return [
        (1,'APPLE'),
        (2,'AMAZ'),
        (3,'MIC'),
        (4,'TSL'),
    ]
    # response = requests.get('https://api.example.com/shares')  # Replace with your API URL
    # if response.status_code == 200:
    #     data = response.json()
    #     return [(share['id'], share['name']) for share in data]  # Adjust according to the API response structure
    # else:
    #     return []