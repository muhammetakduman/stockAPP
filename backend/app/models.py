from . import db
from datetime import datetime ,timezone

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)  
    unit_price = db.Column(db.Float, nullable=False)  
    stock = db.Column(db.Integer, nullable=False)

class Musteri(db.Model):
    #test edildi
    __tablename__ = 'musteriler'
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(100), nullable=False)
    adres = db.Column(db.String(200), nullable=True)
    telefon = db.Column(db.String(20), nullable=True)

from datetime import datetime, timezone

class Teklif(db.Model):
    __tablename__ = 'teklifler'
    id = db.Column(db.Integer, primary_key=True)
    musteri_id = db.Column(db.Integer, nullable=True)  
    urun_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)  
    urun = db.relationship('Product', backref='teklifler')
    urun_adi = db.Column(db.String(100), nullable=True)  
    birim_fiyat = db.Column(db.Float, nullable=False)  
    miktar = db.Column(db.Integer, nullable=False) 
    toplam_fiyat = db.Column(db.Float, nullable=False)
    tarih = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  
    aciklama = db.Column(db.String(200), nullable=True)
    durum = db.Column(db.String(20), default='beklemede')  


class Servis(db.Model):
    __tablename__ = 'servisler'
    id = db.Column(db.Integer, primary_key=True)
    musteri_id = db.Column(db.Integer, db.ForeignKey('musteriler.id'), nullable=False)
    musteri = db.relationship('Musteri', backref='servisler')
    yapilan_is = db.Column(db.String(200), nullable=False)
    ucret = db.Column(db.Float, nullable=False)
    tarih = db.Column(db.DateTime, default=datetime.utcnow)
    durum = db.Column(db.String(20), default='beklemede')  

class AlacakBorc(db.Model):
    __tablename__ = 'alacak_borc'
    id = db.Column(db.Integer, primary_key=True)
    musteri_id = db.Column(db.Integer, db.ForeignKey('musteriler.id'), nullable=True)
    musteri = db.relationship('Musteri', backref='alacak_borc')
    tur = db.Column(db.String(20), nullable=False) 
    miktar = db.Column(db.Float, nullable=False)
    durum = db.Column(db.String(20), default='beklemede')  
    tarih = db.Column(db.DateTime, default=datetime.utcnow)

class GelirGider(db.Model):
    __tablename__ = 'gelir_gider'
    id = db.Column(db.Integer, primary_key=True)
    tur = db.Column(db.String(20), nullable=False)  
    miktar = db.Column(db.Float, nullable=False)
    tarih = db.Column(db.DateTime, default=datetime.utcnow)
    aciklama = db.Column(db.String(200), nullable=True)