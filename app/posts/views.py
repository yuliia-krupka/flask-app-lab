from . import post_bp
from flask import render_template, abort, flash, url_for, redirect, session, json, request
from .forms import PostForm
from .models import Post
from app import db


@post_bp.route('/add_post', methods=["GET", "POST"])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        posted = form.publish_date.data
        category = form.category.data
        is_active = form.is_active.data
        author = session.get('username')
        new_post = Post(title=title, content=content, posted=posted, category=category, author=author,
                        is_active=is_active)
        db.session.add(new_post)
        db.session.commit()

        flash(f"Post {title} added successfully!", "success")
        return redirect(url_for(".get_posts"))
    elif request.method == "POST":
        flash(f"Enter the correct data in the form!", "danger")
    return render_template("add_post.html", form=form)


@post_bp.route('/')
def get_posts():
    stmt = db.select(Post).order_by(Post.posted.desc())
    posts = db.session.scalars(stmt).all()
    return render_template("posts.html", posts=posts)


@post_bp.route('/<int:id>')
def detail_post(id):
    post = db.get_or_404(Post, id)
    return render_template("detail_post.html", post=post)


@post_bp.route('/delete/<int:id>', methods=["POST"])
def delete_post(id):
    post = db.get_or_404(Post, id)
    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title}' has been deleted successfully!", "success")
    return redirect(url_for('.get_posts'))


@post_bp.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = db.get_or_404(Post, post_id)
    form = PostForm(obj=post)

    form.publish_date.data = post.posted

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.is_active = form.is_active.data
        # post.author = session.get('username')
        post.category = form.category.data
        db.session.commit()

        flash('Post updated successfully!', 'success')
        return redirect(url_for('.get_posts'))

    return render_template('add_post.html', form=form)
