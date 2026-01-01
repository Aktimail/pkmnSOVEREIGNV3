import json


data ={
    "nbFrames": 11,
    "framesDuration": 20,
    "loop": True
}

with open("../assets/data/dynamicsTiles/water.json", "w") as f:
    json.dump(data, f)