import urllib
import json
import sqlite3

from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

from util import api_to_db

app = Flask(__name__)

KEY = "697684d3-9e9e-45e8-b3a4-b28ed5a741d9"
URL_STUB = "https://content.guardianapis.com/search?api-key="
URL = URL_STUB + KEY
DB_FILE = "database.db"

try: api_to_db.createTable()
except: pass

#get what to display in form
@app.route("/", methods=["GET"])
def index():
    global data, l
    req = urllib.request.urlopen(URL)
    data = json.loads(req.read())    
    l = data['response']['results']
    s = set()
    #get the different sections, but no repeats. Thus using a set
    for i in l:
       s.add(i['sectionName'])
    #clear the table of its other entries for this json   
    api_to_db.clearTable()
    api_to_db.insertAPI('Guardian', datetime.today(), str(l), KEY)
    return render_template("index.html", data=data, section = s)

#get category, render in template
@app.route("/category", methods = ["POST"])
def get_category():
    global data, l
    if request.method == "POST":
        category = request.form.get('category')
        return render_template("selection.html", category = category, data = data)

if __name__ == "__main__":
    app.debug = True
    app.run()
