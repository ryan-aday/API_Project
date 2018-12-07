import json, urllib

from flask import Flask, session, render_template, request, redirect, flash, url_for
from os import urandom

from util import apiOperator, api_to_db

app = Flask(__name__)  # create instance of class Flask
app.secret_key = urandom(32)

# api for IP address
IPAPI = "https://ipapi.co/json/"

# open weather api setup
OPEN_WEATHER_URL_STUB = "http://api.openweathermap.org/data/2.5/weather?q="
OPEN_WEATHER_ADD = "&units=imperial"
OPEN_WEATHER_API_KEY = "&appid="+apiOperator.getApiKey('OPEN_WEATHER_KEY_1')
print('TEST: '+ OPEN_WEATHER_API_KEY)
#87bdad31331cad64c1efc0c13526c6f8
OPEN_WEATHER_TEST_MULT = "https://samples.openweathermap.org/data/2.5/find?q=London&appid=b1b15e88fa797225412429c1c50c122a1r&units=imperial"

# icons for weather updates
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

# the guardian api setup
GUARDIAN_KEY = apiOperator.getApiKey('Guardian_Key')
GUARDIAN_STUB = "https://content.guardianapis.com/search?api-key="
GUARDIAN_URL =  GUARDIAN_STUB + GUARDIAN_KEY

# create database for stocks if it doesn't already exist
try: api_to_db.createTable()
except: pass
api_to_db.createStockRow()

# root function for index.html
@app.route("/", methods=['GET','POST'])
def root():

    # checks if city is in session -- sets default to city ip address is at if there is no current city
    if not('CITY' in session):
        IPAPI_response = urllib.request.urlopen(IPAPI).read()
        IPAPI_dictionary = json.loads(IPAPI_response.decode('utf-8'))
        IP_CITY = IPAPI_dictionary["city"]
        session['CITY'] = IP_CITY

    # update city
    if (request.form.get('new_location') != None):
        try: # if the city is an actual city
            urllib.request.urlopen(OPEN_WEATHER_URL_STUB+request.form.get('new_location')+ OPEN_WEATHER_ADD+OPEN_WEATHER_API_KEY)
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
        open_weather_response = urllib.request.urlopen(OPEN_WEATHER_URL_STUB+urllib.parse.quote(session["CITY"])+OPEN_WEATHER_ADD+OPEN_WEATHER_API_KEY)
        open_weather = json.loads(open_weather_response.read())
        # checks if there's multiple weather types
        if 'count' in open_weather:
            open_weather = open_weather['list'][0]

    except:
        flash('PLEASE INSERT YOUR OPEN WEATHER KEY!')
        open_weather={'main':{'temp':'-998',
                              'temp_min':"-999",
                              'temp_max':"0"},
                      'weather':[{'icon':'50n', 'main':'API KEY!'}],
                      'name':'No Api Key!'
                      }


    # checks if symbol is in keys
    if (request.method != 'GET'):
        if 'symbl' in request.form.keys():
            l=request.form['symbl']
            if not l:
                return redirect('/')
            api_to_db.modifyStock(l,1)
        return redirect("/")


    # the guardian api informtion
    try:
        req = urllib.request.urlopen(GUARDIAN_URL)
        data = json.loads(req.read())
        l = data['response']['results'] # the specific part that contains news headlines
        s = set()
        for i in l:
            s.add(i['sectionName'])
        if not 'category' in session: #if session['category'] not already defined
            # get random from set (ensure that default category exists)
            # categories are not constant.
            c = list(s)[0]
            category = [c]
            session['category'] = category
        else:
            # category is session['category'] if already defined
            category = session['category']

    except:
        # make user get their own API key
        flash("PLEASE ADD YOUR Guardian API key!")
        category=['No Guardian api key!']
        data={'response':{'result':{'sectionName':'No api key!',
                                    'webURL':'/',
                                    'webTitle':'NO API KEY!'
        }}}


    # render template
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
    '''
    - allows user to choose stock choices from query in index.html
    - allows user to remove stocks they do not like
    '''

    q = request.args.get('stock')#query for AlphaVantage search

    dbstocks = api_to_db.retrieveStock().split(',')#stocks user has already chosen

    if q:#if query is not empty

        matches=apiOperator.alphaVantSearch(q)
        #search for matches to query from AphaVantage

        if matches and matches[0][0].find('Note')==0:
            '''if there's a 'Note' in matches,  user has used up his quota'''

            flash(matches[0][0])#flashes the error returned by AlphaVantage

            api_to_db.modifyStock(matches[1],1)
            #still adds the query searched (matches[1]) into user's choices, so if user enters valid options, stocks can still be displayed

            return render_template('choices.html', dbstocks=dbstocks)

        #everything's normal, displays matches and stocks that can be deleted
        return render_template('choices.html', M=matches, dbstocks=dbstocks)

    else:
        #if query is empty, only show stocks user already chose and can delete
        return render_template('choices.html', dbstocks=dbstocks)



# to remove stocks from choices
@app.route("/rmChoices", methods=["GET"])
def rmChoic():
    '''
    process the user's request to remove the stock, redirects to index.html no matter what
    '''

    q=request.args.get('rm')#get the stock symbol to be removed

    if q:# if not empty
        api_to_db.modifyStock(q,-1)#remove it
        return redirect('/')
    else:
        return redirect('/')


# upon clicking on link that leads to news choices, this form is displayed
# based on current selections of news categories
@app.route("/news_choice", methods = ["GET"])
def change_category():
    try:
        req = urllib.request.urlopen(GUARDIAN_URL)
        news_data = json.loads(req.read())
        l = news_data['response']['results']
        s = set()
        for i in l:
            s.add(i['sectionName'])
        return render_template("news_form.html", data = news_data, section = s)
    except:
        flash('Please add your Guardian API key!')
        return render_template('news_form.html')

# get selection
# update session['category']
@app.route("/category", methods = ["POST"])
def get_category():


    #req = urllib.request.urlopen(GUARDIAN_URL)
    #news_data = json.loads(req.read())
    '''^^^ is above portion used in this fxn?'''


    if not('category' in session):
        session['category'] = []

    if request.method == "POST":
        category = request.form.get("category")

    print("should be adding", category)
    session['category'].append(category)
    session.modified = True
    print("now is, ",session['category'])
    return redirect('/')

# remove news categories from session['category'] through form
@app.route("/removingnews", methods = ["GET"])
def rm_news():
    q=request.args.get('rmnews')
    print(q)
    if q:
        print(q)
        session['category'].remove(q)
        session.modified = True
        print(session['category'])
        return redirect('/')
    else:
        return redirect('/')

# run app
if __name__ == "__main__":
    app.debug = True
    app.run()
