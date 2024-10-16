from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/')
def main():
    return render_template("hello.html")

@app.route('/homepage')
def home():
    """View for the Home page of your website."""
    agent = request.user_agent
    return render_template("home.html", agent=agent)

@app.route('/hi/<string:name>')     # /hi/ivan?age=30
def greetings(name):
    name = name.upper()
    age = request.args.get("age", 0)
    return f"Welcome {name=} {age=}"

@app.route('/admin')
def admin():
    to_url = url_for("greetings", name="administrator", _external=True)   # --> "/hi/admin"
    print(to_url)
    return redirect(to_url)


if __name__ == '__main__':
    app.run(debug=True)
