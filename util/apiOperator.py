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
    print ('NAMES:')
    print(names)
    symb = 'symbols='
    for name in names:
        symb += name + ","
    sym=symb[:-1]
    typ ='types=quote'
    d = apiRetrieve(URL_STUB, symb+'&'+typ) #what we recieve from api
    
    D = [] #list with more useful information
    """[name, latestPrice, percentChange, priceChange, currPrice] """
    """ 0           1          2                 3       4        """
    #print(d)
   
    for name in names:
        if name in d.keys():
            D.append([name,d[name]['quote']['latestPrice'],round((d[name]['quote']['latestPrice']-d[name]['quote']['open'])/d[name]['quote']['open'],4),round(d[name]['quote']['latestPrice']-d[name]['quote']['open'],4),d[name]['quote']['latestPrice']])
    #print("++++++++++")
    #print (D)
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
