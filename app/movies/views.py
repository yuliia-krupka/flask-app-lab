from app.movies.forms import MovieForm, MovieSearchForm
from app.movies.models import Movie, Genre

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from . import movie_bp


@movie_bp.route('/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie():
    form = MovieForm()
    form.genres.choices = [(genre.id, genre.name) for genre in Genre.query.all()]

    if form.validate_on_submit():
        selected_genres = form.genres.data

        movie = Movie.query.filter(
            Movie.title == form.title.data,
            Movie.year == form.year.data,
            Movie.genres.any(Genre.id.in_(selected_genres))
        ).first()

        if not movie:
            movie = Movie(
                title=form.title.data,
                year=form.year.data,
                description=form.description.data,
                rate=form.rate.data,
                user_id=current_user.id,
            )
            db.session.add(movie)
            db.session.commit()

            genres = Genre.query.filter(Genre.id.in_(selected_genres)).all()
            movie.genres.extend(genres)
            db.session.commit()

            flash("Movie added successfully!", "success")
        else:
            flash("This movie already exists.", "info")

        return redirect(url_for('.get_user_movies'))

    return render_template('add_movie_form.html', form=form)


@movie_bp.route('/get_user_movies')
@login_required
def get_user_movies():
    movies = current_user.movies
    return render_template('movies_list.html', movies=movies)


@movie_bp.route('/get_movies')
@login_required
def get_movies():
    form = MovieSearchForm()
    stmt = db.select(Movie).order_by(Movie.title)
    movies = db.session.scalars(stmt).all()
    return render_template('all_movies_list.html', movies=movies, form=form)


@movie_bp.route('/search_movies', methods=['POST'])
@login_required
def search_movies():
    form = MovieSearchForm()
    movies = []

    if form.validate_on_submit():
        search_query = form.search_query.data
        search_field = form.search_field.data

        if search_field == 'title':
            movies = Movie.query.filter(Movie.title.ilike(f'%{search_query}%')).all()

        elif search_field == 'genre':
            if not search_query.isdigit():
                movies = Movie.query.join(Movie.genres).filter(Genre.name.ilike(f'%{search_query}%')).all()
            else:
                flash("Please enter a valid genre", "danger")
                return redirect(url_for('.search_movies'))

        elif search_field == 'rate':
            if search_query.isdigit():
                rate = int(search_query)
                if 1 <= rate <= 10:
                    movies = Movie.query.filter(Movie.rate == rate).all()
                else:
                    flash("Please enter a valid rating (between 1 and 10)", "danger")
                    return redirect(url_for('.search_movies'))
            else:
                flash("Please enter a valid rating (integer)", "danger")
                return redirect(url_for('.search_movies'))

    return render_template('search_movies.html', form=form, movies=movies, search_query=search_query,
                           search_field=search_field)


@movie_bp.route('/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def get_movie(movie_id):
    movie = db.get_or_404(Movie, movie_id)
    return render_template('movie_details.html', movie=movie, current_user=current_user)


@movie_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_movie(id):
    movie = db.get_or_404(Movie, id)

    if movie.author != current_user:
        flash("You are not authorized to delete this movie.", "danger")
        return redirect(url_for('.get_movies'))

    db.session.delete(movie)
    db.session.commit()
    flash("Movie deleted successfully!", "success")
    return redirect(url_for('.get_movies'))


@movie_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_movie(id):
    movie = db.get_or_404(Movie, id)

    if movie.user_id != current_user.id:
        flash("You are not authorized to edit this movie.", "danger")
        return redirect(url_for('.get_user_movies'))

    form = MovieForm(obj=movie)
    form.genres.choices = [(genre.id, genre.name) for genre in Genre.query.all()]

    if form.validate_on_submit():
        movie.title = form.title.data
        movie.description = form.description.data
        movie.rate = form.rate.data
        movie.year = form.year.data

        selected_genre_ids = form.genres.data
        movie.genres = Genre.query.filter(Genre.id.in_(selected_genre_ids)).all()

        db.session.commit()
        flash("Movie updated successfully!", "success")
        return redirect(url_for('.get_user_movies'))
    if request.method == 'GET':
        form.genres.data = [genre.id for genre in movie.genres]

    return render_template('edit_movie.html', form=form, movie=movie)
