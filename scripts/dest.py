# import json
from pprint import pprint
import os
import sys

sys.path.insert(1, os.path.realpath(os.path.curdir))

from data.output.destination import dests
from agent_traveler.libs.extract_update_data import update_destination

# dest_path = "./data/output/destination.json"

# with open(dest_path, "r") as file:
#     data = file.read()

# dests = json.loads(data)
pprint(dests)
