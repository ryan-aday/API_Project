#Team RanQuoR-Turkey
#P01 - ArRESTed Development oh dear
#Period 7
#2018-11-18


import urllib.request, json
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
        return render_template('index.html')

if (__name__) == "__main__":
    app.debug = True
    app.run()
