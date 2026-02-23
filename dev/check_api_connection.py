import requests

BASE_URL = "https://environment.data.gov.uk/hydrology/id"

def test_connection():
    url = f"{BASE_URL}/stations"
    response = requests.get(url)

    print("Status code:", response.status_code)

    if response.status_code == 200:
        print("Connection successful")
    else:
        print("Connection failed")


if __name__ == "__main__":
    test_connection()
