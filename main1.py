

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class InputData(BaseModel):
    category: str
    topic: str
    age: int





def process_text_with_Moviedb(category: str, topic: str, age: int) -> str:
    @app.post("/Moviedb/")
    async def process_text(input_data: InputData):
        # extract input data
        category = input_data.category
        topic = input_data.topic
        age = input_data.age

        # process the input text using the GPT model
        result = process_text_with_Moviedb(category, topic, age)

        # return the result
        return {"result": result}