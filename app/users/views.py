from . import user_bp
from flask import render_template, request, redirect, url_for, make_response, session, flash
from datetime import timedelta


@user_bp.route('/profile', methods=['GET', 'POST'])
def get_profile():
    if "username" in session:
        username_value = session["username"]
        color_theme = request.cookies.get('color_theme', 'light')
        cookies = request.cookies
        if request.method == 'POST':
            if 'add_cookie' in request.form:
                key = request.form['cookie_key']
                value = request.form['cookie_value']
                duration = request.form.get('cookie_duration', type=int)
                response = make_response(redirect(url_for('users.get_profile')))
                response.set_cookie(key, value, max_age=duration)
                flash(f"Cookie was added successfully!", "success")
                return response

            elif 'delete_cookie' in request.form:
                key = request.form['cookie_key_delete']
                response = make_response(redirect(url_for('users.get_profile')))
                response.set_cookie(key, '', expires=0)
                flash(f"Cookie was deleted successfully!", "success")
                return response

            elif 'delete_all_cookies' in request.form:
                response = make_response(redirect(url_for('users.get_profile')))
                for key in cookies:
                    response.set_cookie(key, '', expires=0)
                flash("All cookies were deleted successfully", "success")
                return response

        return render_template("profile.html", username=username_value, cookies=cookies, color_theme=color_theme)
    else:
        flash("Error: access denied. Please login.", "danger")
        return redirect(url_for("users.login"))


@user_bp.route('/set_color_theme', methods=['POST'])
def set_color_theme():
    color_theme = request.form['color_theme']
    response = make_response(redirect(url_for('users.get_profile')))
    response.set_cookie('color_theme', color_theme, max_age=2592000)
    return response


@user_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        valid_username = "user12"
        valid_password = "password"

        if username == valid_username and password == valid_password:
            session["username"] = username
            flash("Success: session added successfully.", "success")
            return redirect(url_for("users.get_profile"))
        else:
            flash("Error: Invalid username or password.", "danger")
            return redirect(url_for("users.login"))
    return render_template("login.html")


@user_bp.route('/logout')
def logout():
    # Видалення користувача із сесії
    session.pop('username', None)
    flash("You have successfully logged out.", "info")
    return redirect(url_for("users.login"))


@user_bp.route('/hi/<string:name>')  # /hi/ivan?age=30
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)
    return render_template("hi.html", name=name, age=age)


@user_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45,
                     _external=True)  # "http://localhost:8080/hi/administrator?age=45"
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
    response.set_cookie('username', '', expires=0)  # response.set_cookie('username', '', max_age=0)
    return response
