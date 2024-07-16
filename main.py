import time
import argparse
from api.server import API
from config import __version__, api
from routes import blueprint_list
from features.kit import IntentKit

server = API(api['HOST'], api['PORT'])
server.register_blueprint_list(blueprint_list)

server.client_name = "Alex"

parser = argparse.ArgumentParser()

parser.add_argument("-s", "--start", action="store_true", help="Start The server")
parser.add_argument("-t", "--train", action="store_true", help="Train the intent engine and exit")

parser.add_argument("-v", "--version", action="version", version=f"Alex Base Api {__version__}")

args = parser.parse_args()

if args.start or args.train:
    if args.train:
        time_stared = time.time()
        print("\33[34mRe-trainig everyting. This process take around 1 to 2 minutes please wait...\33[0m")
        IntentKit().train()
        print("\33[93mTime Took:", time.time() - time_stared, "seconds")
    
    if args.start:
        server.serve()