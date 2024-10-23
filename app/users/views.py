from . import user_bp
from flask import render_template, request, redirect, url_for, abort


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