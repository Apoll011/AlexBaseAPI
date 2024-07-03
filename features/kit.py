import io
import os
import json
from math import exp
from difflib import get_close_matches
from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_EN
from features.user_backend import SearchUsers, CreateUsers, GetUsers

class DictionaryKit:
    
    dictionary = {}
    loaded = False

    def load(self, language = "en"):
        if not self.loaded:
            self.dictionary = json.load(open(f"./features/dictionary/language/{language}.json"))
            self.loaded = True

    def get(self, word):
        try:
            h = word.lower()
            return {"name": h, "definition": self.dictionary[h], "confidence": 1.0}
        except Exception as e:
            return {"name": None, "confidence": 1.0}

    def get_closest(self, word):
        result = get_close_matches(word, self.dictionary.keys())
        if len(result)>0:
            r = {"name": result[0], "definition": self.dictionary[result[0]], "confidence": self.softmax_confidence(len(result)), "others": result}
            return r
        else:
            return {"name": None, "confidence": 0.75}

    def softmax_confidence(self, number, t:int = 1) -> float:
        a = [number, 1]
        new = list(map(lambda x: exp(x/t), a))
        s = sum(new)
        return list(map(lambda x: x/s, new))[0]

    
class IntentKit:
    engine = None
    def __init__(self):
        pass
    
    def reuse(self):
        if self.engine == None:
            self.engine = SnipsNLUEngine.from_path("./features/intent_recognition/snips/engine/")

    def train(self):
        os.system("snips-nlu generate-dataset en ./features/intent_recognition/snips/data/en.yaml > ./features/intent_recognition/snips/dataset/dataset_en.json")
        with io.open("./features/intent_recognition/snips/dataset/dataset_en.json") as f:
            dataset = json.load(f)
        self.engine = SnipsNLUEngine(config=CONFIG_EN)
        self.engine.fit(dataset)
        os.system("rm -rf ./features/intent_recognition/snips/engine")
        self.engine.persist("./features/intent_recognition/snips/engine/")

    def parse(self, text):
        return self.engine.parse(text)


class UserKit:
    users = []
    def __init__(self) -> None:
        for user in os.listdir("./features/user_backend/users"):
            us = open("./features/user_backend/users/"+user, "r")
            self.users.append(json.load(us))
        
        self.searchUser = SearchUsers(self.users)
        self.getUser = GetUsers(self.users)
        self.createUser = CreateUsers
  