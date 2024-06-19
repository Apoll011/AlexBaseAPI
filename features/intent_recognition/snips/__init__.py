import io
import json

from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_EN

class IntentKit:
    def __init__(self):
        pass
    
    def reuse(self):
        self.engine = SnipsNLUEngine.from_path("./features/intent_recognition/snips/engine/")

    def train(self):
        with io.open("./features/intent_recognition/snips/dataset/dataset.json") as f:
            dataset = json.load(f)
        self.engine = SnipsNLUEngine(config=CONFIG_EN)
        self.engine.fit(dataset)
        self.engine.persist("./features/intent_recognition/snips/engine/")

    def parse(self, text):
        return self.engine.parse(text)
