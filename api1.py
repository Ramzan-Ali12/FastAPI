from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from fastapi import FastAPI
from pydantic import BaseModel
from langchain.llms import OpenAI
import os
import requests
app = FastAPI()

class InputData(BaseModel):
    category: str
    topic: str
    age: int


os.environ["OPENAI_API_KEY"] = "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"
#Generate Quiz questions using moviedb
def process_text_with_moviedb(category: str, topic: str, age: int)->str:
    # Set the TMDB API key
    tmdb_api_key= "f71f3c34619b78598760fbd515bf4c07"
    base_url = "https://api.themoviedb.org/3"
    
 

    # Return the quiz questions as JSON
    return 

#Generate Quiz questions using Open Ai
def process_text_with_gpt(category: str, topic: str, age: int) -> str:
    # get the OpenAI API key from environment variable
    os.environ["OPENAI_API_KEY"] = "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"
    llm = OpenAI(temperature=0.9)

    prompt = PromptTemplate(
        input_variables=["product"],
        template="You need to generate the 5 multiple choice questions and 1 correct option about the {product}?",
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
        print(line)
        # skip empty lines
        if line == '':
            continue
        if (line[0].isdigit() and line[1] != '.') and (line[0].isalpha() and line[1] != '.') and (not line.startswith("Answer:")) and (not line.startswith("Correct Answer:")):
            continue
        # create a dictionary for each quiz question
        if (line[0].isdigit() and line[1] == '.') or (line[1].isdigit() and line[0] == 'Q') or (line.startswith("Question ")) or (line.startswith("Q:")) :
            quizObject.append({
                "question": line,
                "options": [],
                "answer": ""
            })
            questionIndex += 1

        # assign options to the options array of the current question
        if line[0].isalpha() and line[1] == '.':
            quizObject[(questionIndex-1)]["options"].append(line)

        # assign the answer to the answer key of the current question
        # if line.startswith("Answer:") or line.startswith("Correct Answer:"):
        #     line = line.replace("Correct Answer: ","")
        #     line = line.replace("Answer: ", "")
        #     quizObject[(questionIndex-1)]["answer"] = line
        # assign the answer to the answer key of the current question
        if not (line[0].isdigit() and line[1] == '.') and not (line.startswith("Question ") or line.startswith("Q:")):
            quizObject[(questionIndex-1)]["answer"] = line


    # return the quiz questions as JSON
    return quizObject

@app.post("/process_text/")
async def process_text(input_data: InputData):
    # extract input data
    category = input_data.category
    topic = input_data.topic
    age = input_data.age

    # process the input text using the appropriate method based on category
    if category == "movie":
        result = process_text_with_moviedb(category, topic, age)
    else:
        result = process_text_with_gpt(category, topic, age)

    # return the result
    return {"result": result}

