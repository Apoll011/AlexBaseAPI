import os
from features.intent_recognition.snips import IntentKit
from kit import *
from api import Blueprint
from config import __version__
import time

alex_blueprint = Blueprint("alex")
intent_blueprint = Blueprint("intent_recognition")
users_blueprint = Blueprint("users")
sound_blueprint = Blueprint("sound")

userKit = UserKit()
intentKit = IntentKit()

@alex_blueprint.route("alive")
def alive(value):
    return {
        "on": True,
        "users": len(userKit.users), 
        "lang": {
            "trained": list(map(lambda e: e[6:-5], list(filter(lambda e: e.endswith(".json"),os.listdir("./features/intent_recognition/intents/graphs/"))))), 
            "instaled": list(map(lambda e: e[9:-4], list(filter(lambda e: e.endswith(".ini"),os.listdir("./features/intent_recognition/intents/sentences/"))))), 
        },
        "version": __version__
        }

@intent_blueprint.route("get/train")
def intent_train(value):
    return intentKit.train()

@intent_blueprint.route("get/reuse")
def intent_train(value):
    return intentKit.reuse()


@intent_blueprint.route("parse")
def intent_reconize(value):
    return intentKit.parse(value)

@users_blueprint.route("search/name")
def user_search_name(value):
    return {"users": userKit.searchUser.by_name(value["query"])}

@users_blueprint.route("search/tags")
def user_search(value: dict):
    if "condition" in value.keys() and "exclude" in value.keys():
        return {"users": userKit.searchUser.by_tags(value["query"], value["condition"], value["exclude"])}
    elif "condition" in value.keys():
        return {"users": userKit.searchUser.by_tags(value["query"], value["condition"])}
    elif "exclude" in value.keys():
        return {"users": userKit.searchUser.by_tags(value["query"], exclue=value["exclude"])}
    elif  "query" not in value.keys():
        raise "QueryIsNecessary"
    else:
        return {"users": userKit.searchUser.by_tags(value["query"])}


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