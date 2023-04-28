from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/products")
def get_products():
    url = "https://api.clover.com/v3/merchants/{6E0YKH0S1NYV0}/items"
    headers = {"Authorization": "Bearer {your_access_token}"}
    response = requests.get(url, headers=headers)
    print(response.json())
    if response.status_code == 200:
        products = response.json()["elements"]
        return products
    else:
        return {"error": "Unable to retrieve products."}
# write a function that add three numbers