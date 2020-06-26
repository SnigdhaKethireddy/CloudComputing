# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 06:30:53 2020

@author: SNIGDHA
"""

import os
import ibm_db
from flask import Flask,redirect,render_template,request
import urllib
import datetime
import json


app = Flask(__name__)


if 'VCAP_SERVICES' in os.environ:
    db2info = json.loads(os.environ['VCAP_SERVICES'])['dashDB For Transactions'][0]
    db2cred = db2info["credentials"]
    appenv = json.loads(os.environ['VCAP_APPLICATION'])
else:
    raise ValueError('Expected cloud environment')


def info(name=None):
    # connect to DB2
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        # we have a Db2 connection, query the database
        sql='select * from PEOPLE where "NAME" = ?'
        # Note that for security reasons we are preparing the statement first,
        # then bind the form input as value to the statement to replace the
        # parameter marker.
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.bind_param(stmt, 1, name)
        ibm_db.execute(stmt)
        
        rows={}
        # fetch the result
        result = ibm_db.fetch_assoc(stmt)
        if result != False:
            rows=result.copy()
            result = ibm_db.fetch_assoc(stmt)
        # close database connection
        print(rows)
        ibm_db.close(db2conn)
    return render_template('person.html', inf=rows)
	
	
# handle database request and query info information
def salarysearch():
    # connect to DB2
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        # we have a Db2 connection, query the database
        sql='select * from PEOPLE where SALARY<99000'
        # Note that for security reasons we are preparing the statement first,
        # then bind the form input as value to the statement to replace the
        # parameter marker.
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.execute(stmt)
        rows=[]
        # fetch the result
        result = ibm_db.fetch_assoc(stmt)
        while result != False:
            rows.append(result.copy())
            result = ibm_db.fetch_assoc(stmt)
        # close database connection
        ibm_db.close(db2conn)
    return render_template('salary.html', inf=rows)	


def addpicture(nameToUpdatePic=None, pic=None):
    # connect to DB2
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        # we have a Db2 connection, query the database
        sql='update PEOPLE set PICTURE=? where "NAME"=?'
        # Note that for security reasons we are preparing the statement first,
        # then bind the form input as value to the statement to replace the
        # parameter marker.
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.bind_param(stmt, 1, pic)
        ibm_db.bind_param(stmt, 2, nameToUpdatePic)
        ibm_db.execute(stmt)
        rows=[]
        # close database connection
        ibm_db.close(db2conn)
    return render_template('updateperson.html', inf=rows)	


	
def removePerson(name=None):
    # connect to DB2
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        # we have a Db2 connection, query the database
        sql='delete from PEOPLE where "NAME"=?'
        # Note that for security reasons we are preparing the statement first,
        # then bind the form input as value to the statement to replace the
        # parameter marker.
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.bind_param(stmt, 1, name)
        ibm_db.execute(stmt)
        rows=[]
        # close database connection
        ibm_db.close(db2conn)
    return render_template('removedperson.html')

# handle database request and query info information
def updatekeyword(nameToUpdateKw=None, keyword=None):
    # connect to DB2
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        # we have a Db2 connection, query the database
        sql='update PEOPLE set KEYWORDS=? where "NAME"=?'
        # Note that for security reasons we are preparing the statement first,
        # then bind the form input as value to the statement to replace the
        # parameter marker.
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.bind_param(stmt, 1, keyword)
        ibm_db.bind_param(stmt, 2, nameToUpdateKw)
        ibm_db.execute(stmt)
        rows=[]
        
        # close database connection
        ibm_db.close(db2conn)
    return render_template('updateperson.html')	
	
def updatesal(nameToUpdateSalary=None, salary=None):
    # connect to DB2
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        # we have a Db2 connection, query the database
        sql='update PEOPLE set "SALARY"=? where "NAME"=?'
        # Note that for security reasons we are preparing the statement first,
        # then bind the form input as value to the statement to replace the
        # parameter marker.
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.bind_param(stmt, 1, salary)
        ibm_db.bind_param(stmt, 2, nameToUpdateSalary)
        ibm_db.execute(stmt)
        rows=[]
        # close database connection
        ibm_db.close(db2conn)
    return render_template('updateperson.html')		


# ROUTES!
    
@app.route('/')
def index():
   return render_template('index.html', app=appenv)

# for testing purposes - use name in URI
# =============================================================================
# @app.route('/hello/<name>')
# def hello(name=None):
#     return render_template('hello.html', name=name)
# =============================================================================

'''@app.route('/search', methods=['GET'])
def searchroute():
    name = request.args.get('name', '')
    return info(name)'''
    
@app.route('/search', methods=['GET'])
def searchroute():
    name = request.args.get('name', '')
    return info(name)

@app.route('/searchsalarylessthan99000', methods=['POST'])
def searchsalary():
   return salarysearch()

@app.route('/addimage', methods=['GET'])
def updateimg():
    nameToUpdatePic = request.args.get('nameToUpdatePic', '')
    pic = request.args.get('newpic', '') 
    if request.method == 'POST':  
        f = request.files['newpic']  
        f.save(f.filename)  
    return addpicture(nameToUpdatePic,pic)
    
@app.route('/remove', methods=['GET'])
def remove():
    name = request.args.get('nameToRemove', '')
    return removePerson(name)	
	
@app.route('/updatekw', methods=['GET'])
def updatekey():
    nameToUpdateKw = request.args.get('nameToUpdateKw', '')
    keyword = request.args.get('newkeyword', '')
    return updatekeyword(nameToUpdateKw, keyword)	

@app.route('/updatesalary', methods=['GET'])
def updatesala():
    nameToUpdateSalary = request.args.get('nameToUpdateSalary', '')
    salary = request.args.get('newSalary', '')
    return updatesal(nameToUpdateSalary, salary)		
	
@app.route('/info/<name>')
def inforoute(name=None):
    return info(name)
# =============================================================================
# @app.route('/info/<name>')
# def inforoute(name=None):
#     return info(name)
# =============================================================================

@app.errorhandler(404)
@app.route("/error404")
def page_not_found(error):
 	return render_template('404.html',title='404')
@app.errorhandler(500)
@app.route("/error500")
def requests_error(error):
 return render_template('500.html',title='500')

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))







# =============================================================================
# @app.route('/',methods=['GET','POST'])
# def index():
# 	form = NameForm()
# 	if form.validate_on_submit():
# 		name = form.name.data
# 		return render_template('index.html',form=form,name=name)
# 	return render_template('index.html',form=form,name=None)
# 
# @app.route('/help')
# def help():
# 	text_list = []
# 	# Python Version
# 	text_list.append({
# 		'label':'Python Version',
# 		'value':str(sys.version)})
# 	# os.path.abspath(os.path.dirname(__file__))
# 	text_list.append({
# 		'label':'os.path.abspath(os.path.dirname(__file__))',
# 		'value':str(os.path.abspath(os.path.dirname(__file__)))
# 		})
# 	# OS Current Working Directory
# 	text_list.append({
# 		'label':'OS CWD',
# 		'value':str(os.getcwd())})
# 	# OS CWD Contents
# 	label = 'OS CWD Contents'
# 	value = ''
# 	text_list.append({
# 		'label':label,
# 		'value':value})
# 	return render_template('help.html',text_list=text_list,title='help')
# 
# @app.errorhandler(404)
# @app.route("/error404")
# def page_not_found(error):
# 	return render_template('404.html',title='404')
# 
# @app.errorhandler(500)
# @app.route("/error500")
# def requests_error(error):
# 	return render_template('500.html',title='500')
# 
# port = int(os.getenv('PORT', '3000'))
# app.run(host='0.0.0.0', port=port)
# 
# =============================================================================
