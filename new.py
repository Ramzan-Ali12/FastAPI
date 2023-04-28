import json
import requests
from fastapi import FastAPI
from datetime import datetime
app = FastAPI()

# Replace with your Apideck and Clover API credentials
APIDECK_CLIENT_ID = "KBD5H4Z3RNHJZJQpPIg5EbJXEGEH0x4HmXpPIg"
APIDECK_CLIENT_SECRET = "sk_live_e06710dc-4a64-453c-a786-92efcc3878bd-TNgSiONEZbgc3mjQ53Ju-f99b8a43-5237-4b4d-9aad-1eab4df47ff5"
CLOVER_MERCHANT_ID = "Z5HAS8KMKP9G1"
CLOVER_API_KEY = "6E0YKH0S1NYV0"
CLOVER_API_SECRET = "431e0117-6d88-2c81-f2ef-ad46f893752c"

@app.get("/orders")
async def get_orders(start_time: int, end_time: int):
    # Authenticate with Clover
    auth_url = "https://apisandbox.dev.clover.com/oauth/token"
    auth_params = {
        "client_id": APIDECK_CLIENT_ID,
        "client_secret": APIDECK_CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    # auth_response = requests.post(auth_url, params=auth_params)
    auth_response = requests.post(auth_url, data=json.dumps(auth_params))
    print(auth_response.json())
    if auth_response.status_code == 200:
        # Extract the access token from the authentication response
        access_token = auth_response.json().get("access_token")
        if not access_token:
            return {"error": "No access token found in authentication response"}

        # Make an API request to the Clover orders endpoint with modifiedTime filter
        orders_url = f"https://apisandbox.dev.clover.com/v3/merchants/{CLOVER_MERCHANT_ID}/orders"
        orders_params = {
            "modifiedTime>": start_time,
            "modifiedTime<": end_time
        }
        orders_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        orders_response = requests.get(orders_url, params=orders_params, headers=orders_headers)

        if orders_response.status_code == 200:
            # Extract the order data from the response
            orders = orders_response.json().get("elements")
            if not orders:
                return []
            return orders
        else:
            return {"error": f"Error retrieving orders: {orders_response.status_code}"}
    else:
        return {"error": f"Error authenticating with Clover: {auth_response.status_code}"}
