
"""
Qian Zhou
SoftDev1 pd07
K -- 
2018
"""

from flask import Flask, render_template

from flask import request, session #login function
from flask import url_for, redirect, flash #redirect functions

from util import apiOperator

import os, random

app = Flask(__name__)

app.secret_key = os.urandom(32)


@app.route("/", methods=["GET","POST"])
def root():
    #session['stocks']=['goog','aapl']
    if (request.method == 'GET'):
        if not session.keys() or not session['stocks']:
            return render_template('bootstrap.html', entry=[])
        return render_template('bootstrap.html', entry=apiOperator.stockRetrieve(session['stocks']))
    else:
        """HOW DO WE GET VALUES OF CHECKBOX INPUT INTO A LIST?????????????"""
        l=request.form['symbl']
        if not l:
            return redirect('/')
        print('------------')
        print(l)
        print('================')
        li = [l]
        session['stocks']=li
        return redirect("/")

        
@app.route("/choices", methods=["GET"])
def choic():

    q = request.args.get('query')
    if q:
        matches=apiOperator.alphaVantSearch(q)
        return render_template('choices.html', M=matches)
    else:
        return redirect('/')
    
    
    return "quarum unam incolunt Belgae, aliam Aquitani, tertiam qui ipsorum lingua Celtae, nostra Galli appelantur. Hi omnes lingua, institutis, legibus inter se differunt. Gallos ab Aquitanis Garumna flumen, a Belgis Matrona et Sequana dividit."


if __name__=="__main__":
    app.debug=True
    app.run()
