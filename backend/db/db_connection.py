from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from db.db_config import USERNAME, PASSWORD, HOST, DATABASE

db = SQLAlchemy()

def db_connection(app):

    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)
    print(db)

