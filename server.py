import os
import json
import shutil
import socket
from api import API
from config import api
from api.routes import users_blueprint, alex_blueprint, intent_blueprint, sound_blueprint



class ApiServer:
    
    server_socket: socket.socket

    HOST: str
    PORT: int

    closed: bool

    def __init__(self) -> None:
        self.define_route()
        self.start_api()

        self.closed = False

    def define_route(self):
        self.HOST = api["HOST"]
        self.PORT = api["PORT"]

    def start_api(self):
        self.api = API()
        self.register_api_blueprints()

    def register_api_blueprints(self):
        self.api.register_blueprint(alex_blueprint)
        self.api.register_blueprint(users_blueprint)
        self.api.register_blueprint(intent_blueprint)
        self.api.register_blueprint(sound_blueprint)

    def print_header_text(self, text, size = 2):
        s = (size + 1)
        terminal_size = shutil.get_terminal_size().columns
        border_size = (terminal_size - len(text) - 2) // s  # 2 is for spaces
        print("\33[91m-" * border_size, f"\33[36m{text}\33[91m", "-" * border_size, "\33[97m")

    def serve(self):
        os.system("clear")
        try:
            self.start_server()
            self.print_header_text(f"Started API Server on address \33[93m{self.HOST}:{self.PORT}", 1)
            
            self.main_loop()
            
            self.server_socket.close()
        except KeyboardInterrupt:
            self.server_socket.close()

        self.print_header_text(f"Closed API Server", 1)

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen()
    
    def main_loop(self):
        while not self.closed:
            conn, addr = self.server_socket.accept()
            with conn:
                self.conect_client(conn, addr)

    def conect_client(self, conn, addr):
        print(f"\33[32mConection from alex. Host \33[93m{addr}\33[32m connected\33[0m")
        self.client_main_loop(conn)
        print(f"\33[31mConection with alex. Host \33[93m{addr}\33[31m closed\33[0m")

    def client_main_loop(self, conn):
        while True:
            data = conn.recv(1024)
            
            if not data:
                continue

            received_json = json.loads(data.decode("utf-8"))
            
            if received_json["route"] == "close" and  received_json["value"] == "Alex.Server" :
                conn.close()
                self.closed = True
                break
            
            response = self.api.call(received_json["route"], received_json["value"])
            conn.send(response.encode("utf-8"))
            conn.close()
            break