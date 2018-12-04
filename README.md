# Team RanQuoR_Turkey
##### Ryan Aday, Clara Mohri, Rachel Ng, Qian Zhou

### Overview
Our page displays customizable daily updates. We provide stocks, news, and weather updates.  
The default location for the weather updates using a current location API, but can be set through a form.   
Stock data comes from the IEX API. Stock cards can be added and removed through a form.  
News data comes from The Guardian's API. The default news category is a random one, but it can be customized through a form. 

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
   
5. Run the python file called app.py:
    ```
    $ python app.py
    ``` 
6. You can now view the page in your ```http://localhost:5000```
