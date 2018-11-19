#Ryan Aday
#K26 - APIs
#Period 7
#2018-11-14

import urllib.request
import json
from flask import Flask, render_template
from util import parse_API

app = Flask(__name__)#Creates an instance of Flask

@app.route('/')
def reroute():
        url='https://content.guardianapis.com/search?api-key=c6f7002f-00e5-43fe-9a95-57504e62f4e0'
        with urllib.request.urlopen(url) as testfile, open('dataset.json', 'w') as f:
            f.write(testfile.read().decode())

        return render_template("index.html")

if (__name__) == "__main__":#if this file is run directly then the Flask app will run
    app.debug = True#allows changes to directly affect local host without rerunning app
    app.run()
