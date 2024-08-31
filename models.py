from enum import Enum
from typing import List, Dict
from pydantic import BaseModel


class Gender(Enum):
    M = "M"
    F = "F"

class Body(BaseModel):
    genner: Gender
    age: int
    skin_tone: str
    height: str
    weight: str

class Citizenship(BaseModel):
    birth: str
    name: str
    nacionality: str

class Data(BaseModel):
    body: Body
    psycho_map: Dict[str, str] = {}
    citizenship: Citizenship

class Tag(BaseModel):
    label: str
    value: str

class User(BaseModel):
    name: str
    data: Data
    tags: List[List[Tag]] = []
    id: str

class Lang(str, Enum):
    EN = "en"
    PT = "pt"

class TagsSearch(BaseModel):
    query: str
    condition: str = ">:0"
    exclude: List[str] = []