from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from cryptography.fernet import Fernet
import base64, os

db = SQLAlchemy()
jwt = JWTManager()

key = os.getenv('FERNET_KEY', '1234567890QWERTYUIOPASDFGHJKLZXC').encode('ascii')
fernet_key = base64.urlsafe_b64encode(key)
f = Fernet(fernet_key)