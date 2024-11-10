from . import db

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)  # Ürün toplam fiyatı
    unit_price = db.Column(db.Float, nullable=False)  # Adet fiyatı
    stock = db.Column(db.Integer, nullable=False)
