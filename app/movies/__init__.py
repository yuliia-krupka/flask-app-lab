from flask import Blueprint

movie_bp = Blueprint("movies",
                     __name__,
                     url_prefix="/movie",
                     template_folder="templates/movies",
                     static_folder="static",
                     static_url_path="static_for_movies"
                     )

from . import views
