from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
app = FastAPI()
students={
    1:{
        "name":"john",
        "age":"12",
        "class1":"final year"
    }
}
class student(BaseModel):
    name:str
    age:int
    class1:str
    
# get Operations to "read data"
@app.get("/")
def root():
    return {"message": "Hello World"}

# pass a path parameter to get data
@app.get("/get-student{student_id}")
def root(student_id:int):
    return students[student_id]

# Combining the path Parameter and Query Parameter
@app.get("/get-name{student_id}")
def get_name(*,name:Optional[str]=None,student_id:int):
    for i in students:
        if students[i]["name"]==name:
            return students[i]
        return {"Data":"Not Found"}
        
        
# Post Operation is used to create data
@app.post("/create-student{student_id}")
def create_student(student_id:int,obj:student):
    if student_id in students:
        return {"Error":"Student exists"}
    
    students[student_id]=obj
    return students[student_id]
    
