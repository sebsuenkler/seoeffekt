from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import URLField
from wtforms.validators import url
from wtforms.validators import DataRequired

class URLForm(FlaskForm):
    url = URLField(label="URL to check:", validators=[url()])
    submit = SubmitField('Check')
