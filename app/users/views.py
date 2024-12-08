from werkzeug.utils import secure_filename
import uuid as uuid
import os

from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import select

from . import user_bp
from flask import render_template, request, redirect, url_for, make_response, session, flash
from datetime import timedelta

from .forms import RegistrationForm, LoginForm, UpdateAccountForm, ChangePasswordForm
from .models import User
from .. import db
from flask import current_app


@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def get_profile():
    color_theme = request.cookies.get('color_theme', 'light')
    cookies = request.cookies

    if request.method == 'POST':
        if 'add_cookie' in request.form:
            key = request.form['cookie_key']
            value = request.form['cookie_value']
            duration = request.form.get('cookie_duration', type=int)
            response = make_response(redirect(url_for('users.get_profile')))
            response.set_cookie(key, value, max_age=duration)
            flash("Cookie was added successfully!", "success")
            return response

        elif 'delete_cookie' in request.form:
            key = request.form['cookie_key_delete']
            response = make_response(redirect(url_for('users.get_profile')))
            response.set_cookie(key, '', expires=0)
            flash("Cookie was deleted successfully!", "success")
            return response

        elif 'delete_all_cookies' in request.form:
            response = make_response(redirect(url_for('users.get_profile')))
            for key in cookies:
                response.set_cookie(key, '', expires=0)
            flash("All cookies were deleted successfully", "success")
            return response

    return render_template(
        "profile.html",
        username=current_user.username,
        cookies=cookies,
        color_theme=color_theme
    )


@user_bp.route('/set_color_theme', methods=['POST'])
def set_color_theme():
    color_theme = request.form['color_theme']
    response = make_response(redirect(url_for('users.get_profile')))
    response.set_cookie('color_theme', color_theme, max_age=2592000)
    return response


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


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = User.hash_password(form.password.data)

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()

        flash(f'Account for {form.username.data} was created!', 'success')
        return redirect(url_for('users.login'))

    return render_template('register.html', form=form, title='Register')


@user_bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user, remember=form.remember.data)
            flash('You logged in successfully!', 'success')
            return redirect(url_for('users.account'))
        flash("Error: Invalid username or password.", "danger")
    return render_template("login.html", form=form, title='Login')


@user_bp.route("/account")
@login_required
def account():
    return render_template("account.html", title="Account")


@user_bp.route("/update_account", methods=['GET', 'POST'])
@login_required
def update_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        if form.image.data:
            pic_filename = secure_filename(form.image.data.filename)
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            save_path = os.path.join(current_app.root_path, 'users/static/images', pic_name)
            form.image.data.save(save_path)
            current_user.image_file = pic_name
        db.session.commit()
        flash('Your account was updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    return render_template('update_account.html', form=form)


@user_bp.route("/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.change_password(form.new_password.data)
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('users.account'))
    return render_template('change_password.html', form=form)


@user_bp.route('/logout')
def logout():
    logout_user()
    flash("You have successfully logged out.", "info")
    return redirect(url_for("users.login"))


@user_bp.route('/get_all_users', methods=['GET'])
@login_required
def get_all_users():
    users = db.session.execute(select(User)).scalars().all()
    return render_template('users.html', users=users)
