from . import post_bp
from flask import render_template, abort, flash, url_for, redirect, session, json, request
from .forms import PostForm
from .models import Post
from app import db

from .utils import load_posts, save_post, get_post


@post_bp.route('/add_post', methods=["GET", "POST"])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        publish_date = form.publish_date.data.strftime('%d.%m.%Y')
        category = form.category.data
        is_active = form.is_active.data
        author = session.get('username')
        # обробка логіки
        new_post = Post(title=title, content=content)
        # save_post(new_post)

        db.session.add(new_post)
        db.session.commit()

        flash(f"Post {title} added successfully!", "success")
        return redirect(url_for(".get_posts"))
    elif request.method == "POST":
        flash(f"Enter the correct data in the form!", "danger")
    return render_template("add_post.html", form=form)


@post_bp.route('/')
def get_posts():
    stmt = db.select(Post).order_by(Post.title)
    posts = db.session.scalars(stmt).all()
    return render_template("posts.html", posts=posts)


@post_bp.route('/<int:id>')
def detail_post(id):
    post = get_post(id)
    if not post:
        return abort(404)
    return render_template("detail_post.html", post=post)
