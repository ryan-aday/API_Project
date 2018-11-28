import json, urllib

from flask import Flask, session, render_template, request, redirect, flash
app = Flask(__name__)  # create instance of class Flask
app.secret_key = "asdfadsfjskdfjqweruioqwerjlkasdjfl;asdjfadlksfkjlfdsjkldfsjkl"

import util.db

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


@app.route("/", methods=['POST'])
def root():

    IPAPI_response = urllib.request.urlopen(IPAPI).read()
    IPAPI_dictionary = json.loads(IPAPI_response)
    IP_CITY = IPAPI_dictionary["city"]

    #session.clear()
    
    if not('CITY' in session):
        session['CITY'] = IP_CITY

    if (request.form.get('new_location') != None):
        try: 
            urllib.request.urlopen(URL_STUB + request.form.get('new_location')  + ADD + API_KEY)
            print(session["CITY"] + " -> " + request.form.get('new_location'))
            try:
                float(request.form.get('new_location') )
                session["CITY"] = request.form.get('new_location') + "," + d["country"]
                print(session["CITY"])
            except ValueError:
                session["CITY"] = request.form.get('new_location').title()
        except:
            pass
    
    print(session["CITY"])
    print(URL_STUB + urllib.parse.quote(session["CITY"]) + ADD + API_KEY)
    
    open_weather_response = urllib.request.urlopen(URL_STUB + urllib.parse.quote(session["CITY"]) + ADD + API_KEY)

    open_weather = json.loads(open_weather_response.read())

    print(list(open_weather.keys()))
    print(open_weather)
    
    if 'count' in open_weather:
        open_weather = open_weather['list'][0]

    return render_template("base.html",
                           location = open_weather['name'],
                           weather_main = open_weather['weather'],
                           temp_now = open_weather['main']['temp'],
                           temp_min = open_weather['main']['temp_min'],
                           temp_max = open_weather['main']['temp_max'],
                           icons = icons
    )
    
    
if __name__ == "__main__":
    util.db.create_table()
    app.debug = True
    app.run()
