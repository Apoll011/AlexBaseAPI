import json
class API:
    defs = {
        
    }
    def route(self, route):
        def decorator(fun): 
            self.defs[route] = fun
            def wrapper(*args, **kwargs):
                return fun(*args, **kwargs)
            return wrapper
        return decorator

    def call(self, route, value):
        if route in self.defs.keys():
            return json.dumps({"responce": self.defs[route](value)})
        else:
            return json.dumps({"responce": "invalid"})
