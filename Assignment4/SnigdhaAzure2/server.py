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
from io import BytesIO
import base64
import hashlib
from copy import deepcopy
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
plt.rcParams['figure.figsize'] 
plt.style.use('ggplot')

app = Flask(__name__)


dbconn = pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:snigdhasqlserver.database.windows.net,1433;Database=adbdb;Uid=snigdha;Pwd=5190$Niggi;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')

r = redis.Redis(host='snigdhakethireddy1.redis.cache.windows.net',
        port=6379, db=0, password='NkVtcezXTWsKSsWK8Re1YCt4ld9D6KdTuVn8bcoGq94=')
   
def ranges(rangefrom1=None,rangeto1=None):
    dbconn =pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:snigdhasqlserver.database.windows.net,1433;Database=adbdb;Uid=snigdha;Pwd=5190$Niggi;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
    #dbconn = pypyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = dbconn.cursor()
    success="SELECT depth,mag from all_month where mag between '"+str(rangefrom1)+"' and '"+str(rangeto1)+"' "
    cursor.execute(success)
    rows = cursor.fetchall()
    depth=[]
    mag=[]
    for row in rows:
            depth.append(row['depth'])
            mag.append(row['mag'])
    X = np.array(list(zip(depth, mag)))
    kmeans = KMeans(n_clusters = int(8))
    kmeans.fit(X)
    centroid = kmeans.cluster_centers_
    labels = kmeans.labels_
    imga=BytesIO()
    all = [[]] * 8
    for i in range(len(X)):

        # print(index)
        # print(X[i], labels[i])

            colors = ["b.", "r.", "g.", "w.", "y.", "c.", "m.", "k."]
            for i in range(len(X)):
               plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize=3)

            plt.scatter(centroid[:, 0], centroid[:, 1], marker="x", s=150, linewidths=5, zorder=10)
            plt.savefig(imga, format='png')
            imga.seek(1)

            plot_url = base64.b64encode(imga.getvalue()).decode()
            
            plt.show()
            plt.clf()
            
            break 
    return render_template('search.html', plot_url=plot_url)

    

@app.route('/displaydata', methods=['GET'])
def display():
    rangefrom1 = float(request.args.get('rangefrom1',''))
    rangeto1 =float(request.args.get('rangeto1',''))
    return ranges(rangefrom1,rangeto1) 


def piechart(rangefrom2=None,rangeto2=None):
    dbconn =pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:snigdhasqlserver.database.windows.net,1433;Database=adbdb;Uid=snigdha;Pwd=5190$Niggi;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
    #dbconn = pypyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = dbconn.cursor()
    ss = float((float(rangeto2)-float(rangefrom2))/5)
    print(ss)
    sizes=[]
    labels=[]
    j = float(rangefrom2)
    k=0
    #img=BytesIO()
    for i in range(0,int(5)):
          k= j+ss
          success="SELECT count(*) from all_month where mag between '"+str(j)+"'and '"+str(k)+"'"
          cursor.execute(success)
          result_set = cursor.fetchall()
          print(result_set)
          for row in result_set:
              sizes.append(row[0])
              labels.append('magrange'+str(round(j,2))+' and '+str(round(k,2)))
          j=k
    print(labels)
    print(sizes)
    colors = ['gold', 'yellow', 'red','blue','black']
    explode = (0.1, 0, 0)
    imgb=BytesIO()
    plt.pie(sizes,labels=labels, colors=colors,autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.savefig(imgb, format='png')
    imgb.seek(1)

    plot_url = base64.b64encode(imgb.getvalue()).decode()
    
    plt.show()
    plt.clf()         
    
            
      
    # plt.savefig(img, format='png')
    # img.seek(0)
    # plot_url = base64.b64encode(img.getvalue())
    # response = make_response(img.getvalue())
    # response.headers['Content-Type'] = 'image/png'
    # return response
    
    return render_template('search.html', plot_url=plot_url )


@app.route('/pie', methods=['GET'])
def piec():
    rangefrom2 = str(request.args.get('rangefrom2',''))
    rangeto2 =str(request.args.get('rangeto2',''))
    return piechart(rangefrom2,rangeto2)


def barchart(rangefrom3=None,rangeto3=None):
    dbconn =pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:snigdhasqlserver.database.windows.net,1433;Database=adbdb;Uid=snigdha;Pwd=5190$Niggi;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
    #dbconn = pypyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = dbconn.cursor()
    ss = float((float(rangeto3)-float(rangefrom3))/5)
    print(ss)
    performance=[]
    labels=[]
    j1 = float(rangefrom3)
    k1=0
    #img=BytesIO()
    for i in range(0,int(5)):
          k1= j1+ss
          success="SELECT count(*) from all_month where mag between '"+str(j1)+"'and '"+str(k1)+"'"
          cursor.execute(success)
          result_set = cursor.fetchall()
          print(result_set)
          rows=[]
          for row in result_set:
              performance.append(row[0])
              labels.append('magrange'+str(round(j1,2))+' and '+str(round(k1,2)))
          j1=k1
    print(labels)
    print(performance)
    y_pos = np.arange(len(labels))
    plt.bar(y_pos, performance, align='center', alpha=0.5, color='darkorange')
    plt.xticks(y_pos, labels)
    plt.ylabel('Count')
    plt.title('barchart')
    imgc=BytesIO()
    
    plt.savefig(imgc, format='png')
    imgc.seek(1)

    plot_url = base64.b64encode(imgc.getvalue()).decode()
    
    plt.show()
    plt.clf()
    
    return render_template('search.html', plot_url=plot_url )

		

@app.route('/bar', methods=['GET'])
def barc():
    rangefrom3 = str(request.args.get('rangefrom3',''))
    rangeto3 = str(request.args.get('rangeto3',''))
   
    return barchart(rangefrom3,rangeto3) 	






@app.route('/')
def hello_world():
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
