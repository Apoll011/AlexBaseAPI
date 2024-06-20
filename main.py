import os
import json
import shutil
import socket
from api import API
from api.routes import users_blueprint, alex_blueprint, intent_blueprint, sound_blueprint

api = API()
api.register_blueprint(alex_blueprint)
api.register_blueprint(users_blueprint)
api.register_blueprint(intent_blueprint)
api.register_blueprint(sound_blueprint)

def print_header_text(text, size = 2):
    s = (size + 1)
    terminal_size = shutil.get_terminal_size().columns
    border_size = (terminal_size - len(text) - 2) // s  # 2 is for spaces
    print("\33[91m-" * border_size, f"\33[36m{text}\33[91m", "-" * border_size, "\33[97m")

def main():
    os.system("clear")
    try:
        HOST = "127.0.0.1"
        PORT = 1178
        
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print_header_text(f"Started API Server on address \33[93m{HOST}:{PORT}", 1)
        closed = False
        
        while not closed:
            conn, addr = server_socket.accept()
            
            with conn:
                print(f"\33[34mConection from alex. Host \33[93m{addr}\33[34m connected\33[0m")
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
                print(f"\33[31mConection with alex. Host \33[93m{addr}\33[31m closed\33[0m")
                
        
        server_socket.close()
    except KeyboardInterrupt:
        server_socket.close()

    print_header_text(f"Closed API Server", 1)
main()
