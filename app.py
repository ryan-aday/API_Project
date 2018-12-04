import json, urllib

from flask import Flask, session, render_template, request, redirect, flash, url_for

from util import apiOperator, api_to_db

app = Flask(__name__)  # create instance of class Flask
app.secret_key = "asdfadsfjskdfjqweruioqwerjlkasdjfl;asdjfadlksfkjlfdsjkldfsjkl"




IPAPI = "https://ipapi.co/json/"

OPEN_WEATHER_URL_STUB = "http://api.openweathermap.org/data/2.5/weather?q="
OPEN_WEATHER_ADD = "&units=imperial"
OPEN_WEATHER_API_KEY = "&appid=87bdad31331cad64c1efc0c13526c6f8"
OPEN_WEATHER_TEST_MULT = "https://samples.openweathermap.org/data/2.5/find?q=London&appid=b1b15e88fa797225412429c1c50c122a1r&units=imperial"

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

try: api_to_db.createTable()
except: pass
api_to_db.createStockRow()

@app.route("/", methods=['GET','POST'])
def root():

    if (request.method != 'GET'):
        if 'symbl' in request.form.keys():
            l=request.form['symbl']
            print(l)
            if not l:
                return redirect('/')
            api_to_db.modifyStock(l,1)
        return redirect("/")

    
    IPAPI_response = urllib.request.urlopen(IPAPI).read()
    IPAPI_dictionary = json.loads(IPAPI_response)
    IP_CITY = IPAPI_dictionary["city"]

    #session.clear()
    
    if not('CITY' in session):
        session['CITY'] = IP_CITY

    if (request.args.get('new_location') != None):
        try: 
            urllib.request.urlopen(OPEN_WEATHER_URL_STUB + request.args.get('new_location')  + OPEN_WEATHER_ADD + OPEN_WEATHER_API_KEY)
            print(session["CITY"] + " -> " + request.args.get('new_location'))
            print(OPEN_WEATHER_URL_STUB + urllib.parse.quote(request.args.get('new_location') + ",US") + OPEN_WEATHER_ADD + OPEN_WEATHER_API_KEY)
            try:
                float(request.args.get('new_location') )
                session["CITY"] = request.args.get('new_location') + "," + "US"
                print(session["CITY"])
            except ValueError:
                session["CITY"] = request.args.get('new_location').title()
        except:
            pass
    
    print(session["CITY"])
    print(OPEN_WEATHER_URL_STUB + urllib.parse.quote(session["CITY"]) + OPEN_WEATHER_ADD + OPEN_WEATHER_API_KEY)
    
    open_weather_response = urllib.request.urlopen(OPEN_WEATHER_URL_STUB + urllib.parse.quote(session["CITY"]) + OPEN_WEATHER_ADD + OPEN_WEATHER_API_KEY)

    open_weather = json.loads(open_weather_response.read())

    print(list(open_weather.keys()))
    print(open_weather)

    print(request.args.get('new_location'))
    print(request.form.get('new_location'))

    
    if 'count' in open_weather:
        open_weather = open_weather['list'][0]

    return render_template("index.html",
                           location = open_weather['name'],
                           weather_main = open_weather['weather'],
                           temp_now = open_weather['main']['temp'],
                           temp_min = open_weather['main']['temp_min'],
                           temp_max = open_weather['main']['temp_max'],
                           icons = icons,
                           entry = apiOperator.stockRetrieve(api_to_db.retrieveStock())
    )
    
@app.route("/choices", methods=["GET"])
def choic():

    q = request.args.get('creditcard')
    if q:
        matches=apiOperator.alphaVantSearch(q)
        print (matches)
        if matches and matches[0][0].find('Note')==0:
            flash(matches[0][0])
            api_to_db.modifyStock(matches[1],1)
            
            return redirect ('/')#edit
        dbstocks = api_to_db.retrieveStock().split(',')
        return render_template('choices.html', M=matches, dbstocks=dbstocks)
    else:
        return redirect('/')
    
@app.route("/rmChoices", methods=["GET"])
def rmChoic():

    q=request.args.get('rm')
    if q:
        api_to_db.modifyStock(q,-1)
        return redirect('/')
    else:
        return redirect('/')

if __name__ == "__main__":
    app.debug = True
    app.run()
