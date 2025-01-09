from app import create_app
from extensions import db

app = create_app('dev')

with app.app_context():
    db.create_all()
    print("Database tables created successfully!")