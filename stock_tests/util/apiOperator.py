import json
from urllib import request

def apiRetrieve(URL_STUB, URL_other):
    '''general api retrieval function'''
    URL=URL_STUB+URL_other
    response = request.urlopen(URL)
    s = response.read()
    d = json.loads(s)
    return d

def stockRetrieve(names):
    '''specific IEX retrieval function'''
    URL_STUB = 'https://api.iextrading.com/1.0/stock/market/batch?'
    symb = 'symbols='
    for name in names:
        symb += name + ","
    typ ='types=quote'
    d = apiRetrieve(URL_STUB, symb+'&'+typ) #what we recieve from api
    D = [] #list with more useful information
    #print(d)
    #print(names)
    for name in names:
        D.append([name,d[name]['quote']['latestPrice'],(d[name]['quote']['latestPrice']-d[name]['quote']['open'])/d[name]['quote']['open']])
    return D

def alphaVantSearch(query):
    
    '''
    searching function from alpha Vantage, 5/min, 500/day
    query must be non-empty
    '''
    

    URL='https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={}&apikey=XDFTB6OV8CPHPJ45'.format(query)
    print(URL)
    d = apiRetrieve(URL, '')
    listOfMatches = []
    for entry in d['bestMatches']:
        listOfMatches.append(entry['1. symbol'])
    print(listOfMatches)
    return listOfMatches
