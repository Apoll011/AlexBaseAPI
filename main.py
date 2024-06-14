import os
import json
import socket

from features.intent_recognition import *
from kit import *
from api import API

__version__ = "3.8"
 
api = API()
userKit = UserKit()

@api.route("alex/alive")
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

@api.route("intent_recognition/train")
def intent_train(value):
    return train(value)

@api.route("intent_recognition/recoginze")
def intent_reconize(value):
    return recog(value["lang"], value["intent"])

@api.route("users/search/name")
def user_search_name(value):
    return {"users": userKit.searchUser.by_name(value["query"])}

@api.route("users/search/tags")
def user_serach(value):
    return {"users": userKit.searchUser.by_tags(value["query"], value["condition"], value["exclude"])}

@api.route("users/get")
def user_get(value):
    return userKit.getUser.by_id(value)

@api.route("users/create")
def user_create(value):
    return userKit.createUser(value)

@api.route("sound/pt-pt/tts")
def ttsPT(value):
    return AudioKit.audio_pt.tts(value["text"])

@api.route("sound/en-us/tts")
def ttsEN(value):
    return AudioKit.audio_en.tts(value["text"])

@api.route("sound/pt-pt/stt")
def sttPT(value):
    return AudioKit.audio_pt.stt()

@api.route("sound/en-us/stt")
def sttEN(value):
    return AudioKit.audio_en.stt()

def main():
    try:
        HOST = "127.0.0.1"
        PORT = 1178
        
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        
        closed = False
        
        while not closed:
            conn, addr = server_socket.accept()
            
            with conn:
                print(f"Alex of host {addr} connected")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        continue
                    received_json = json.loads(data.decode("utf-8"))
                    if received_json["route"] == "close" and  received_json["value"] == "Alex.Server" :
                        conn.close()
                        closed = True
                        break
                    response = api.call(received_json["route"], received_json["value"])
                    print(response)
                    conn.send(response.encode("utf-8"))
                    conn.close()
                    break
                
        print("Exiting...")
        server_socket.close()
    except KeyboardInterrupt:
        print("Exiting...")
        server_socket.close()

main()
