from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.fields.choices import SelectMultipleField, SelectField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, Length, NumberRange


class MovieForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=1888, max=2024)])
    rate = IntegerField('Rate', validators=[DataRequired(), NumberRange(min=1, max=10)])
    genres = SelectMultipleField(
        'Genres',
        coerce=int
    )

    submit = SubmitField('Add Movie')


class MovieSearchForm(FlaskForm):
    search_field = SelectField('Search By', choices=[
        ('title', 'Title'),
        ('genre', 'Genre'),
        ('rate', 'Rating')
    ], validators=[DataRequired()])
    search_query = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')
