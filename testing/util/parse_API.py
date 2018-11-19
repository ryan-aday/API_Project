import urllib.request
import json

def explanation():
    data={}
    with open("dataset.json", "r") as read_file:
        data = json.load(read_file)
    return data["explanation"]


def video():
    data={}
    with open("dataset.json", "r") as read_file:
        data = json.load(read_file)
    return data["url"]

def title():
    data={}
    with open("dataset.json", "r") as read_file:
        data = json.load(read_file)
    return data.get("title", "None")

def version():
    data={}
    with open("dataset.json", "r") as read_file:
        data = json.load(read_file)
    return data.get("version", "None")

def media_type():
    data={}
    with open("dataset.json", "r") as read_file:
        data = json.load(read_file)
    return data.get("media_type", "None")

def imagesun():
    data={}
    with open("sundataset.json", "r") as read_file:
        data = json.load(read_file)
    return data.get("image", "None")
