from flask import Flask
from extensions import db, jwt
from models import User, Book
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configure the app
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600)))
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_SECURE'] = False  # Set to True in production
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # Set to True in production
    app.config['JWT_COOKIE_SAMESITE'] = None  # Set to 'Lax' in production
    
    db.init_app(app)
    jwt.init_app(app)
    
    from routes.auth import auth
    from routes.books import books
    
    app.register_blueprint(auth, url_prefix='/api/auth')
    app.register_blueprint(books, url_prefix='/api/books')
    
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0')