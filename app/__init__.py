#!/usr/bin/env python

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from config import config
from flask_login import LoginManager
import os



bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
ckeditor = CKEditor()
login_manager = LoginManager()
login_manager.login_view = 'auth.signin'

base_dir = os.path.dirname(__file__)

pt1=['Items','Posters']
pt2=['Read','Write','Modify','List','Manage']
pt3=['Category','Author','Id']


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)


    #register blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .item import item as item_blueprint
    app.register_blueprint(item_blueprint, url_prefix='/item')

    from .comment import comment as comment_blueprint
    app.register_blueprint(comment_blueprint, url_prefix='/comment')

    from .post import post as post_blueprint
    app.register_blueprint(post_blueprint, url_prefix='/post')

    return app


