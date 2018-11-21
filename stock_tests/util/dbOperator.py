import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O



def createUSER(user):
    DB_FILE="./data/stock.db"      
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()               
    cmd = "CREATE TABLE {}(symbol TEXT)".format(user)
    c.execute(cmd)    #run SQL statement
    db.commit() #save changes
    db.close()  #close database
    return

def modify(user, symbol, action):
    """modifies entry symbol in user's table, action =1 add, =-1 delete"""
    DB_FILE="./data/stock.db"      
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()       
    if action > 0:
        symb = [(symbol)]
        cmd = "INSERT INTO [{}] VALUES(?)".format(user)
        c.executemany(cmd, symb)
    else:
        cmd = "DELETE FROM [{}] WHERE symbol = '{}'".format(user, symbol)
        c.execute(cmd)
        
    db.commit() #save changes
    db.close()  #close database
    return

def symbolOf(user):
    DB_FILE="./data/stock.db"      
    db = sqlite3.connect(DB_FILE) 
    c = db.cursor()  
    cmd = "SELECT * FROM '{}'".format(user)
    l = c.execute(cmd).fetchall()
    regularList=[]
    for entry in l:
        regularList.append(entry)
    return regularList
    
