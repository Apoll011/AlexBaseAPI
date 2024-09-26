import time
from random import choice, randint

import requests

def test_lib():
    url = "http://0.0.0.0:1178/version_control/lib/upload"

    for _ in range(50):
        file = {"file": open("README.md", "rb")}
        responce = requests.post(url=f"{url}?version={'.'.join(map(lambda x: str(x), (randint(1, 30), randint(1, 9), randint(1, 15))))}&lib_type={choice(['web', 'audio', 'language', 'model'])}", files=file)
        print(responce.json())

def test_alex():
    url = "http://0.0.0.0:1178/version_control/main/upload"

    for _ in range(20):
        file = {"file": open("README.md", "rb")}
        responce = requests.post(url=f"{url}?version={'.'.join(map(lambda x: str(x), (randint(1, 30), randint(1, 9), randint(1, 15))))}&platform={choice(['win', 'linux', 'macos'])}", files=file)
        print(responce.json())

test_lib()
test_alex()