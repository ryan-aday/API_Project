import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O

#==========================================================

DB_FILE="./data/<intended_name>"      #<SUBSTITUTE FILE NAME>
db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

#==========================================================
#INSERT YOUR POPULATE CODE IN THIS ZONE

cmd = "CREATE TABLE table_name(name TEXT, age INTEGER, id INTEGER)"

"""INSERT"""
#cmd = "INSERT INTO [{}] VALUES(?,?)".format(user)

"""SELECT"""
#cmd = "SELECT name FROM sqlite_master WHERE name = '{}'".format(storyName)
"""how to extract table names"""
#cmd = "SELECT * FROM '{}' WHERE authors = '{}'".format(storyname, username)
#      'SELECT name FROM sqlite_master WHERE type = "table" '
#result = c.execute(cmd).fetchall() #listyfy
"""
if result:#list is not empty
        return True
    # Otherwise, the user has not contributed. (Return false).
    return False
"""

#build SQL stmt, save as string
c.execute(cmd)    #run SQL statement

#==========================================================

db.commit() #save changes
db.close()  #close database
