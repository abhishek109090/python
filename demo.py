from flask import Flask,request,jsonify
import mysql.connector
from mysql.connector import Error

from flask_cors import CORS


app = Flask(__name__)
CORS(app)

def myfun():
    connection= None
    try:
        connection = mysql.connector.connect(
         host= '107.180.116.73',
    port= '3306',
    user= 'rvlc82',
    password= 'MRVTechnology@123',
    database= 'mrvtech'
        )
    except Error as e:
        print(f"the error is '{e}'")
    return connection

@app.route('/')
def fetch():
    return 'hello world'
@app.route('/items/<int:id>',methods=["GET"])
def getitems(id):
    connection=myfun()
    cursor = connection.cursor(dictionary=True) 
    cursor.execute('select * from login1 where id = %s',(id,))
    item = cursor.fetchone()
    cursor.close()
    connection.close()
    if item:
        return jsonify(item)
    else:
        return jsonify({"error":"items not found"})


@app.route('/postitem',methods=["POST"])
def createitem():
    data=request.get_json()
    phone = data.get('phone')
    password=data.get('password')
    connection =myfun()
    cursor = connection.cursor()
    cursor.execute("insert into login1 (phone,password) values(%s,%s)",(phone,password))
    connection.commit()
    itemid=cursor.lastrowid
    cursor.close()
    connection.close()
    return jsonify({"message":"item added to the database"}),200

@app.route('/items/<int:id>',methods=["PUT"])
def updateitem(id):
    data=request.get_json()
    phone = data.get('phone')
    password=data.get('password')
    connection =myfun()
    cursor = connection.cursor()
    cursor.execute("update login1 set phone=%s,password= %s where id=%s",(phone,password,id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message":"item updated successfully"})

@app.route('/del/<int:id>',methods=["DELETE"])
def delitem(id):
    connection= myfun()
    cursor = connection.cursor()
    cursor.execute("delete from login1 where id = %s",(id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message":"item deleted"})

if __name__=="__main__":
    app.run(debug=True)

    