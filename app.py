from flask import Blueprint, render_template, request, flash, redirect, url_for, Flask
from model.registerPlayer import registerPlayer
from model.loginPlayer import loginPlayer
import mysql.connector
from datetime import datetime
from PIL import Image
import json
import os
# import marketplace

mydb = mysql.connector.connect(
    user="Nishad", 
    password="Game@1998",
    host="betting-game.mysql.database.azure.com",
    port=3306,
    database="bettinggame", 
    ssl_ca="DigiCertGlobalRootCA.crt.pem", 
    ssl_disabled=False
    )

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registerPlayer",  methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("registerDetails.html")
    else:
        print("Hello")
        registerPlayer(mydb, request)
        return render_template("index.html")
    
@app.route("/loginPlayer",  methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("loginDetails.html")
    else:
        loginPlayer(mydb, request)
        return render_template("index.html")


@app.route("/bet", methods=["POST"])
def bet():
    if request.method == "POST":
        user_bet = request.form["bet"]
        coin_toss_result = random.choice(["heads", "tails"])

        if user_bet == coin_toss_result:
            result = "You win!"
        else:
            result = "You lose."

        return render_template("result.html", user_bet=user_bet, result=result, coin_toss_result=coin_toss_result)

if __name__ == "__main__":
    app.run(debug=True)
