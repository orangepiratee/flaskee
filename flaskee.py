#!/usr/bin/env python
import os
from app import create_app, db
from app.models import *
from flask_migrate import Migrate


#app = create_app('production')
app = create_app('development')

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)


if __name__ == '__main__':
    #db.app = app
    #db.create_all()
    app.run()