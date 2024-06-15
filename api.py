import json
import time

class Blueprint:
    defs = {
        
    }
    pre = ""
    def __init__(self, main_route = "") -> None:
        self.pre = main_route

    def route(self, route):
        def decorator(fun): 
            self.defs[self.pre + "/" + route] = fun
            def wrapper(*args, **kwargs):
                return fun(*args, **kwargs)
            return wrapper
        return decorator

class API:
    defs = {
        
    }
    def register_blueprint(self, blueprint: Blueprint):
        self.defs = blueprint.defs | self.defs

    def call(self, route, value):
        time_s = time.time()
        try:
            if route in self.defs.keys():
                return json.dumps({"responce": self.defs[route](value),"code": 200, "time": time.time() - time_s})
            else:
                return json.dumps({"responce": "invalid", "code": 404, "time":  time.time() - time_s})
        except Exception as e:
            return json.dumps({"responce": e.__str__(), "code": 400, "time":  time.time() - time_s})


