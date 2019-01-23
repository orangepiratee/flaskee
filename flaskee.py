#!/usr/bin/env python
import os
from app import create_app, db
from app.models import *
from flask_migrate import Migrate


#app = create_app('production')
#app = create_app('development')



if __name__ == '__main__':
    #db.app = app
    #db.create_all()
    str = input('input the mode:')
    app = create_app(str)
    app.run()