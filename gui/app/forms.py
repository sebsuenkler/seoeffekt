from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextField, DateField, SelectMultipleField
from wtforms.fields.html5 import URLField
from wtforms.validators import url
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea
from wtforms import widgets

# sys libs
import os
import os, sys
import os.path
import json
sys.path.insert(0, '..')

#db libs
from db.connect import DB
from libs.scrapers import Scrapers
from libs.queries import Queries
from libs.results import Results
from libs.studies import Studies
from libs.evaluations import Evaluations
from libs.helpers import Helpers
from libs.sources import Sources


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class Form(FlaskForm):

    study_list = SelectField(label='Select study')
    study_name = StringField(u'or create a new study')
    submit = SubmitField('Start')


class StudyForm(FlaskForm):
    study_name = StringField(u'Name of the study')
    study_description = StringField(u'Description of the study', widget=TextArea())
    study_se = StringField(u'Search Engines')
    study_queries = StringField(u'Queries (one query per row', widget=TextArea())
    submit = SubmitField('Edit')

class editStudyForm(FlaskForm):
    study_name = StringField(u'Name of the study')
    study_description = StringField(u'Description of the study', widget=TextArea())
    study_se = MultiCheckboxField('Search Engines')
    study_delete = StringField(u'Type DELETE if you want to delete the study')
    study_queries = StringField(u'Queries (one query per row', widget=TextArea())
    submit = SubmitField('Save')


class insertStudyForm(FlaskForm):
    study_name = StringField(u'Name of the study')
    study_description = StringField(u'Description of the study', widget=TextArea())
    study_se = MultiCheckboxField('Search Engines')
    submit = SubmitField('Save')
