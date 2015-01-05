import os
import json


with open(os.path.join(os.path.dirname(__file__), 'courses.json')) as file:
    data = json.load(file)