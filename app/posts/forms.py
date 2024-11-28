from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, DateField, SelectField
from wtforms.fields.choices import SelectMultipleField
from wtforms.fields.datetime import DateTimeLocalField
from wtforms.validators import DataRequired, Length
from datetime import datetime as dt


CATEGORIES = [('tech', 'Tech'), ('science', 'Science'), ('lifestyle', 'Lifestyle')]


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=2, max=100)])
    content = TextAreaField("Content", render_kw={"rows": 5, "cols": 40}, validators=[DataRequired()])
    is_active = BooleanField("Is this post active?", default=True)
    publish_date = DateTimeLocalField("Publish date", format='%Y-%m-%dT%H:%M', default=dt.now(),
                                      validators=[DataRequired()])
    category = SelectField("Category", choices=CATEGORIES, validators=[DataRequired()])
    author = SelectField("Author", coerce=int)
    tags = SelectMultipleField("Tags", coerce=int)

    submit = SubmitField("Add Post")
