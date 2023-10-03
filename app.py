from flask import Blueprint, render_template, request, flash, redirect, url_for, Flask
from model.registerPlayer import registerPlayer
from model.loginPlayer import loginPlayer
import mysql.connector
from datetime import datetime
from PIL import Image
import json
import os
# import marketplace

from flask_socketio import SocketIO, emit, join_room, close_room #, rooms, leave_room

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
socketio = SocketIO(app)

route_users = {}
game_bets = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/game/<route>')
def game(route):
    return render_template('game.html', route=route)

@app.route('/test',  methods = ["GET", "POST"])
def test():
    if request.method == "GET":
        return render_template("test.html")
    else:
        return redirect(url_for('game', route=1))

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

@socketio.on('listGames')
def listGames():
    gameRooms = { roomNumber: len(route_users[roomNumber]) for roomNumber in route_users }
    emit('get_games_list', { 'rooms': gameRooms, 'user': request.sid }, broadcast=False)

@app.route("/selectGame", methods = ["POST"])
def selectGame():
    data = request.get_json()
    print('selected room', data)
    # return redirect(url_for('game', route=str(data)), code=302)
    return {'url': 'game/'+str(data)}


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
    
@app.route('/makeBets/<route>', methods=["GET", "POST"])
def makeBets(route):
    if request.method == "POST":
        emailAddress = request.form.get("email")
        password = request.form.get("password")

        print(emailAddress, password)
        game_bets.append((emailAddress, password))
        print(route, 'game bets', game_bets)
        # user_bet = request.form["bet"]
        # coin_toss_result = random.choice(["heads", "tails"])

        # if user_bet == coin_toss_result:
        #     result = "You win!"
        # else:
        #     result = "You lose."

        return render_template("result.html", user_bet=1, result=1, coin_toss_result=1)
    print("~~~~~~ MAKE YOUR BETS ~~~~~~~")
    return render_template("makeBets.html")

@app.route('/winner', methods=["GET"])
def winner():
    return render_template("winner.html")

@app.route('/loser', methods=["GET"])
def loser():
    return render_template("loser.html")

@socketio.on('determine_winner')
def determine_winner():
    route = request.args.get('route')

@socketio.on('connect')
def handle_connect():
    route = request.args.get('route')
    print('Connected, args route = ', route)

@socketio.on('join')
def join(route_info):
    r = request.args.get('route')
    print('args route', r)
    route = route_info['route']
    if route not in route_users:
        route_users[route] = []

    if len(route_users[route]) < 3:
        route_users[route].append(request.sid)
        print(route_users)
        join_room(route)
        emit('message', {'data': 'Connected', 'count': len(route_users[route])}, room=r)
        print('route', route, 'num users', route_users[route])
        if len(route_users[route]) == 3:
            print('here')
            emit('start_game', {'route': route}, broadcast=True, room=route)
            # return redirect(url_for('login'))
    else:
        emit('message', {'data': 'Room full. Cannot join.'})


@socketio.on('disconnect')
def handle_disconnect():
    route = request.args.get('route')
    if route in route_users:
        route_users[route].remove(request.sid)
        emit('message', {'data': 'Disconnected', 'count': len(route_users[route])}, room=route)


@socketio.on('chat_message')
def handle_message(data):
    route = request.args.get('route')
    emit('chat_message', {'data': data['data'], 'user': request.sid}, broadcast=True, room=route)

@socketio.on('place_bets')
def place_bets(data):
    if data['route'] not in game_bets:
        game_bets[data['route']] = []
    
    game_bets[data['route']].append((request.sid, data['bet']))

    if len(game_bets[data['route']]) == 3:
        sorted_bets = sorted(game_bets[data['route']], key=lambda k: k[1], reverse=True)
        winner = sorted_bets[0][0]
        emit('results_win', to=winner)
        emit('results_lose', to=[sb[0] for sb in sorted_bets[1:]])
        # for sb in sorted_bets:
        #     leave_room(data['route'], sid=sb[0])
        close_room(data['route'])
    


if __name__ == '__main__':
    socketio.run(app, debug=True)

# if __name__ == "__main__":
#     app.run(debug=True)
