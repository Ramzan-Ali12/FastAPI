from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from fastapi import FastAPI
from pydantic import BaseModel
from langchain.llms import OpenAI
import os
from typing import List
import requests
import random

app = FastAPI()

class InputData(BaseModel):
    category: str
    topic: str
    age: int

os.environ["OPENAI_API_KEY"] = "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"
os.environ['TMDB_API_KEY']= "f71f3c34619b78598760fbd515bf4c07"


def process_text_with_moviedb(category: str, topic: str, age: int) -> List[str]:
    

    return None




def process_text_with_gpt(category: str, topic: str, age: int) -> str:
    # get the OpenAI API key from environment variable
    llm = OpenAI(temperature=0.9)

    prompt = PromptTemplate(
        input_variables=["product"],
        template="You need to generate the 5 multiple choice questions and 1 correct option about the {product}?\n1. \n a) \n b) \n c) \n d) \nAnswer: ",
    )

    # create an instance of the language model chain
    chain = LLMChain(llm=llm, prompt=prompt)

    # generate quiz questions using the language model
    string = chain.run(topic)
    lines = string.split("\n")

    # parse the quiz questions and store them in a list
    quizObject = []
    questionIndex = 0
    for line in lines:
        # skip empty lines and lines that contain only whitespace
        if not line.strip():
            continue
        if line.startswith("Answer:") or line.startswith("Correct Answer:"):
            continue
        if (line[0].isdigit() and line[1] == '.') or (line[1].isdigit() and line[0] == 'Q') or (line.startswith("Question ")) or (line.startswith("Q:")) :
            quizObject.append({
                "question": line,
                "options": [],
                "answer": ""
            })
            questionIndex += 1
        elif line[0].isalpha() and line[1] == '.':
            if len(quizObject) > questionIndex - 1:
                quizObject[questionIndex - 1]["options"].append(line)
        elif line.startswith("Answer:"):
            if len(quizObject) > questionIndex - 1:
                quizObject[questionIndex - 1]["answer"] = line[8:]
        elif line.startswith("Correct Answer:"):
            if len(quizObject) > questionIndex - 1:
                quizObject[questionIndex - 1]["answer"] = line[16:]

    # return the quiz questions as JSON
    return quizObject



@app.post("/process_text/")
async def process_text(input_data: InputData):
    # extract input data
    category = input_data.category
    topic = input_data.topic
    age = input_data.age

    # process the input text using the appropriate method based on category
    if category == "movies":
        result = process_text_with_moviedb(category, topic, age)
    else:
        result = process_text_with_gpt(category, topic, age)

    # return the result
    return {"result": result}


