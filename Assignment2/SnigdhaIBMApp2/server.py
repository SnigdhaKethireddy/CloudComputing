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


db2cred = {
  "db": "BLUDB",
  "dsn": "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=bjv36723;PWD=62v3fx+9lwnwb39c;",
  "host": "dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net",
  "hostname": "dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net",
  "https_url": "https://dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net",
  "jdbcurl": "jdbc:db2://dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net:50000/BLUDB",
  "parameters": {},
  "password": "62v3fx+9lwnwb39c",
  "port": 50000,
  "ssldsn": "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net;PORT=50001;PROTOCOL=TCPIP;UID=bjv36723;PWD=62v3fx+9lwnwb39c;Security=SSL;",
  "ssljdbcurl": "jdbc:db2://dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net:50001/BLUDB:sslConnection=true;",
  "uri": "db2://bjv36723:62v3fx%2B9lwnwb39c@dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net:50000/BLUDB",
  "username": "bjv36723"
}
appenv =  {
  "application_id": "b67b12fd-3c3f-4496-b757-b9ec66b15c2e",
  "application_name": "SnigdhaIBMApp1",
  "application_uris": [
   "SnigdhaIBMApp1.us-south.cf.appdomain.cloud",
   "snigdhaibmapp1.mybluemix.net"
  ],
  "application_version": "e6cd7529-fbdb-4c94-89ca-67233c2e5230",
  "cf_api": "https://api.us-south.cf.cloud.ibm.com",
  "limits": {
   "disk": 1024,
   "fds": 16384,
   "mem": 64
  },
  "name": "SnigdhaIBMApp1",
  "organization_id": "1071ffc6-aedd-499c-ad28-76be36243eb8",
  "organization_name": "snigdhasniggi96@gmail.com",
  "process_id": "b67b12fd-3c3f-4496-b757-b9ec66b15c2e",
  "process_type": "web",
  "space_id": "84a2ac71-1136-4434-805b-c04a76e3cfc2",
  "space_name": "dev",
  "uris": [
   "SnigdhaIBMApp1.us-south.cf.appdomain.cloud",
   "snigdhaibmapp1.mybluemix.net"
  ],
  "users": "",
  "version": "e6cd7529-fbdb-4c94-89ca-67233c2e5230"
 }




	
	
# handle database request and query info information
def largest():
    # connect to DB2
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        # we have a Db2 connection, query the database
        sql='select "mag","time","place" from EARTHQUAKE where "mag" IS NOT NULL order by "mag" desc LIMIT 5'
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
    return render_template('large.html', r=rows)	

def rad1():
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        # we have a Db2 connection, query the database'
        sql='SELECT "mag", "time", "place" FROM EARTHQUAKE WHERE acos(sin(0.0175*32.7357) * sin(0.0175*"latitude") + cos(0.0175*32.7357) * cos(0.0175*"latitude") * cos(0.0175*"longitude" - (0.0175* -97.1081)) )* 6371 < 500'
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
    return render_template('rad1.html',r=rows)    


def magni(datefrom=None, dateto=None):
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        # we have a Db2 connection, query the database
        sql='select count(*) from EARTHQUAKE where "mag">3 and ("time" between ? and ?)'
        # Note that for security reasons we are preparing the statement first,
        # then bind the form input as value to the statement to replace the
        # parameter marker.
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.bind_param(stmt, 1, datefrom)
        ibm_db.bind_param(stmt, 2, dateto)
        ibm_db.execute(stmt)
        rows=[]
        # fetch the result
        result = ibm_db.fetch_assoc(stmt)
        while result != False:
            rows.append(result.copy())
            result = ibm_db.fetch_assoc(stmt)
        # close database connection
        ibm_db.close(db2conn)
    return render_template('magnitu.html', r=rows)	

def ritch(magfrom=None, magto=None, datefromritch=None, datetoritch=None):
    # connect to DB2
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        # we have a Db2 connection, query the database
       
        sql='select count(*) from EARTHQUAKE where ("mag" BETWEEN ? AND ?) AND ("time" between ? AND ?)'
        #Note that for security reasons we are preparing the statement first,
        # then bind the form input as value to the statement to replace the
        # parameter marker.
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.bind_param(stmt, 1, magfrom)
        ibm_db.bind_param(stmt, 2, magto)
        ibm_db.bind_param(stmt, 3, datefromritch)
        ibm_db.bind_param(stmt, 4, datetoritch)
        ibm_db.execute(stmt)
        rows=[]
        # fetch the result
        result = ibm_db.fetch_assoc(stmt)
        while result != False:
            rows.append(result.copy())
            result = ibm_db.fetch_assoc(stmt)
        # close database connection
        ibm_db.close(db2conn) 
    return render_template('ritcher.html', r=rows)



def new():
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        # we have a Db2 connection, query the database
        sql='SELECT count(*) FROM EARTHQUAKE WHERE acos(sin(0.0175*32.7767) * sin(0.0175*"latitude") + cos(0.0175*32.7767) * cos(0.0175*"latitude") * cos(0.0175*"longitude" - (0.0175* -97.1081))) * 6371 < 1000'
        stmt = ibm_db.prepare(db2conn,sql)
        ibm_db.execute(stmt)
        rows=[]
        result = ibm_db.fetch_assoc(stmt)
        while result != False:
            rows.append(result.copy())
            result = ibm_db.fetch_assoc(stmt)
        sql1='SELECT count(*) FROM EARTHQUAKE WHERE acos(sin(0.0175*61) * sin(0.0175*"latitude") + cos(0.0175*61) * cos(0.0175*"latitude") * cos(0.0175*"longitude" - (0.0175* -150))) * 6371 < 1000'
        stmt = ibm_db.prepare(db2conn,sql1)
        ibm_db.execute(stmt)
        rows1=[]
        # fetch the result
        result = ibm_db.fetch_assoc(stmt)
        while result != False:
            rows1.append(result.copy())
            result = ibm_db.fetch_assoc(stmt)
        # close database connection
        ibm_db.close(db2conn)
    return render_template('bet.html',r=rows, f=rows1)

@app.route('/newsearch', methods=['GET'])
def newarea():
    return new()

def rad2():
    db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")
    if db2conn:
        # we have a Db2 connection, query the database'
        sql='SELECT "place", "mag" FROM EARTHQUAKE WHERE acos(sin(0.0175*32.7767) * sin(0.0175*"latitude") + cos(0.0175*32.7767) * cos(0.0175*"latitude") * cos(0.0175*"longitude" - (0.0175* -97.1081))) * 6371 < 200 order by "mag" desc LIMIT 1'
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
    return render_template('rad2.html',r=rows)
    
    

    



    


    
@app.route('/')
def index():
   return render_template('index.html', app=appenv)

@app.route('/largest5', methods=['POST'])
def large():
    return largest()

@app.route('/radi1', methods=['POST'])
def radi():
    return rad1()

@app.route('/magnitude', methods=['GET'])
def mag():
    datefrom = request.args.get('datefrom', '')
    dateto = request.args.get('dateto', '')
    return magni(datefrom, dateto)  
        
@app.route('/ritcher', methods=['GET'])
def rit():
    magfrom = request.args.get('magfrom', '')
    magto = request.args.get('magto', '')
    datefromritch = request.args.get('datefromritch', '')
    datetoritch = request.args.get('datetoritch', '')
    return ritch(magfrom , magto, datefromritch, datetoritch)	



@app.route('/radi2', methods=['POST'])
def radii():
    return rad2()


    




    



 

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
	app.run(host='127.0.0.1', port=int(port))







