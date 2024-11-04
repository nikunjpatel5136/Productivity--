from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user

from website.models import User
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)

@auth.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Successfully Logged In", category= "success")
                login_user(user, remember= "True")      #remembers that the user is logged in
                return redirect(url_for("views.home"))  #once the account is created, redirect the user to the home page
            else:
                flash("Incorrect Password. Please Try Again.", category= "error")
        else:
            flash("Email does not exist.", category= "error")

        

                
        
    return render_template("login.html", user = current_user)

@auth.route("/logout")
@login_required                 #this is a Decorator that makes sure that we can not access this unless the user is logged in
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/sign-up", methods = ["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists.", category= "error")
        elif len(email) < 4:
            flash("Email must be greater than 4 characters", category = "error")
        elif len(firstName) <2:
            flash("First Name must be greater than 1 character", category = "error")
        elif password1 != password2:
            flash("Passwords do not match", category = "error")

        elif len(password1) < 8:
            flash("Password must be at least 8 characters", category = "error")

        else:
            new_user = User(email = email, first_name = firstName, password = generate_password_hash(password1, method="scrypt")) #hashing to define password
            db.session.add(new_user) #makes new user
            db.session.commit()
                        
            #add user to database
            flash("Account Created", category = "success")
            return redirect(url_for("views.home")) #once the account is created, redirect the user to the home page

            


    return render_template("sign_up.html", user = current_user)
