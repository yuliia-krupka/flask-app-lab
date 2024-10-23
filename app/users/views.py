from . import user_bp
from flask import render_template, request, redirect, url_for


@user_bp.route('/hi/<string:name>')     # /hi/ivan?age=30
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)
    return render_template("hi.html", name=name, age=age)

@user_bp.route('/admin')
def admin():
    to_url = url_for("users.greetings", name="administrator", _external=True)   # --> "/hi/admin"
    print(to_url)
    return redirect(to_url)