#!/usr/bin/env python

from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, SubmitField, TextAreaField, TextField, RadioField
from wtforms.validators import DataRequired, Length

class ItemForm(FlaskForm):
    title = StringField('Title here', validators=[DataRequired(),Length(1,254)])
    content = CKEditorField('Content here',validators=[DataRequired()])
    classification = RadioField('Classification here', choices=((1,'A'),(2,'B')))
    submit = SubmitField('Submit',render_kw={'class':'btn btn-small btn-success'})