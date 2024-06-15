import json
import socket
from promise import Promise

class ApiCall:
    HOST = "127.0.0.1"
    PORT = 1178

    def __init__(self):
        pass

    def call_route(self, route, value=""):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.HOST, self.PORT))
        d = {"route": route, "value": value}
        s.send(bytes(json.dumps(d).encode("utf-8")))
        promise = Promise()
        promise.resolve(lambda: self.get_info(s, promise))
        return promise

    def get_info(self, s, promise):
        try:
            data = s.recv(1024).decode("utf-8")
            promise.resolve(lambda: json.loads(data))
            s.close()  # Close the socket object
        except socket.error as e:
            promise.reject(e)
            s.close()  # Close the socket object
        except json.JSONDecodeError as e:
            promise.reject(e)
            s.close()  # Close the socket object

api = ApiCall()
p = api.call_route("intent_recognition/recognize", {"lang": "pt-pt", "text": "aumentar volume"})

p.then(lambda data: print("Success:", data))
p.catch(lambda error: print("Error:", error))

print("djdnj")