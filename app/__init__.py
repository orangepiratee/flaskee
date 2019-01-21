#!/usr/bin/env python

from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment

from flask_sqlalchemy import SQLAlchemy
from config import config

import pymysql,os

from datetime import datetime

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    #routes here

    #register blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


