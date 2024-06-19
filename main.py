import json
import socket
from api import API
from api.routes import users_blueprint, alex_blueprint, intent_blueprint, sound_blueprint

api = API()
api.register_blueprint(alex_blueprint)
api.register_blueprint(users_blueprint)
api.register_blueprint(intent_blueprint)
api.register_blueprint(sound_blueprint)

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
                print(f"Conection from alex. Host {addr} connected")
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
                    conn.send(response.encode("utf-8"))
                    conn.close()
                    break
                
        print("Exiting...")
        server_socket.close()
    except KeyboardInterrupt:
        print("Exiting...")
        server_socket.close()

main()
