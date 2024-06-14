import json
import socket

class ApiCall:
    HOST = "127.0.0.1"
    PORT = 1178
    
    def __init__(self) -> None:
        pass

    def call_route(self, route, value = ""):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            d = {"route": route, "value": value}
            s.connect((self.HOST, self.PORT))
            s.send(bytes(json.dumps(d).encode("utf-8")))
            return self.get_info(s)
    
    def get_info(self, s):
        while True:
            data = s.recv(1024)
            if not data:
                continue
            break
        received_json = json.loads(data.decode("utf-8"))
        return received_json


api = ApiCall()
print(api.call_route("intent_recognition/recoginze", {"lang": "pt-pt", "text": "aumentar volume"}))
 