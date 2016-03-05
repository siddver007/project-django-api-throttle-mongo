from mongoengine import *
from django.conf import settings
import datetime

connect(settings.DBNAME)

# User model to create a user collection
class User(Document):
    name = StringField(max_length=120, required=True)
    user_id = StringField(max_length=120, required=True , unique = True)
    password = StringField(max_length=120, required=True)
    plan = StringField(max_length=120, required=True)
    dateModified = DateTimeField(default = datetime.datetime.now, required = True)
    isVerified = BooleanField(required = True)
    counter = IntField(required = True)

# Data model to create a data collection
class Data(Document):
    user_id = StringField(max_length=120, required = True)
    content = StringField(required = True)
    