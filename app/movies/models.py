from app import db

movie_genres = db.Table('movie_genres',
                        db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
                        db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True)
                        )


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    year = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.Integer, nullable=False)

    genres = db.relationship('Genre', secondary=movie_genres, back_populates='movies')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # поле визначає людину, яка створила запис про фільм
    author = db.relationship('User', backref='movies', lazy=True)

    def __repr__(self):
        return f'<Movie {self.title}>'


class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200))

    movies = db.relationship('Movie', secondary=movie_genres,
                             back_populates='genres')

    def __repr__(self):
        return f'<Genre {self.name}>'
