import json

data = { 1: {"name" : "Eric Lin", "Count": 10},
         2: {"name" : "Stanley Chen", "Count": 10}}

with open('stuff.json', 'w') as fp:
    json.dump(data, fp)

