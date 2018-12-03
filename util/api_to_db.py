import sqlite3
import time
import datetime

def timestamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return st


DB_FILE = "./data/database.db"

# function to create a table for apis
def createTable():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("CREATE TABLE apis (api TEXT, timestamp TEXT, data TEXT, key TEXT)")
    db.commit()
    db.close()

# insert an API's info into the data table 'apis'
def insertAPI(api, timestamp, data, key):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    params = (api, timestamp, data, key)
    c.execute("INSERT INTO apis VALUES(?, ?, ?, ?)", params)
    db.commit()
    db.close()
    return True

# clear table function
def clearTable():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("delete from apis where api!='IEX'")
    #do not clear api name for IEX, since I think users should be able to keep selections from last time
    db.commit()
    db.close()

""" ----------------stock functions----------------------"""
def createStockRow():
    """creates stock row at very start"""
    db = sqlite3.connect(DB_FILE)
    c=db.cursor()
    cmd = 'SELECT api FROM apis WHERE api="IEX"'
    entry = c.execute(cmd).fetchall()
    print(entry)
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    db.close()
    if not entry:
        insertAPI('IEX',timestamp(),'','')
    return

def retrieveStock():
    """retrieves comma separated string of all stock that will be displayed"""

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    cmd ="SELECT data FROM apis WHERE api='IEX'"
    stocks= c.execute(cmd).fetchall()
    print(stocks)
    stock_list=''
    if stocks:
        stock_list=stocks[0][0]
    return stock_list

def join(list):
    """joins a list item into a comma separated string"""
    s=""
    for elem in list:
        s+=elem+","
    return s[:-1]

def modifyStock(stock, action):

    """modifies entry symbol in user's table, action =1 add, =-1 delete"""
    """ stock is a string that is already verifiied"""


    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    stock_list=retrieveStock().split(',')
    cmd=""
    if stock in stock_list:
        if action <0:
            stock_list.pop(stock_list.index(stock))
            stocks = join(stock_list)
            cmd = "UPDATE apis SET data='{}',timestamp='{}' WHERE api='IEX'".format(stocks, timestamp())

    else:
        stock=stock.upper()
        print(stock+"---------------------")
        stock_list.append(stock)
        if stock_list[0]=='':
            stock_list.pop(0)
        stocks = join(stock_list)
        print(stocks)
        cmd = "UPDATE apis SET data='{}',timestamp='{}' WHERE api='IEX'".format(stocks, timestamp())
        

    c.execute(cmd)
    db.commit() #save changes
    db.close()  #close database
    return
