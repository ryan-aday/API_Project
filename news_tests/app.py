import urllib
import json
import sqlite3

from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

KEY = "697684d3-9e9e-45e8-b3a4-b28ed5a741d9"
URL_STUB = "https://content.guardianapis.com/search?api-key="
URL = URL_STUB + KEY
DB_FILE = "database.db"

#function to create a table for apis
def createTable():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("CREATE TABLE apis (api TEXT, timestamp TEXT, data TEXT, key TEXT)")
    db.commit()
    db.close()

try: createTable()
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
    clearTable()
    insertAPI('Guardian', datetime.today(), str(l), KEY)
    return render_template("index.html", data=data, section = s)

#get category, render in template
@app.route("/category", methods = ["POST"])
def get_category():
    global data, l
    if request.method == "POST":
        category = request.form.get('category')
        return render_template("selection.html", category = category, data = data)


#insert an API's info into the data table 'apis'
def insertAPI(api, timestamp, data, key):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    params = (api, timestamp, data, key)
    c.execute("INSERT INTO apis VALUES(?, ?, ?, ?)", params)
    db.commit()
    db.close()
    return True

#clear table function
def clearTable():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("delete from apis")
    db.commit()
    db.close()

if __name__ == "__main__":
    app.debug = True
    app.run()
