from extensions import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    alamat = db.Column(db.String, nullable=False)
    transactions = db.relationship("Transaction", back_populates="user")

    
    def to_json(self):
        return {
            'id' : self.id,
            'username' : self.username,
            'email' : self.email,
            'alamat' : self.alamat,
            'transactions' : [t.to_json() for t in self.transactions]
        }
    
    def to_json_without_transaction(self):
        return {
            'id' : self.id,
            'username' : self.username,
            'email' : self.email,
            'alamat' : self.alamat,
        }
    