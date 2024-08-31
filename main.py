import os
import uvicorn
from features.kit import *
from config import __version__  
from fastapi import FastAPI, Query

app = FastAPI(title="Alex Server", version=__version__, description="Alex api server that handes complex and heavy tasks such an nlp user managements etc.", summary="Alex base server used for handling heavy functions", contact={"name": "Tiago Bernardo", "email": "tiagorobotik@gmail.com"}, license_info={"name": "Apache 2.0","url": "https://www.apache.org/licenses/LICENSE-2.0.html",})

userKit = UserKit()
intentKit = IntentKit()
dictionaryKit = DictionaryKit()

@app.get("/alex/alive", name="Check If Alive", description="This checks if ale is running and send the basic values")
async def alive():
    responce = {
        "on": True,
        "kit": {
            "all_on": True and intentKit.loaded and  dictionaryKit.loaded,
            "user": True,
            "intent": intentKit.loaded,
            "dictionary": dictionaryKit.loaded
        },
        "users": len(userKit.users), 
        "lang": {
            "trained": list(map(lambda e: e[6:-5], list(filter(lambda e: e.endswith(".yaml"),os.listdir("./features/intent_recognition/snips/data/"))))), 
            "instaled": list(map(lambda e: e[9:-4], list(filter(lambda e: e.endswith(".json"),os.listdir("./features/intent_recognition/snips/dataset/"))))), 
        },
        "version": __version__
        }
    return responce

@app.get("/intent_recognition/get/train", name="Train the Intent Recognition Engine")
async def intent_train():
    return {"responce": intentKit.train()}

@app.get("/intent_recognition/get/reuse")
async def intent_reuse():
    try:
        intentKit.reuse()
        return {"responce": True}
    except Exception:
        return {"responce": False}

@app.get("/intent_recognition/parse")
def intent_reconize(text: str):
    return intentKit.parse(text)

@app.get("/users/get/name")
def user_search_name(name: str):
    return {"users": userKit.searchUser.by_name(name)}

@app.get("/users/search/tags")
def user_search(value: dict):
    if "condition" in value.keys() and "exclude" in value.keys():
        return {"users": userKit.searchUser.by_tags(value["query"], value["condition"], value["exclude"])}
    elif "condition" in value.keys():
        return {"users": userKit.searchUser.by_tags(value["query"], value["condition"])}
    elif "exclude" in value.keys():
        return {"users": userKit.searchUser.by_tags(value["query"], exclue=value["exclude"])}
    elif  "query" not in value.keys():
        return {"error": "Query required"}
    else:
        return {"users": userKit.searchUser.by_tags(value["query"])}

@app.get("/user/get")
def user_get(id: str):
    return userKit.getUser.by_id(id)

@app.get("/user/create")
def user_create(user):
    return userKit.createUser(user)

@app.get("/dictionary/get")
def dict_get(word: str):
    return dictionaryKit.get(word)

@app.get("/dictionary/get/closest")
def dict_get_cosest(word:str):
    return dictionaryKit.get_closest(word)

@app.get("/dictionary/load")
def load_dic():
    dictionaryKit.load()
    return {"responce": True}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
