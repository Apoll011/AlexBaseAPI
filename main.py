import os
import uvicorn
from models import *
from features.kit import *
from fastapi import FastAPI, Query
from config import __version__, api
from typing_extensions import Annotated, Literal

userKit = UserKit()
intentKit = IntentKit()
dictionaryKit = DictionaryKit()

app = FastAPI(title="Alex Server", version=__version__, description="Alex api server that handes complex and heavy tasks such an nlp user managements etc.", summary="Alex base server used for handling heavy functions", contact={"name": "Tiago Bernardo", "email": "tiagorobotik@gmail.com"}, license_info={"name": "Apache 2.0","url": "https://www.apache.org/licenses/LICENSE-2.0.html",}, on_startup=[intentKit.reuse, dictionaryKit.load])


"""
TO ADD:
/auth
"""
@app.get("/", name="Route")
async def roote():
    return {"name": "Alex"}


@app.get("/alex/alive", name="Check If Alive", description="This checks if alex is running and send the basic values")
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

@app.get("/intent_recognition/get/reuse", name="Load saved Engine", description="This will load teh saved intent recognition engine to memory")
async def intent_reuse():
    try:
        intentKit.reuse()
        return {"responce": True}
    except Exception:
        return {"responce": False}

@app.get("/intent_recognition/parse", name="Recognize intent from sentence", description="This will recognize the intent from a givin sentence and return the result parsed")
async def intent_reconize(text: Annotated[str, Query(max_length=250, min_length=2)]):
    try:
        return intentKit.parse(text)
    except AttributeError:
        return {"error": "Engine not trained"}

@app.get("/users/get/name", name="Search user by name")
async def user_search_name(name: Annotated[str, Query(max_length=65, min_length=2)]):
    return {"users": userKit.searchUser.by_name(name)}

@app.options("/users", name="Get all users ID")
async def get_users_id() -> List[str]:
    return userKit.all()

@app.get("/users/search/tags", name="Search users by tags", description="Will search user using the tags each one has. Query is the tags name, exclude is a list of ids the exclud from the result, condition is (The sign to compare to the intensity: <, >, <=, >=, !=, =):(the Intensity of the tag) ex query=Friend, exclude=['0000000001(Master user id)'], condition = '>:50'. will return all the more that 50% friends excluding the master user.")
async def user_search(search: TagsSearch): #FIXME: This bugs on browser 
    try:
        return {"users": userKit.searchUser.by_tags(search.query, search.condition, search.exclude)}
    except Exception:
        return {"error": "An error occurered"}

@app.get("/user/get", name="Get user object", description="gets an user object from a given id eg: 0815636592")
async def user_get(id: Annotated[str, Query(min_length=10)]):
    return userKit.getUser.by_id(id)

@app.put("/user/create", name="Create user", description="Will create an user from an user object")
async def user_create(user: User):
    try:
        userKit.createUser(user)
        return {"responce":True}
    except Exception as e:
        return {"error": f"Wont abble to create user ({e})"}

@app.delete("/user/delete", name="Delete user", description="Will delete an user from an given user id")
async def user_delete(id: str):
    responce = userKit.delete_user(id)
    return {"responce": responce}

@app.get("/dictionary/get", name="Get word from dictionary", description="Will return the definition of a given word. Return null if no match is found.")
async def dict_get(word: Annotated[str, Query(max_length=25, min_length=2)]):
    return dictionaryKit.get(word)

@app.get("/dictionary/get/closest", name="Get the closes match in Dictionary", description="Will get the closes match of the word found in the dictionary. and return it and others matches too. Return null if no match is found.")
async def dict_get_cosest(word: Annotated[str, Query(max_length=25, min_length=2)]):
    return dictionaryKit.get_closest(word)

@app.get("/dictionary/load", name = "Load the dictionary", description="Loads the dictionary file based on the given language.")
async def load_dic(lang:Lang = Lang.EN):
    try:
        dictionaryKit.load(lang)
        return {"responce": True}
    except Exception:
        return {"error": "Unable to load dictionary"}

@app.get("/close")
async def close():
    return {"responce": True}

if __name__ == "__main__":
    print("Started server process")
    print("Waiting for application startup.")
    print(f"App started on http://{api['HOST']}:{api['PORT']}")
    uvicorn.run(app, host=api["HOST"], port=api["PORT"], log_level="warning")