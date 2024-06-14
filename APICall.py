import json
import socket

class ApiCall:
    HOST = "127.0.0.1"
    PORT = 1178
    
    def __init__(self) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen()

    def call_route(self, route, value = ""):
        self.conn.send(json.dumps({"route": route.encode("utf-8"), "value": value.encode("utf-8")}))
        return self.get_info()
    
    def get_info(self):
        while True:
            data = self.conn.recv(1024)
            if not data:
                continue
            break
        received_json = json.loads(data.decode("utf-8"))
        return received_json

    def connect(self):
        self.conn, self.addr = self.server_socket.accept()

    def disconect(self):
        self.conn.close()


api = ApiCall()
api.connect()
print(api.call_route("alex/alive"))
api.disconect()
