import glob
import os.path

import lingua_franca
import uvicorn
from starlette.responses import FileResponse, JSONResponse
from models import *
from kit import *
from fastapi import FastAPI, File, Query, UploadFile
from config import __version__, api
from typing_extensions import Annotated

userKit = UserKit()
intentKit = IntentKit()
dictionaryKit = DictionaryKit()

app = FastAPI(title="Alex Server", version=__version__, description="Alex api server that handles complex and heavy tasks such an nlp user managements etc.", summary="Alex base server used for handling heavy functions", contact={"name": "Tiago Bernardo", "email": "tiagorobotik@gmail.com"}, license_info={"name": "Apache 2.0","url": "https://www.apache.org/licenses/LICENSE-2.0.html",}, on_startup=[intentKit.reuse, dictionaryKit.load])

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
            "trained": list(filter(lambda e: e.endswith(".yaml"),os.listdir("./features/intent_recognition/snips/data/"))), 
            "instaled": list(filter(lambda e: e.endswith(".json"),os.listdir("./features/intent_recognition/snips/dataset/"))), 
        },
        "version": __version__
        }
    return responce

@app.get("/intent_recognition/engine", name="Train or Reuse the Intent Recognition Engine")
async def intent_train(type: IntentRecongnitionEngineTrainType = IntentRecongnitionEngineTrainType.REUSE):
    try:
        if type == IntentRecongnitionEngineTrainType.REUSE:
            intentKit.reuse()
        else:
            intentKit.train()
        return {"responce": True}
    except Exception:
        return {"responce": False}

@app.get("/intent_recognition/", name="Recognize intent from sentence", description="This will recognize the intent from a givin sentence and return the result parsed")
async def intent_reconize(text: Annotated[str, Query(max_length=250, min_length=2)]):
    try:
        return intentKit.parse(text)
    except AttributeError:
        return {"error": "Engine not trained"}

@app.options("/users", name="Get all users ID")
async def get_users_id() -> List[str]:
    return userKit.all()

@app.get("/users/search/name", name="Search user by name")
async def user_search_name(name: Annotated[str, Query(max_length=65, min_length=2)]):
    return {"users": userKit.search_by_name(name)}

@app.get("/users/search/tags", name="Search users by tags", description="Will search user using the tags each one has. Query is the tags name, exclude is a list of ids the exclud from the result, condition is (The sign to compare to the intensity: <, >, <=, >=, !=, =):(the Intensity of the tag) ex query=Friend, exclude=['0000000001(Master user id)'], condition = '>:50'. will return all the more that 50% friends excluding the master user.")
async def user_search(query: Annotated[str, Query(max_length=25, min_length=2)], condition: Annotated[str, Query(max_length=6, min_length=3)] = ">:0", exclude=None):
    if exclude is None:
        exclude = []
    try:
        return {"users": userKit.search_by_tags(query, condition, exclude)}
    except Exception:
        return {"error": "An error occurred"}

@app.get("/user/", name="Get user object", description="gets an user object from a given id eg: 0815636592")
async def user_get(id: Annotated[str, Query(min_length=10)]):
    return userKit.get(id)

@app.put("/user/", name="Create user", description="Will create an user from an user object")
async def user_create(user: User):
    try:
        userKit.createUser(user)
        return {"responce":True}
    except Exception as e:
        return {"error": f"Wont abble to create user ({e})"}

@app.delete("/user/", name="Delete user", description="Will delete an user from an given user id")
async def user_delete(id: str):
    responce = userKit.delete_user(id)
    return {"responce": responce}

@app.get("/dictionary/get", name="Get word from dictionary", description="Will return the definition of a given word. Return null if no match is found.")
async def dict_get(word: Annotated[str, Query(max_length=25, min_length=2)]):
    return dictionaryKit.get(word)

@app.get("/dictionary/get/closest", name="Get the closes match in Dictionary", description="Will get the closes match of the word found in the dictionary. and return it and others matches too. Return null if no match is found.")
async def dict_get_closest(word: Annotated[str, Query(max_length=25, min_length=2)]):
    return dictionaryKit.get_closest(word)

@app.get("/dictionary/load", name = "Load the dictionary", description="Loads the dictionary file based on the given language.")
async def load_dic(lang:Lang = Lang.EN):
    try:
        dictionaryKit.load(lang)
        return {"responce": True}
    except FileNotFoundError:
        return {"error": "Unable to load dictionary"}

@app.get("/close")
async def close():
    return {"responce": True}

@app.post("/version_control/main/upload")
async def main_upload(file: UploadFile = File(...), version = "-1.1.1", platform = PlatformType.LINUX):
    chunk = 1024 * 5
    if platform == PlatformType.LINUX:
        extension = ".zip"
    elif platform == PlatformType.MACOS:
        extension = ".app"
    else:
        extension = ".exe"

    try:
        if os.path.isfile(f"./features/version_controller/main/alex.v{version}{extension}"):
            return {"error": "Already exists"}

        with open(f"./features/version_controller/main/alex.v{version}{extension}", "wb") as f:
            while contents := file.file.read(chunk * chunk):
                f.write(contents)
    except Exception as e:
        return {"error": e}
    finally:
        file.file.close()

    return {"responce": True}

@app.post("/version_control/lib/upload")
async def lib_upload(lib_type: LibType, file: UploadFile = File(...), version = "-1.1.1", platform = PlatformType.LINUX):
    chunk = 1024 * 5

    try:
        if os.path.isfile(f"./features/version_controller/lib/{lib_type}.v{version}.zip"):
            return {"error": "Already exists"}

        with open(f"./features/version_controller/lib/{lib_type}.v{version}.zip", "wb") as f:
            while contents := file.file.read(chunk * chunk):
                f.write(contents)
    except Exception as e:
        return {"error": e}
    finally:
        file.file.close()

    return {"responce": True}

@app.get("/version_control/main/last")
def main_last(platform = PlatformType.LINUX):
    bigger = None
    name = None
    if platform == PlatformType.LINUX:
        extension = ".zip"
    elif platform == PlatformType.MACOS:
        extension = ".app"
    else:
        extension = ".exe"

    files = list(map(lambda x: x.split("/")[-1].rstrip(extension),glob.glob(f"./features/version_controller/main/*{extension}")))

    for main_core in files:
        version = main_core.split(".v")[1]
        version_core_tuple = tuple(map(lambda v: int(v), version.split(".")))
        if (bigger and version_core_tuple > bigger) or bigger is None:
            bigger = version_core_tuple
            name = main_core
    return {"name": name + extension if name is not None else None, "version": bigger, "versions": files}

@app.get("/version_control/main/get")
async def main_get(platform = PlatformType.LINUX):
    l = main_last(platform)
    if l["name"] is not None:
        return FileResponse(f"./features/version_controller/main/{l['name']}", media_type="application/octet-stream", filename=l["name"])
    else:
        return JSONResponse({"error": "Not Found"}, status_code=404)

@app.get("/version_control/lib/last")
def lib_last(lib_type: LibType):
    bigger = None
    name = None

    files = list(map(lambda x: x.split("/")[-1].rstrip(".zip"),glob.glob(f"./features/version_controller/lib/{lib_type}*.zip")))

    for lib_core in files:
        version = lib_core.split(".v")[1]
        version_core_tuple = tuple(map(lambda v: int(v), version.split(".")))
        if (bigger and version_core_tuple > bigger) or bigger is None:
            bigger = version_core_tuple
            name = lib_core
    return {"name": name + ".zip" if name is not None else None , "version": bigger, "versions": files}

@app.get("/version_control/lib/get")
async def lib_get(lib_type: LibType):
    l = lib_last(lib_type)
    if l["name"] is not None:
        return FileResponse(f"./features/version_controller/lib/{l['name']}", media_type="application/octet-stream", filename=l["name"])
    else:
        return JSONResponse({"error": "Not Found"}, status_code=404)

@app.get("/get")
async def get():
    return FileResponse("features/alex.sh")


def lock_pid():
    pid = os.getpid()
    with open('/home/pegasus/.alex_server', "x") as pidfile:
        pidfile.write(str(pid))

def clean():
    os.system("rm /home/pegasus/.alex_server")

def main():
    print("Started server process")
    print("Waiting for application startup.")
    print(f"App started on http://{api['HOST']}:{api['PORT']}")
    uvicorn.run(app, host=api["HOST"], port=api["PORT"], log_level="warning")

if __name__ == "__main__":
    try:
        lock_pid()
        main()
    except Exception:
        pass
    clean()