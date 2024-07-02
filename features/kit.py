import io
import os
import re
import json
import wikipedia
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_EN
from features.user_backend import SearchUsers, CreateUsers, GetUsers

class DictionaryKit:
    dictionary = {}

    def load(self, language = "en"):
        print("Preparing to load dic elements")
        for dic in os.listdir(f"./features/dictionary/language/{language}"):
            dic_name = dic.replace(".dic", "").replace(".", " ").strip()
            context = "" if not dic_name.endswith(")") else re.sub(r'.* (.*)', r'\1', dic_name)
            sn = dic_name.replace(context, "").replace("()","").strip()
            h = hash(sn.lower())
            try:
                with open(f"./features/dictionary/language/{language}/{dic}", "r", encoding="utf-8") as c:
                    content = c.read()
                    cont = content.split("\n")[0]
            except Exception:
                with open(f"./features/dictionary/language/{language}/{dic}", "r", encoding="windows-1252") as c:
                    content = c.read()
                    cont = content.split("\n")[0]
            
            self.dictionary[h] = {"small_name":sn , "name": dic_name, "ctx": context.replace("(", "").replace(")", ""), "definition": cont}

        print(f"Loaded {len(self.dictionary)} elements")

    def get(self, name):
        try:
            h = hash(name.lower())
            return self.dictionary[h]
        except Exception as e:
            return {"name": None}

    def get_closest(self, name, confidence_threshold=0.5):
        closest_match = {"name": None}
        closest_confidence = 0
        for h, entry in self.dictionary.items():
            sm = SequenceMatcher(None, name.lower(), entry["small_name"].lower())
            confidence = sm.ratio()
            if confidence > closest_confidence and confidence >= confidence_threshold:
                closest_match = entry
                closest_confidence = confidence
        return closest_match

    def download_from_wikipedia(self):
        wikipedia.set_lang("en")
        while True:
            topic = input("Enter a topic (or 'random' for a random page): ")
            if topic.lower() == "random":
                while True:
                    try:
                        topic = wikipedia.random(pages=1)
                        print(f"Downloading {topic}...")
                        page = wikipedia.page(topic).summary
                        file_name = topic.replace(" ", ".").lower() + ".dic"
                        file_path = f"./features/dictionary/language/en/{file_name}"
                        if not os.path.exists(file_path):
                            with open(file_path, "w", encoding="utf-8") as f:
                                f.write(page)
                            print(f"Saved {file_name} to disk.")
                    except KeyboardInterrupt:
                        print("Stopping download...")
                        break
                    except wikipedia.exceptions.DisambiguationError as e:
                        print(f"Disambiguation error: {e}")
                    except wikipedia.exceptions.PageError as e:
                        print(f"Page error: {e}")
            else:
                try:
                    pages = wikipedia.search
                    page = wikipedia.page(topic, auto_suggest=True).summary
                    file_name = topic.replace(" ", "") + ".dic"
                    file_path = f"./features/dictionary/language/en/{file_name}"
                    if not os.path.exists(file_path):
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(page)
                        print(f"Saved {file_name} to disk.")
                except wikipedia.exceptions.DisambiguationError as e:
                    print(f"Disambiguation error: {e}")
                except wikipedia.exceptions.PageError as e:
                    print(f"Page error: {e}")
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
  