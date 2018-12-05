import json, urllib

from flask import Flask, session, render_template, request, redirect, flash, url_for
from os import urandom

from util import apiOperator, api_to_db

app = Flask(__name__)  # create instance of class Flask
app.secret_key = urandom(32)

IPAPI = "https://ipapi.co/json/"

OPEN_WEATHER_URL_STUB = "http://api.openweathermap.org/data/2.5/weather?q="
OPEN_WEATHER_ADD = "&units=imperial"
OPEN_WEATHER_API_KEY = "&appid="+apiOperator.getApiKey('OPEN_WEATHER_KEY')
#87bdad31331cad64c1efc0c13526c6f8
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

GUARDIAN_KEY = apiOperator.getApiKey('Guardian_Key')
#"697684d3-9e9e-45e8-b3a4-b28ed5a741d9"
GUARDIAN_STUB = "https://content.guardianapis.com/search?api-key="
GUARDIAN_URL =  GUARDIAN_STUB + GUARDIAN_KEY

try: api_to_db.createTable()
except: pass
api_to_db.createStockRow()



@app.route("/", methods=['GET','POST'])
def root():

    # checks if city is in session -- sets default to city ip address is at if there is no current city
    if not('CITY' in session):
        IPAPI_response = urllib.request.urlopen(IPAPI).read()
        IPAPI_dictionary = json.loads(IPAPI_response)
        IP_CITY = IPAPI_dictionary["city"]
        session['CITY'] = IP_CITY



    # update city
    if (request.form.get('new_location') != None):
        try: # if the city is an actual city
            urllib.request.urlopen(OPEN_WEATHER_URL_STUB + request.form.get('new_location')  + OPEN_WEATHER_ADD + OPEN_WEATHER_API_KEY)
            try: # if it's a zipcode (float, 5 digits), defaults to the US
                float(request.form.get('new_location'))
                if(len(request.form.get('new_location')) == 5):
                    session["CITY"] = request.form.get('new_location') + "," + "US"
                else:
                    pass
            except ValueError:
                session["CITY"] = request.form.get('new_location').title()
        except:
            flash("Error: Invalid Location", category="location")
            pass


    try:
        open_weather_response = urllib.request.urlopen(OPEN_WEATHER_URL_STUB + urllib.parse.quote(session["CITY"]) + OPEN_WEATHER_ADD + OPEN_WEATHER_API_KEY)
        open_weather = json.loads(open_weather_response.read())
    except:
        flash('PLEASE INSERT YOUR OPEN WEATHER KEY!')
        open_weather={'main':{'temp':'-998',
                              'temp_min':"-999",
                              'temp_max':"0"},
                      'weather':[{'icon':'50n', 'main':'API KEY!'}],
                      'name':'No Api Key!'
                      }

    # checks if there's multiple weather types
    if 'count' in open_weather:
        open_weather = open_weather['list'][0]

    # checks if symbol is in keys
    if (request.method != 'GET'):
        if 'symbl' in request.form.keys():
            l=request.form['symbl']
            print(l)
            if not l:
                return redirect('/')
            api_to_db.modifyStock(l,1)
        return redirect("/")


    try:
        req = urllib.request.urlopen(GUARDIAN_URL)
        data = json.loads(req.read())
        l = data['response']['results']
        s = set()
        for i in l:
            s.add(i['sectionName'])

        if not 'category' in session:
            # get random from set (ensure that default category exists)
            # categories are not constant.
            category = list(s)[0]

        else:
            category = session['category']
    except:
        flash("PLEASE ADD YOUR Guardian API key!")
        category='No api key!'
        data={'response':{'result':{'sectionName':'No api key!',
                                    'webURL':'/',
                                    'webTitle':'NO API KEY!'
        }}}



    return render_template("index.html",
                           location = open_weather['name'],
                           weather_main = open_weather['weather'],
                           temp_now = open_weather['main']['temp'],
                           temp_min = open_weather['main']['temp_min'],
                           temp_max = open_weather['main']['temp_max'],
                           icons = icons,
                           news = data,
                           category = category,
                           entry = apiOperator.stockRetrieve(api_to_db.retrieveStock()))



@app.route("/choices", methods=["GET"])
def choic():

    q = request.args.get('creditcard')
    dbstocks = api_to_db.retrieveStock().split(',')
    if q:
        matches=apiOperator.alphaVantSearch(q)
        print (matches)


        if matches and matches[0][0].find('Note')==0:
            flash(matches[0][0])
            api_to_db.modifyStock(matches[1],1)

            return render_template('choices.html', dbstocks=dbstocks)

        return render_template('choices.html', M=matches, dbstocks=dbstocks)
    else:
        """ONLY DELETING"""
        return render_template('choices.html', dbstocks=dbstocks)
        #return redirect('/')



@app.route("/rmChoices", methods=["GET"])
def rmChoic():

    q=request.args.get('rm')
    if q:
        api_to_db.modifyStock(q,-1)
        return redirect('/')
    else:
        return redirect('/')


# upon clicking on link that leads to news choices, this form is displayed
# based on current selections of news categories
@app.route("/news_choice", methods = ["GET"])
def change_category():
    req = urllib.request.urlopen(GUARDIAN_URL)
    news_data = json.loads(req.read())
    l = news_data['response']['results']
    s = set()

    for i in l:
        s.add(i['sectionName'])

    for checkbox in 'category':
    value = request.form.get(checkbox):
    if value:
#need to add list for selected news 

    return render_template("news_form.html", data = news_data, section = s)

# get selection
# update session['category']
@app.route("/category", methods = ["POST"])
def get_category():
    req = urllib.request.urlopen(GUARDIAN_URL)
    news_data = json.loads(req.read())
    if request.method == "POST":
        category = request.form.get("category")
        session['category'] = category
        return redirect('/')


if __name__ == "__main__":
    app.debug = True
    app.run()
