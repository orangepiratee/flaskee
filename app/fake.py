from random import randint
from faker import Faker
from sqlalchemy.exc import IntegrityError
from . import db
from .models import *

def Users(count=100):
    faker = Faker()
    i = 0
    while i<count:
        u = User(user_name=faker.user_name(),
                 user_password='password',
                 user_role=1,
                 user_department=0,
                 user_available=1)
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except:
            db.session.rollback()

def Items(count=100):
    faker = Faker()
    i = 0
    while i<count:
        item = Item(item_title=faker.txt(),
                    item_content=faker.txt(),
                    item_author=User.query.count(),
                    item_class=0
                    )
        db.session.add(item)
        try:
            db.session.commit()
            i += 1
        except:
            db.session.rollback()
