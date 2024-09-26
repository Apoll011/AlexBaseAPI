from enum import Enum
from fastapi import Query
from typing import List, Dict
from pydantic import BaseModel
from typing_extensions import Annotated


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

class User(BaseModel):
    name: str
    data: Data
    tags: List[List[str]] = []

class Lang(str, Enum):
    EN = "en"
    PT = "pt"

class PlatformType(str, Enum):
    LINUX = "linux"
    MACOS = "macos"
    WINDOWS = "win"

class LibType(str, Enum):
    WEB = "web"
    AUDIO = "audio"
    LANGUAGE = "language"
    MODEL = "model"

class IntentRecongnitionEngineTrainType(str, Enum):
    TRAIN = "train"
    REUSE = "reuse"