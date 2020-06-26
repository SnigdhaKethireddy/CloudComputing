import os
from flask import Flask,redirect,render_template,request
import pypyodbc
import time
import random
import urllib
import datetime
import json
import redis
import pickle
import hashlib

app = Flask(__name__)


dbconn = pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:snigdhasqlserver.database.windows.net,1433;Database=adbdb;Uid=snigdha;Pwd=5190$Niggi;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')

r = redis.Redis(host='snigdhakethireddy1.redis.cache.windows.net',
        port=6379, db=0, password='NkVtcezXTWsKSsWK8Re1YCt4ld9D6KdTuVn8bcoGq94=')
def selca(num2=None):
    dbconn = pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:snigdhasqlserver.database.windows.net,1433;Database=adbdb;Uid=snigdha;Pwd=5190$Niggi;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
    cursor = dbconn.cursor()
    start = time.time()
    for i in range(0,int(num2)):
        success="DELETE TOP(2) PERCENT from all_month COMMIT"
        cursor.execute(success)
    success2="SELECT count(*) from all_month"
    cursor.execute(success2)
    rows = cursor.fetchall()
    end = time.time()
    exectime = end - start
    return render_template('search.html', t=exectime,r=rows)

@app.route('/datemag', methods=['GET'])
def sel1():
    num2 = request.args.get('num2','')
    return selca(num2) 


def selnca(num3=None):
    dbconn =pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:snigdhasqlserver.database.windows.net,1433;Database=adbdb;Uid=snigdha;Pwd=5190$Niggi;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
    #dbconn = pypyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = dbconn.cursor()
    start = time.time()
    for i in range(0,int(num3)):
        success="DELETE TOP(2) PERCENT from all_month COMMIT"
        success2="SELECT count(*) from all_month"
        hash = hashlib.sha224(success.encode('utf-8')).hexdigest()
        key = "redis_cache:" + hash
        if (r.get(key)):
           print("redis cached")
           rows=[]
        else:
           # Do MySQL query   
           cursor.execute(success)
           cursor.execute(success2)
           data = cursor.fetchall()
           rows = []
           for j in data:
                rows.append(str(j))  
           # Put data into cache for 1 hour
           r.set(key, pickle.dumps(list(rows)) )
           r.expire(key, 36)
        cursor.execute(success)
        cursor.execute(success2)
    end = time.time()
    exectime = end - start
    return render_template('search.html', t=exectime,r=rows)

@app.route('/dmagca', methods=['GET'])
def sel2():
    num3 = request.args.get('num3','')
    return selnca(num3) 
 
   
def rangeca(rangefrom=None,rangeto=None,datefrom=None,dateto=None,num=None):
    dbconn =pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:snigdhasqlserver.database.windows.net,1433;Database=adbdb;Uid=snigdha;Pwd=5190$Niggi;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
    #dbconn = pypyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = dbconn.cursor()
    start = time.time()
    for i in range(0,int(num)):
        mag= round(random.uniform(rangefrom, rangeto),1)
        success="SELECT * from all_month where mag>'"+str(mag)+"'and (time between '"+str(datefrom)+"' and '"+str(dateto)+"')"
        hash = hashlib.sha224(success.encode('utf-8')).hexdigest()
        key = "redis_cache:" + hash
        if (r.get(key)):
           print("redis cached")
        else:
           # Do MySQL query   
           cursor.execute(success)
           data = cursor.fetchall()
           rows = []
           for j in data:
                rows.append(str(j))  
           # Put data into cache for 1 hour
           r.set(key, pickle.dumps(list(rows)) )
           r.expire(key, 36)
        cursor.execute(success)
    end = time.time()
    exectime = end - start
    return render_template('search.html', t=exectime)

@app.route('/magnituca', methods=['GET'])
def sel3():
    rangefrom = float(request.args.get('rangefrom',''))
    rangeto = float(request.args.get('rangeto',''))
    datefrom = request.args.get('datefrom','')
    dateto = request.args.get('dateto','')
    num = request.args.get('num','')
    return rangeca(rangefrom,rangeto,datefrom,dateto,num) 
	
def rangenc(rangefrom1=None,rangeto1=None,datefrom1=None,dateto1=None,num1=None):
    dbconn = pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:snigdhasqlserver.database.windows.net,1433;Database=adbdb;Uid=snigdha;Pwd=5190$Niggi;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
    cursor = dbconn.cursor()
    start = time.time()
    for i in range(0,int(num1)):
        mag= round(random.uniform(rangefrom1, rangeto1),1)
        success="SELECT * from all_month where mag>'"+str(mag)+"' and (time between '"+str(datefrom1)+"' and '"+str(dateto1)+"')"
        cursor.execute(success)
        rows = cursor.fetchall()
    end = time.time()
    exectime = end - start
    return render_template('search.html', t=exectime,ci=rows)

@app.route('/magnitu', methods=['GET'])
def sel4():
    rangefrom1 = float(request.args.get('rangefrom1',''))
    rangeto1 = float(request.args.get('rangeto1',''))
    datefrom1 = request.args.get('datefrom1','')
    dateto1 = request.args.get('dateto1','')
    num1 = request.args.get('num1','')
    return rangenc(rangefrom1,rangeto1,datefrom1,dateto1,num1) 




@app.route('/')
def index():
  return render_template('index.html')


@app.errorhandler(404)
@app.route("/error404")
def page_not_found(error):
	return render_template('404.html',title='404')

@app.errorhandler(500)
@app.route("/error500")
def requests_error(error):
	return render_template('500.html',title='500')




      
port = os.getenv('PORT', '8000')
if __name__ == "__main__":
	app.run(host='127.0.0.1', port=int(port))
