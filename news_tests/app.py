import urllib
import json

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

KEY = "697684d3-9e9e-45e8-b3a4-b28ed5a741d9"
URL_STUB = "https://content.guardianapis.com/search?api-key="
URL = URL_STUB + KEY

@app.route("/", methods=["GET"])
def index():
    global data
    req = urllib.request.urlopen(URL)
    data = json.loads(req.read())
    return render_template("index.html", data=data, section = 'sport')

@app.route("/category", methods = ["POST"])
def get_category():
    global data
    if request.method == "POST":
        if request.form.get('category') == 'politics':        
            return render_template("index.html", data = data, section = 'SPORT')
        if request.form.get('category') == None:
            return redirect(url_for("index"))


if __name__ == "__main__":
    app.debug = True
    app.run()
