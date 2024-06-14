import json

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
        if route in self.defs.keys():
            return json.dumps({"responce": self.defs[route](value)})
        else:
            return json.dumps({"responce": "invalid"})


