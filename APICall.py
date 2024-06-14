import json
import socket
import threading

class Promise:
    def __init__(self):
        self.resolved = False
        self.rejected = False
        self.value = None
        self.error = None
        self.then_callback = None
        self.catch_callback = None

    def then(self, callback):
        if self.resolved:
            callback(self.value)
        else:
            self.then_callback = callback
        return self

    def catch(self, callback):
        if self.rejected:
            callback(self.error)
        else:
            self.catch_callback = callback
        return self

    def resolve(self, value):
        threading.Thread(target=self.do_resolve, args=(value,)).start()

    def do_resolve(self, value):
        if not self.resolved and not self.rejected:
            v = value()
            if v:
                self.value = v
                self.resolved = True
                if self.then_callback:
                    self.then_callback(v)

    def reject(self, error):
        if not self.rejected and not self.resolved:
            self.rejected = True
            self.error = error
            if self.catch_callback:
                self.catch_callback(error)

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
p = api.call_route("intent_recognition/recoginze", {"lang": "pt-pt", "text": "aumentar volume"})

p.then(lambda data: print("Success:", data))
p.catch(lambda error: print("Error:", error))

print("djdnj")