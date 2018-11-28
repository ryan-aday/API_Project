
from flask import Flask, render_template

from flask import request, session #login function
from flask import url_for, redirect, flash #redirect functions

from util import apiOperator, dbOperator

import os, random

app = Flask(__name__)

app.secret_key = os.urandom(32)


@app.route("/", methods=["GET","POST"])
def root():
    #session['stocks']=['goog','aapl']

    if (request.method == 'GET'):

        return render_template('bootstrap.html', entry=apiOperator.stockRetrieve(dbOperator.retrieveStock()))
    else:
        
        l=request.form['symbl']
        if not l:
            return redirect('/')
        dbOperator.modifyStock(l,1)
        return redirect("/")

        
@app.route("/choices", methods=["GET"])
def choic():

    q = request.args.get('query')
    if q:
        d= dbOperator.retrieveStock().split(',')
        
        matches=apiOperator.alphaVantSearch(q)
        return render_template('choices.html', M=matches, dbstocks=d)
    else:
        return redirect('/')
    
    
    return "quarum unam incolunt Belgae, aliam Aquitani, tertiam qui ipsorum lingua Celtae, nostra Galli appelantur. Hi omnes lingua, institutis, legibus inter se differunt. Gallos ab Aquitanis Garumna flumen, a Belgis Matrona et Sequana dividit."

@app.route("/rmChoices", methods=["GET"])
def rmChoic():

    q=request.args.get('rm')
    if q:
        dbOperator.modifyStock(q,-1)
        return redirect('/')
    else:
        return redirect('/')


if __name__=="__main__":
    app.debug=True
    app.run()
    
    
