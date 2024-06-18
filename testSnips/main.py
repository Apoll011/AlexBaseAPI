import io
import json
import time

from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_EN

time_ie_od = time.time()
engine = SnipsNLUEngine(config=CONFIG_EN)

with io.open("./testSnips/dataset.json") as f:
    dataset = json.load(f)
finish_ie_od = time.time() - time_ie_od

time_train = time.time()
engine.fit(dataset)
finish_trian = time.time() - time_train

print(finish_ie_od, finish_trian)

while True:
    time_parse = time.time()
    parsing = engine.parse(input("Sentence: "))
    finish_parse = time.time() - time_parse
    print(json.dumps(parsing, indent=2), finish_parse)