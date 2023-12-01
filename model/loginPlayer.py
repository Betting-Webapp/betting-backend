from flask import Blueprint, render_template, redirect, url_for, jsonify
import mysql.connector

def loginPlayer(request):
    mydb = mysql.connector.connect(
        user="admin", 
        password="bettingTrial",
        host="bettingtrial.cxodugipf8wx.us-east-2.rds.amazonaws.com",
        port=3306,
        database="bettingGame",
        ssl_ca="./certs/rds-combined-ca-bundle.pem",
        ssl_disabled=False
    )
    if request.method == "POST":
        data = request.get_json()
        if 'uuid' in data and data['uuid']:
            response_data = {
                'route': 'game-list',
                'uuid': data['uuid'],
                'status': 302
            }
            return jsonify(response_data), 302
        emailAddress = data['emailAddress']
        password = data["password"]
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM userDetails where email_id ='" + str(emailAddress) + "' and password = '" + str(password) + "';")
        myresult = mycursor.fetchall()
        print(myresult)

        if myresult == []:
            response_data = {
                'route': 'login',
                'status': 302
            }
            return jsonify(response_data), 302
        else:
            response_data = {
                'route': 'game-list',
                'uuid': myresult[0][0],
                'status': 302
            }
            return jsonify(response_data), 302

    else:
        response_data = {
            'route': 'login',
            'status': 302
        }
        return jsonify(response_data), 302