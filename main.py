import os
import json
import socket

from features.intent_recognition import *
from features.user_backend import SearchUsers, CreateUsers, GetUsers
from features.audio_processing import Audio

__version__ = "3.8"

users = []
for user in os.listdir("./features/user_backend/users"):
	us = open("./features/user_backend/users/"+user, "r")
	users.append(json.load(us))

SearchUser = SearchUsers(users)
GetUser = GetUsers(users)
CreateUser = CreateUsers
audio_pt = Audio("pt-pt")
audio_en = Audio("en-us")
   
def index():
    return {
        "on": True,
        "users": len(users), 
        "lang": {
            "trained": list(map(lambda e: e[6:-5], list(filter(lambda e: e.endswith(".json"),os.listdir("./intents/graphs/"))))), 
            "instaled": list(map(lambda e: e[9:-4], list(filter(lambda e: e.endswith(".ini"),os.listdir("./intents/sentences/"))))), 
        },
        "version": __version__
        }
        
def process(json_data):
    if json_data["action"] == "alive":
        return json.dumps({"responce": index()})
    elif json_data["action"] == "train":
        return json.dumps({"responce": {"done": train(json_data["value"])}})
    elif json_data["action"] == "intent":
        return json.dumps({"responce": recog(json_data["value"]["lang"], json_data["value"]["intent"])})
    elif json_data["action"] == "search":
        return json.dumps({"responce":  {"users": SearchUser.by_name(json_data["value"]["query"]) if json_data["value"]["by"] == "name" else SearchUser.by_tags(json_data["value"]["query"], json_data["value"]["value"], json_data["value"]["exclude"])}})
    elif json_data["action"] == "get":
        return json.dumps({"responce":  {"users": GetUser.by_id(json_data["value"])}})
    elif json_data["action"] == "create":
        return json.dumps({"responce":  {"done": CreateUser(json_data["value"])}})
    elif json_data["action"] == "stt":
        return json.dumps({"responce":  audio_pt.stt() if json_data["value"] == "pt-pt" else audio_en.stt()})
    elif json_data["action"] == "tts":
        return json.dumps({"responce":  {"done": audio_pt.tts(json_data["value"]["text"]) if json_data["value"]["lang"] == "pt-pt" else audio_en.tts(audio_pt.tts(json_data["value"]["text"]))}})
    else:
        return json.dumps({"responce": "invalid"})

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
                    if received_json["action"] == "close" and  received_json["value"] == "Alex.Server" :
                        conn.close()
                        closed = True
                        break
                    response = process(received_json)
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
