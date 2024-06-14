import json

class Blueprint:
    defs = {
        
    }
    def route(self, route):
        def decorator(fun): 
            self.defs[route] = fun
            def wrapper(*args, **kwargs):
                return fun(*args, **kwargs)
            return wrapper
        return decorator

class API(Blueprint):
    def register_blueprint(self, blueprint: Blueprint):
        self.defs = blueprint.defs
    def call(self, route, value):
        if route in self.defs.keys():
            return json.dumps({"responce": self.defs[route](value)})
        else:
            return json.dumps({"responce": "invalid"})


