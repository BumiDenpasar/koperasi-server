from extensions import db

class Saldo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="saldo")
    jumlah = db.Column(db.Numeric, nullable='false')

    def to_json(self):
        return {
            'jumlah' : self.jumlah,
        }