from pydantic import BaseModel

class Query(BaseModel):
    question: str
    name:str
    file1:str
    file2:str


class Evaluation(BaseModel):
    is_acceptable: bool
    feedback: str