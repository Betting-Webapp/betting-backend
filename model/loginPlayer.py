from flask import Blueprint, render_template, redirect, url_for

def loginPlayer(mydb, request):
    if request.method == "POST":
        emailAddress = request.form.get("email")
        password = request.form.get("password")
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM userDetails where email_id ='" + str(emailAddress) + "'")
        myresult = mycursor.fetchall()

        if myresult == []:
            return render_template("loginDetails.html")
        if myresult[0][3] == password:
            global currentEmail
            currentEmail = emailAddress
            return redirect(url_for("auth.get_products"))
        else:
            return render_template("loginDetails.html")
    else:
        return render_template("loginDetails.html")