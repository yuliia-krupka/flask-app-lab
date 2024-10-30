from . import user_bp
from flask import render_template, request, redirect, url_for, make_response, session, flash
from datetime import datetime, timedelta

@user_bp.route('/profile')
def get_profile():
    if "username" in session:
        username_value = session["username"]
        return render_template("profile.html", username=username_value)
    flash("Invalid: Session.", "danger")
    return redirect(url_for("users.login"))

@user_bp.route("/login",  methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form["login"]
        session["username"] = username
        flash("Success: session added successfully.", "success")
        return redirect(url_for("users.get_profile"))
    return render_template("login.html")

@user_bp.route('/logout')
def logout():
    # Видалення користувача із сесії
    session.pop('username', None)
    return redirect(url_for("users.get_profile"))



@user_bp.route('/hi/<string:name>')     # /hi/ivan?age=30
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)
    return render_template("hi.html", name=name, age=age)

@user_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)   #"http://localhost:8080/hi/administrator?age=45"
    print(to_url)
    return redirect(to_url)

@user_bp.route('/set_cookie')
def set_cookie():
    response = make_response('Кука встановлена')
    response.set_cookie('username', 'student', max_age=timedelta(seconds=60))
    return response

@user_bp.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    return f'Користувач: {username}'

@user_bp.route('/delete_cookie')
def delete_cookie():
    response = make_response('Кука видалена')
    response.set_cookie('username', '', expires=0) # response.set_cookie('username', '', max_age=0)
    return response