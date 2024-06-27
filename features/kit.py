import io
import os
import json

from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_EN
from features.user_backend import SearchUsers, CreateUsers, GetUsers

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
  