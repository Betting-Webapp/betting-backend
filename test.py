import mysql.connector
import uuid
import ast
import random


mydb = mysql.connector.connect(
    user="admin", 
    password="bettingTrial",
    host="bettingtrial.cxodugipf8wx.us-east-2.rds.amazonaws.com",
    port=3306,
    database="bettingGame",
    ssl_ca="./certs/rds-combined-ca-bundle.pem",
    ssl_disabled=False
    )

print("Testing Code")

random_list = []
for i in range(10):
    random_list.append(random.randint(0,200))
print(random_list)

# mycursor = mydb.cursor()
# mycursor.execute("select * from playerbalances where gameuuid = %s and is_active = %s and skip_round = %s;", (1, True, False))
# games = mycursor.fetchall()
# print(games, type(games))

# playeruuids = ['4e2ab68e-ae7b-46b6-b55e-36b6a7581e2f', '9b4f332e-aaa4-4535-8dda-e59eb9e7d3d6', '63c63de7-ac5d-4c17-81da-11478ea59c98', 'f328eed1-23df-497c-889a-14b63fc96888', 'fc4a14c1-e757-4f4e-ad22-defbad94b3f4', 'e1232e41-6d83-42f8-be4a-0ac96d0aa8ad', '69b8e25c-1b19-4c1c-a7a3-5ed5aae7a942', 'cbccde07-7aa5-42ee-8b87-b025d7151bd4', '5ae4d0bb-5165-481b-957c-369200159197', '354645ca-c70a-47d8-94bf-c2c5cb3d0d27']
# for pu in playeruuids:
#     try:
#         mycursor = mydb.cursor()
#         mycursor.execute("SELECT * FROM playerbalances WHERE gameuuid=%s AND playeruuid=%s", ("4c0d20dc-5bc9-4dd8-9486-9caa0debd1c9", pu))
#         games = mycursor.fetchall()[0]
#         print(games, type(games))
#     except:
#         print('User not available', pu)


# new_uuid = uuid.uuid4()
# sql = "INSERT INTO userDetails (id, email_id, firstName, lastName, password, contact) VALUES (%s, %s, %s, %s, %s, %s)"
# values = (str(new_uuid), "test9@iu.edu", "Test", "Nine", "test9", "1111111111")
# mycursor = mydb.cursor()
# mycursor.execute(sql, values)
# mydb.commit()

# mycursor = mydb.cursor()
# uu = '0f87afa4-9023-4925-95ce-5a990fbd0464'
# mycursor.execute("select * from gamesDetail where gameuuid=%s", (uu,))
# games = mycursor.fetchall()
# print(len(ast.literal_eval(games[0][1])))

