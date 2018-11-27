import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O



def create():
    """create database file and insert stuff, for developing purposes"""
    DB_FILE="./data/apis.db"      
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()               
    cmd = "CREATE TABLE api(name TEXT, lastUpdate TEXT, lastJson TEXT, otherInfo TEXT)"
    c.execute(cmd)
    cmd = "insert into api values('IEX', '','', 'GOOG,aapl')"
    
    c.execute(cmd)    #run SQL statement
    db.commit() #save changes
    db.close()  #close database
    return

#create()
def retrieveStock():
    """retrieves comma separated string of all stock that will be displayed"""
    DB_FILE="./data/apis.db"      
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()
    cmd ="SELECT otherInfo FROM api WHERE name='IEX'"
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
    
    DB_FILE="./data/apis.db"      
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()
    stock_list=retrieveStock().split(',')
    if stock in stock_list:
        if action <0:
            stock_list.pop(stock_list.index(stock))
            stocks = join(stock_list)
            cmd = "UPDATE api SET otherInfo='{}' WHERE name='IEX'".format(stocks)
            c.execute(cmd)
    else:
        stock=stock.upper()
        stock_list.append(stock)
        stocks = join(stock_list)
        cmd = "UPDATE api SET otherInfo='{}' WHERE name='IEX'".format(stocks)
        print(cmd)
        c.execute(cmd)
    """if action > 0:
        symb = [(symbol)]
        cmd = "INSERT INTO [{}] VALUES(?)".format(user)
        c.executemany(cmd, symb)
    else:
        cmd = "DELETE FROM [{}] WHERE symbol = '{}'".format(user, symbol)
        c.execute(cmd)
    """
    db.commit() #save changes
    db.close()  #close database
    return
#modifyStock('blah',-1)
