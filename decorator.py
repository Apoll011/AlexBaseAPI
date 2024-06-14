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
            return self.defs[route](value)
        else:
            raise AttributeError(name=f"{route} was not defined as a route for this API.")

api = API()

@api.route("text")
def stringJoin(value): 
    st = value
    return st

@api.route("number")
def summation(value): 
    summ = int(value)
    return summ + 1

print(api.call("number", "1"))

