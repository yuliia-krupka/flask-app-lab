from flask import Blueprint

user_bp = Blueprint("users",
                    __name__,
                    url_prefix="/user",
                    template_folder="templates/users",
                    static_folder="static",
                    static_url_path="/static/users"
                    )

from . import views