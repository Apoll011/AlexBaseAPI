import os
from features.intent_recognition import *
from kit import *
from api import Blueprint
from config import __version__

alex_blueprint = Blueprint("alex")
intent_blueprint = Blueprint("intent_recognition")
users_blueprint = Blueprint("users")
sound_blueprint = Blueprint("sound")

userKit = UserKit()

@alex_blueprint.route("alive")
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

@intent_blueprint.route("train")
def intent_train(value):
    return train(value)

@intent_blueprint.route("recoginze")
def intent_reconize(value):
    return recog(value["lang"], value["intent"])

@users_blueprint.route("search/name")
def user_search_name(value):
    return {"users": userKit.searchUser.by_name(value["query"])}

@users_blueprint.route("search/tags")
def user_serach(value):
    return {"users": userKit.searchUser.by_tags(value["query"], value["condition"], value["exclude"])}

@users_blueprint.route("get")
def user_get(value):
    return userKit.getUser.by_id(value)

@users_blueprint.route("create")
def user_create(value):
    return userKit.createUser(value)

@sound_blueprint.route("pt-pt/tts")
def ttsPT(value):
    return AudioKit.audio_pt.tts(value["text"])

@sound_blueprint.route("en-us/tts")
def ttsEN(value):
    return AudioKit.audio_en.tts(value["text"])

@sound_blueprint.route("pt-pt/stt")
def sttPT(value):
    return AudioKit.audio_pt.stt()

@sound_blueprint.route("en-us/stt")
def sttEN(value):
    return AudioKit.audio_en.stt()
