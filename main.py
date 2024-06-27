import time
import argparse
from api.server import API
from config import __version__, api
from routes import blueprint_list
from features.kit import IntentKit

server = API(api['HOST'], api['PORT'])
server.register_blueprint_list(blueprint_list)

server.connected_client_text = "Conection from alex. Host \33[93m#addr#\33[32m connected"
server.disconnected_client_text = "Conection with alex. Host \33[93m#addr#\33[31m closed"

parser = argparse.ArgumentParser()

parser.add_argument("--list-routes", action="store_true", help="Will list all the routes installed")
parser.add_argument("-s", "--start", action="store_true", help="Start The server")
parser.add_argument("-t", "--train", action="store_true", help="Train the intent engine and exit")

parser.add_argument("-v", "--version", action="version", version=f"Alex Base Api {__version__}")

args = parser.parse_args()

if args.list_routes or args.start:
    if args.list_routes:
        for route in server.route_functions:
            print("\33[36mRoute:\33[32m", route, " \33[36mUp and running\33[0m")
    if args.start:
        if args.list_routes:
            time.sleep(2)
        server.serve()

elif args.train:
    time_stared = time.time()
    print("\33[34mRe-trainig everyting. This process take around 1 minute please wait...\33[0m")
    IntentKit().train()
    print("\33[93mTime Took:", time.time() - time_stared, "seconds")