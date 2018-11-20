import json, urllib

from flask import Flask, render_template, request, redirect, flash
app = Flask(__name__)  # create instance of class Flask
app.secret_key = "asdfadsfjskdfjqweruioqwerjlkasdjfl;asdjfadlksfkjlfdsjkldfsjkl"

URL_STUB = "http://api.openweathermap.org/data/2.5/weather?q=10007,us&units=imperial"
URL_QUERY = "url="
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

@app.route("/")
def root():
    response = urllib.request.urlopen(URL_STUB + API_KEY)
    o = json.loads(response.read())

    print(list(o.keys()))
    print(o)

    if 'count' in o:
        print(o['list'][0]['weather'])

        o = o['list'][0]
        return render_template("base.html",
                               title = o['name'],
                               weather_main = o['weather'],
                               temp_now = o['main']['temp'],
                               temp_min = o['main']['temp_min'],
                               temp_max = o['main']['temp_max'],
                               icons = icons
        )
    else: 
        print(o['weather'])
                    
        return render_template("base.html",
                               title = o['name'],
                               weather_main = o['weather'],
                               temp_now = o['main']['temp'],
                               temp_min = o['main']['temp_min'],
                               temp_max = o['main']['temp_max'],
                               icons = icons
        )
    
if __name__ == "__main__":
    app.debug = True
    app.run()