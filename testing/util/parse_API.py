import urllib.request
import json

def explanation():
    data={}
    with open("dataset.json", "r") as read_file:
        data = json.load(read_file)
    return data["response"]["results"]


def video():
    data={}
    with open("dataset.json", "r") as read_file:
        data = json.load(read_file)
    return data["url"]
