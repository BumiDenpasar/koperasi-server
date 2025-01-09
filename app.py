# app.py
from flask import Flask
from flask_cors import CORS
from config import config_by_name
from extensions import db, jwt
from users.routes import users
from transactions.routes import transactions
from saldo.routes import saldo
from dotenv import load_dotenv

load_dotenv()

def create_app(config_name='dev'):
    app = Flask(__name__)
    CORS(app)
    
    # Load config
    app.config.from_object(config_by_name[config_name])
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    
    # Register blueprints
    app.register_blueprint(users)
    app.register_blueprint(transactions)
    app.register_blueprint(saldo)

    
    return app

if __name__ == "__main__":
    app = create_app('dev')
    app.run()