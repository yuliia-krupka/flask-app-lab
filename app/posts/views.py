from . import post_bp
from flask import render_template, abort, flash, url_for, redirect, session, json
from .forms import PostForm

try:
    with open('posts.json', 'r') as f:
        posts = json.load(f)
except FileNotFoundError:
    posts = []


@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        new_id = max([post['id'] for post in posts], default=0) + 1
        id = new_id
        title = form.title.data
        content = form.content.data
        publish_date = form.publish_date.data.strftime('%d.%m.%Y')
        category = form.category.data
        is_active = form.is_active.data
        author = session.get('username')

        new_post = {
            'id': id,
            'title': title,
            'content': content,
            'publish_date': publish_date,
            'category': category,
            'is_active': is_active,
            'author': author
        }

        posts.append(new_post)

        with open('posts.json', 'w') as f:
            json.dump(posts, f, indent=2)

        # обробка логіки
        flash(f"Post {title} added successfully! ", "success")
        return redirect(url_for(".get_posts"))
    return render_template("add_post.html", form=form)


@post_bp.route('/')
def get_posts():
    return render_template("posts.html", posts=posts)


@post_bp.route('/<int:id>')
def detail_post(id):
    post = next((p for p in posts if p['id'] == id), None)
    if post:
        return render_template('detail_post.html', post=post)
    else:
        abort(404)
