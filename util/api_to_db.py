import sqlite3

DB_FILE = "database.db"

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
    c.execute("delete from apis")
    db.commit()
    db.close()
