import urllib
import json

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

KEY = "697684d3-9e9e-45e8-b3a4-b28ed5a741d9"
URL_STUB = "https://content.guardianapis.com/search?api-key="
URL = URL_STUB + KEY

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
    return render_template("index.html", data=data, section = s)

@app.route("/category", methods = ["POST"])
def get_category():
    global data, l
    if request.method == "POST":
        for i in l:
            print(i['sectionName'])
            if i['sectionName'] == request.form.get('category'):
                print('found')
                print(i['webTitle'], i['sectionName'])
        return request.form.get('category')
        if request.form.get('category') == 'Society':        
            return render_template("index.html", data = data, section = 'SPORT')
        if request.form.get('category') == None:
            return redirect(url_for("index"))
    return("hello")

if __name__ == "__main__":
    app.debug = True
    app.run()
