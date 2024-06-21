from server import ApiServer
from config import __version__
import argparse
import time

server = ApiServer()

parser = argparse.ArgumentParser()

parser.add_argument("--list-routes", action="store_true", help="Will list all the routes installed")
parser.add_argument("-s", "--start", action="store_true", help="Start The server")

parser.add_argument("-v", "--version", action="version", version=f"Alex Base Api {__version__}")

args = parser.parse_args()

if args.list_routes or args.start:
    if args.list_routes:
        for route in server.api.defs:
            print("\33[36mRoute:\33[32m", route, " \33[36mUp and running\33[0m")
    if args.start:
        if args.list_routes:
            time.sleep(2)
        server.serve()
