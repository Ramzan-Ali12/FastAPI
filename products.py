from fastapi import FastAPI
from pydantic import BaseModel
import httpx

app = FastAPI()

class InputData(BaseModel):
    merchant_id: str

# make route to create data
@app.post("/Products/")
async def products(input: InputData):
    # extract input data
    merchant_id = input.merchant_id

    # make a request to Apideck API to fetch product data
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": "Bearer sk_live_78c1d411-f826-43a3-b1e7-e19b6e4813d4-8Hw5HgmPPZxoocmuTyOE-4c4644b5-a9f1-45af-923e-798ace556d18"}
        url = f"https://api.apideck.com/hub/clover/v3/merchants/{merchant_id}/items"
        response = await client.get(url, headers=headers)

        # raise an exception if the API request failed
        response.raise_for_status()

        # extract the product data from the response
        product_data = response.json()

    # return the product data as the result
    return {"result": product_data}
