from extensions import db
from utils.transactions import convert_jenis_to_str
import datetime

class Transaction(db.Model):
    __tablename__ = "transaksi"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="transactions")
    tanggal = db.Column(db.Date, nullable=True, server_default=db.func.now())
    jumlah = db.Column(db.Numeric, nullable=False)
    jenis = db.Column(db.Integer, nullable=False)

    def to_json(self):
        jenis_str = convert_jenis_to_str(self.jenis)
        return {
            'id' : self.id,
            'user' : self.user.to_json_without_transaction(),
            'tanggal' : self.tanggal,
            'jumlah' : self.jumlah,
            'jenis' : jenis_str,
        }
    