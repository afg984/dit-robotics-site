import os
import json
import itertools


weekdays = 'MTWRFS'
classsects = '1234n56789abc'
times = tuple(''.join(p) for p in itertools.product(weekdays, classsects))
times_as_table = tuple(tuple(w + s for s in classsects) for w in weekdays)


with open(os.path.join(os.path.dirname(__file__), 'courses.json')) as file:
    data = json.load(file)