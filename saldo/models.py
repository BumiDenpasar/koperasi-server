from extensions import db

class Saldo(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="saldo")