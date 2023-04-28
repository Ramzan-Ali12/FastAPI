import requests

# Replace with your Apideck and Clover API credentials
APIDECK_CLIENT_ID = "NNhWoev4UwmT6mU8cHHQRWVr2dkkE4fQOFCcHHQ"
APIDECK_CLIENT_SECRET = "sk_live_e4bb5545-75f0-4868-9d4f-9dbf3d4a0901-TrIamTCyA39uksc4QIR4-5435b73c-efec-468f-becf-2a0bfce00a39"
CLOVER_MERCHANT_ID = "Z5HAS8KMKP9G1"
CLOVER_API_KEY = "6E0YKH0S1NYV0"
CLOVER_API_SECRET = "431e0117-6d88-2c81-f2ef-ad46f893752c"

# Authenticate with Apideck
auth_url = "https://connect.apideck.com/oauth/token"
auth_params = {
    "grant_type": "client_credentials",
    "client_id": APIDECK_CLIENT_ID,
    "client_secret": APIDECK_CLIENT_SECRET
}
auth_response = requests.post(auth_url, data=auth_params,verify=False)

if auth_response.status_code == 200:
    # Extract the access token from the authentication response
    access_token = auth_response.json().get("access_token")

    # Make an API request to the Clover inventory items endpoint
    inventory_items_url = f"https://api.apideck.com/clover/{CLOVER_MERCHANT_ID}/inventory_items"
    inventory_items_headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Clover-Auth": f"{CLOVER_API_KEY}:{CLOVER_API_SECRET}"
    }
    inventory_items_response = requests.get(inventory_items_url, headers=inventory_items_headers)

    if inventory_items_response.status_code == 200:
        # Extract the product data from the inventory items response
        products = inventory_items_response.json().get("data")
        print(products)
    else:
        print(f"Error retrieving inventory items: {inventory_items_response.status_code}")
else:
    print(f"Error authenticating with Apideck: {auth_response.status_code}")
