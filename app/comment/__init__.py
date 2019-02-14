#!/usr/bin/env python

from flask import Blueprint

comment = Blueprint('comment', __name__)

from . import views, errors, forms
