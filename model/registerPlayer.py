from flask import Blueprint, render_template, request, flash, redirect, url_for, Flask
import uuid


def registerPlayer(mydb, request):
        if request.method == "POST":
            emailAddress = request.form.get("email")
            password = request.form.get("password")
            confirmPassword = request.form.get("confirmPassword")
            if password != confirmPassword or len(emailAddress) == 0:
                return render_template("registerDetails.html", text = "In register Customer")
            
            mycursor = mydb.cursor()
            sql = "SELECT email_id from userDetails"
            mycursor.execute(sql)
            emails = mycursor.fetchall()

            if emailAddress in emails:
                return render_template("registerDetails.html", text = "In register Customer")

            firstName = request.form.get("firstName")
            lastName = request.form.get("lastName")
            contact = request.form.get("contact")

            if len(firstName) == 0 or len(lastName) == 0 or len(contact) == 0:
                return render_template("registerDetails.html", text = "In register Customer")

            answerOne = request.form.get("answerOne")
            answerTwo = request.form.get("answerTwo")
            answerThree = request.form.get("answerThree")

            if len(answerOne) == 0 or len(answerTwo) == 0 or len(answerThree) == 0:
                return render_template("registerDetails.html", text = "In register Customer")
            
            
            new_uuid = uuid.uuid4() 
            mycursor = mydb.cursor()
            print(new_uuid)
            print(type(new_uuid))
            sql = "INSERT INTO userDetails (id, email_id, firstName, lastName, password, contact) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (str(new_uuid), emailAddress, firstName, lastName, password, contact)

            mycursor.execute(sql, values)
            mydb.commit()

            mycursor = mydb.cursor()
            sql = "INSERT INTO resetpassword (email_id, answer_one, answer_two, answer_three) VALUES (%s, %s, %s, %s)"
            values = (emailAddress, answerOne, answerTwo, answerThree)
            mycursor.execute(sql, values)
            mydb.commit()
            return render_template("loginDetails.html")
        return render_template("registerDetails.html", text = "In register Customer")