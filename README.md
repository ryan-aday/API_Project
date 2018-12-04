# Team RanQuoR_Turkey
##### Ryan Aday, Clara Mohri, Rachel Ng, Qian Zhou

### Overview
Our page displays customizable daily updates. We provide stocks, news, and weather updates.  
The default location for the weather updates using a current location API, but can be set through a form.   
Stock data comes from the IEX API. Stocks can be searched from the AlphaVantage API. They can be added or removed through a form. 
News data comes from The Guardian's API. The default news category is a random one, but it can be customized through a form. 


### Dependencies
We use Flask, wheel, Boostrap and Python.
- **Flask**
  To install in your virtual environment: 
  ```
  $ pip3 install flask
  ```
  For web framework.
- **Wheel installation**
  To install in your virtual environment
  ```
  $ pip3 install wheel
  ```
  For jinja2 dependency for templating.
- **Boostrap**:  
  Already part of the file, CDN is used in templates/index.html
  This is used for nice formatting.
  
  
### How to Run

0. Clone our repo: 
  
    ```
    $ git clone git@github.com:ryan-aday/RanQuoR-Turkey--adayR-mohriC-ngR-zhouQ.git API_Project
    ```
1. Change directories into your newly cloned directory: 
  
    ```
    $ cd API_Project
    ```
3. At this point, you may want to procure your own API keys instead of using ours. Only some of the API's we used require keys.
  -   Weather API: 
      We use OpenWeatherMap's free API. You can procure your key by following the instructions [here](https://openweathermap.org/price)
  -  News API: 
      We use The Guardian's free API. You can procure your key by following the instructions [here](https://open-platform.theguardian.com/access/)

4. Once you've created your keys, you can replace them in our app.py file for your own use.   
  Line 18 contains the key for Open Weather.   
  Line 32 contains the key for The Guardian.  
  Alpha Vantage API key is found in `util/apiOperator.py` line 53
   
5. Activate your virtual environment:
   ```
    $ . path/to/venv/bin/activate
   ```
6. Run the python file called app.py:
    ```
    $ python app.py
    ``` 
7. You can now view the page in your ```http://localhost:5000```
