import json

with open('stuff.json') as fp:
    data = json.load(fp)
print data
print data["1"]["name"]
