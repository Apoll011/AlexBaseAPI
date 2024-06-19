import io
import json
import os

from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_EN

class IntentKit:
    def __init__(self):
        pass
    
    def reuse(self):
        self.engine = SnipsNLUEngine.from_path("./features/intent_recognition/snips/engine/")

    def train(self):
        os.system("snips-nlu generate-dataset en ./features/intent_recognition/snips/data/en.yaml > ./features/intent_recognition/snips/dataset/dataset_en.json")
        with io.open("./features/intent_recognition/snips/dataset/dataset_en.json") as f:
            dataset = json.load(f)
        print(dataset)
        self.engine = SnipsNLUEngine(config=CONFIG_EN)
        print("ddd")
        self.engine.fit(dataset)
        print("dd")
        print(self.engine.parse("Hi"))
        os.system("rm -rf ./features/intent_recognition/snips/engine")
        self.engine.persist("./features/intent_recognition/snips/engine/")

    def parse(self, text):
        return self.engine.parse(text)
