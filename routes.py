import os
from features.intent_recognition import *
from kit import *
from api import Blueprint
from config import __version__

main = Blueprint()

userKit = UserKit()

@main.route("alex/alive")
def alive(value):
    return {
        "on": True,
        "users": len(userKit.users), 
        "lang": {
            "trained": list(map(lambda e: e[6:-5], list(filter(lambda e: e.endswith(".json"),os.listdir("./intents/graphs/"))))), 
            "instaled": list(map(lambda e: e[9:-4], list(filter(lambda e: e.endswith(".ini"),os.listdir("./intents/sentences/"))))), 
        },
        "version": __version__
        }

@main.route("intent_recognition/train")
def intent_train(value):
    return train(value)

@main.route("intent_recognition/recoginze")
def intent_reconize(value):
    return recog(value["lang"], value["intent"])

@main.route("users/search/name")
def user_search_name(value):
    return {"users": userKit.searchUser.by_name(value["query"])}

@main.route("users/search/tags")
def user_serach(value):
    return {"users": userKit.searchUser.by_tags(value["query"], value["condition"], value["exclude"])}

@main.route("users/get")
def user_get(value):
    return userKit.getUser.by_id(value)

@main.route("users/create")
def user_create(value):
    return userKit.createUser(value)

@main.route("sound/pt-pt/tts")
def ttsPT(value):
    return AudioKit.audio_pt.tts(value["text"])

@main.route("sound/en-us/tts")
def ttsEN(value):
    return AudioKit.audio_en.tts(value["text"])

@main.route("sound/pt-pt/stt")
def sttPT(value):
    return AudioKit.audio_pt.stt()

@main.route("sound/en-us/stt")
def sttEN(value):
    return AudioKit.audio_en.stt()
