import json
from urllib import request

# get api key from keys directory
def getApiKey(filename):
    f=open('./keys/{}.txt'.format(filename))
    fread=f.read()
    print(filename+"'s key: "+fread)
    f.close()
    return fread

# get json from api
def apiRetrieve(URL_STUB, URL_other):
    '''general api retrieval function'''
    URL=URL_STUB+URL_other
    response = request.urlopen(URL)
    s = response.read()
    d = json.loads(s.decode('utf-8'))
    return d

# get stock info
def stockRetrieve(names):
    '''
    specific IEX retrieval function
    names is comma separated string
    '''
    if not names:
        return []
    URL_STUB = 'https://api.iextrading.com/1.0/stock/market/batch?'
    names=names.upper()
    symb = 'symbols='+names
    '''for name in names:
        symb += name + ","
    sym=symb[:-1]'''
    typ ='types=quote'
    d = apiRetrieve(URL_STUB, symb+'&'+typ) #what we recieve from api

    D = [] #list with more useful information
    """[name, latestPrice, percentChange, priceChange, currPrice, compName] """
    """ 0           1          2                 3       4           5      """
    #print(d)
    names=names.split(',')
    for name in names:
        if name in d.keys():
            D.append([name,d[name]['quote']['latestPrice'],round((d[name]['quote']['latestPrice']-d[name]['quote']['open'])/d[name]['quote']['open'],4),round(d[name]['quote']['latestPrice']-d[name]['quote']['open'],4),d[name]['quote']['latestPrice'], d[name]['quote']['companyName']])
    #print("++++++++++")
    return D

# search through alpha vantage to see if there are stocks that match
def alphaVantSearch(query):

    '''
    searching function from alpha Vantage, 5/min, 500/day
    query must be non-empty
    returns empty list if none matched,
    else return list of [[symbol, name]]
    '''


    fread=getApiKey('AlphaVantageKey')

    URL='https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={}&apikey={}'.format(query,fread)

    try:
        d = apiRetrieve(URL, '')
    except:
        return [['Note:' + "your request produced some errors, your query is directly added to the database regardless of its validity"],query]

    if 'Note' in d.keys():
        #"if there's a note section, then quotas are used up"
        print(d['Note'])
        return [['Note:' + d['Note'] + '-- AlphaVantage  Your choice has automatically been added to your database regardless of its validity'],query]#triple list to match other return
    if 'Error Message' in d.keys():
        return[['Note:' + d['Error Message']+" Your choice is directly added to the database regardless of its validity."], query]

    listOfMatches = []
    for entry in d['bestMatches']:
        if entry['1. symbol'].find('.') <0:
            listOfMatches.append([entry['1. symbol'], entry['2. name']])

    return listOfMatches
