from flask import Flask # Flask is a class
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__) # create first instance of class Flask, parameter will always
# be __name__
app.config.from_object(Config)
#   config subclass of a dictionary
# from_object will go through class attributes

# Create an instance of SQLAlchemy (the ORM) with the Flask Application
db = SQLAlchemy(app)
# Create an instance of Migrate which will be our migration engine and pass in the app and SQLAlchemy instance
migrate = Migrate(app, db)



from . import routes, models