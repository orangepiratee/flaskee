#!/usr/bin/env python

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, TextField
from wtforms.validators import DataRequired, Length

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('create table')

class ItemForm(FlaskForm):
    title = TextAreaField('Title here', validators=[DataRequired(),Length(1,254)])
    content = TextAreaField('Content here', validators=[DataRequired()])
    submit = SubmitField('Submit')