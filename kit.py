import io
import os
import json
import uuid
from math import exp
from difflib import get_close_matches
from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_EN, CONFIG_PT_PT

class DictionaryKit:
    
    dictionary = {}
    loaded = False

    def load(self, language = "en"):
        if not self.loaded:
            path = f"./features/dictionary/language/{language}"
            if os.path.isfile(f"{path}_full.json"):
                path += "_full"
            path += ".json"

            with open(path, "r") as dicti:
                self.dictionary = json.load(dicti)
            
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
            r = {"name": result[0], "definition": self.dictionary[result[0]], "confidence": self.softmax_confidence(len(result)), "others": result[1:]}
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
    loaded = False
    def __init__(self):
        self.lang = None
    
    def reuse(self, lang = "en"):
        if self.lang != lang:
            self.lang = lang
            self.engine = SnipsNLUEngine.from_path(f"./features/intent_recognition/snips/engine/{lang}")
            self.loaded = True

    def train(self, lang = "en"):
        test = "en" if lang=="en" else "pt_pt"
        os.system(f"snips-nlu generate-dataset {test} ./features/intent_recognition/snips/data/{lang}.yaml > ./features/intent_recognition/snips/dataset/dataset_{lang}.json")
        with io.open(f"./features/intent_recognition/snips/dataset/dataset_{lang}.json") as f:
            dataset = json.load(f)
        
        if self.engine is not None:
            del self.engine
        self.engine = SnipsNLUEngine(config=CONFIG_EN if lang == "en" else CONFIG_PT_PT)
        self.engine.fit(dataset)
        os.system(f"rm -rf ./features/intent_recognition/snips/engine/{lang}/")
        self.engine.persist(f"./features/intent_recognition/snips/engine/{lang}")
        self.loaded = True
        self.lang = lang

    def parse(self, text):
        if isinstance(self.engine, SnipsNLUEngine):
            return self.engine.parse(text)
        else:
            raise Exception("Intent recognition Engine not loaded")

class UserKit:
    users = []
    ids = []
    def __init__(self) -> None:
        self.update()

    def update(self):
        self.users = []
        for user in os.listdir("./features/user_backend/users"):
            us = json.load(open("./features/user_backend/users/"+user, "r"))
            self.users.append(us)
            self.ids.append(us['id'])

    def get(self, id: str):
        if id is not None:
            users = []
            for user in self.users:
                if type(id) != list:
                    #print(u)
                    if user["id"] == id:
                        return user
                else:
                    for ii in id:
                        if user["id"] == ii:
                            users.append(user)
            return users
        else:
            return None

    def createUserFuntion(self, user_data):
        user = json.loads(user_data.replace("'", "\""))
        user["id"] = str(uuid.uuid4())
        with open("./features/user_backend/users/"+user["id"]+".user", 'a') as ui:
            json.dump(user, ui)

    def createUser(self, user_data):
        self.createUserFuntion(user_data=user_data)
        self.update()

    def update_user(self, user_data):
        user = json.loads(user_data.replace("'", "\""))
        with open("./features/user_backend/users/"+user["id"]+".user", 'w') as ui:
            json.dump(user, ui)
        self.update()

    def delete_user(self, id):
        try:
            os.system(f"rm ./features/user_backend/users/{id}.user")
            self.update()
            return True
        except:
            return False
    
    def all(self):
        return self.ids
    
    def search_by_name(self, query):
        result = []
        for user in self.users:
            if query in user["name"]:
                result.append(user["id"])
        return result
    
    def search_by_tags(self, query, condition =">:0", exclude=None):
        if exclude is None:
            exclude = []
        result = []
        condition_parsed = {
            "symbol": condition.split(":")[0],
            "value": int(condition.split(":")[1])
        }
        for user in self.users:
            if user["id"] in exclude:
                continue
            else:
                for tag in user["tags"]:
                    query_list:list[str] = query if type(query) == list else [query] # type: ignore
                    tag[1] = int(tag[1])
                    for individual_query in query_list:
                        if individual_query.lower() == tag[0].lower():
                            if condition_parsed["symbol"] == ">":
                                if tag[1] > condition_parsed["value"]:
                                    result.append(user["id"])
                            elif condition_parsed["symbol"] == "<":
                                if tag[1] < condition_parsed["value"]:
                                    result.append(user["id"])
                            elif condition_parsed["symbol"] == ">=" or condition_parsed["symbol"] == "=>":
                                if tag[1] >= condition_parsed["value"]:
                                    result.append(user["id"])
                            elif condition_parsed["symbol"] == "<=":
                                if tag[1] <= condition_parsed["value"]:
                                    result.append(user["id"])
                            elif condition_parsed["symbol"] == "!=":
                                if tag[1] != condition_parsed["value"]:
                                    result.append(user["id"])
                            elif condition_parsed["symbol"] == "=":
                                if tag[1] == condition_parsed["value"]:
                                    result.append(user["id"])
        return result