#Team RanQuoR-Turkey
#P01 - ArRESTed Development oh dear
#Period 7
#2018-11-18


import urllib.request, json

from flask import Flask, render_template
from flask import request, session #login function
from flask import url_for, redirect, flash #redirect functions

from util import apiOperator, dbOperator

app = Flask(__name__)

app.secret_key = "asdfadsfjskdfjqweruioqwerjlkasdjfl;asdjfadlksfkjlfdsjkldfsjkl"

IPAPI = "https://ipapi.co/json/"

URL_STUB = "http://api.openweathermap.org/data/2.5/weather?q="
ADD = "&units=imperial"
API_KEY = "&appid=87bdad31331cad64c1efc0c13526c6f8"

TEST_MULT = "https://samples.openweathermap.org/data/2.5/find?q=London&appid=b1b15e88fa797225412429c1c50c122a1r&units=imperial"

icons = {'01d': "sun", '01n': "moon", # clear sky
         '02d': "cloud-sun", '02n': "cloud-moon", # few clouds
         '03d': "cloud-sun", '03n': "cloud-moon", # scattered clouds
         '04d': "cloud", '04n': "cloud", # broken clouds
         '09d': "cloud-rain", '09n': "cloud-rain", # shower rain
         '10d': "cloud-showers-heavy", '10n': "cloud-showers-heavy", # rain
         '11d': "bolt", '11n': "bolt", # thunderstorm
         '13d': "snowflake", '13n': "snowflake", # snow
         '50d': "smog", '50n': "smog", # mist
}

@app.route("/", methods=['GET','POST'])
def root():
    if not (request.method == 'GET'):
        
        l=request.form['symbl']
        print(l)
        if not l:
            return redirect('/')
        dbOperator.modifyStock(l,1)
        return redirect("/")

    
    f = urllib.request.urlopen(IPAPI).read()
    d = json.loads(f)
    CITY = d["city"]
    
    print(CITY)

    print(URL_STUB + urllib.parse.quote(CITY) + ADD + API_KEY)

    response = urllib.request.urlopen(URL_STUB + urllib.parse.quote(CITY) + ADD + API_KEY)
    o = json.loads(response.read())

    print(list(o.keys()))
    print(o)

    if 'count' in o:
        print(o['list'][0]['weather'])

        o = o['list'][0]

        return render_template("index.html",
                               title = o['name'],
                               weather_main = o['weather'],
                               temp_now = o['main']['temp'],
                               temp_min = o['main']['temp_min'],
                               temp_max = o['main']['temp_max'],
                               icons = icons,
                               entry = apiOperator.stockRetrieve(dbOperator.retrieveStock())
            )

    else:
        print(o['weather'])

        return render_template("index.html",
                               title = o['name'],
                               weather_main = o['weather'],
                               temp_now = o['main']['temp'],
                               temp_min = o['main']['temp_min'],
                               temp_max = o['main']['temp_max'],
                               icons = icons,
                               entry = apiOperator.stockRetrieve(dbOperator.retrieveStock())
            )

@app.route("/choices", methods=["GET"])
def choic():

    q = request.args.get('creditcard')
    if q:
        matches=apiOperator.alphaVantSearch(q)
        return render_template('choices.html', M=matches)
    else:
        return redirect('/')

    
if __name__ == "__main__":
    app.debug = True
    app.run()
