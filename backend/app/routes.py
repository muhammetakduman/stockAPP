from flask import Blueprint, jsonify, request
from .models import Product , Teklif
from . import db
import logging
logging.basicConfig(level=logging.DEBUG)

main = Blueprint('main', __name__)

@main.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    output = [{'id': product.id, 'name': product.name, 'description': product.description, 'price': product.price, 'unit_price': product.unit_price, 'stock': product.stock} for product in products]
    return jsonify({'products': output})

@main.route('/api/products', methods=['POST'])
def add_product():
    data = request.get_json()

    # Verilerin doğru türlere dönüştürülmesi
    try:
        unit_price = float(data['unit_price'])  # Birim fiyatı float olarak alıyoruz
        stock = int(data['stock'])  # Stok miktarını integer olarak alıyoruz
    except ValueError:
        return jsonify({"error": "Birim fiyat veya stok miktarı geçerli bir sayı değil."}), 400

    # Ürün adını küçük harfe çevirerek aynı isimde bir ürün olup olmadığını kontrol ediyoruz
    normalized_name = data['name'].lower()
    product = Product.query.filter(Product.name == normalized_name).first()

    if product:
        # Aynı isimde bir ürün varsa, ortalama birim fiyatını ve stok miktarını güncelle
        total_stock = product.stock + stock
        weighted_average_price = ((product.unit_price * product.stock) + (unit_price * stock)) / total_stock

        product.stock = total_stock
        product.unit_price = weighted_average_price
        product.price = product.unit_price * product.stock  # Yeni toplam fiyatı güncelle
    else:
        # Yeni bir ürün oluştur
        product = Product(
            name=normalized_name,
            description=data['description'],
            unit_price=unit_price,
            price=unit_price * stock,  # Toplam fiyat, adet fiyatı x stok olarak hesaplanıyor
            stock=stock
        )
        db.session.add(product)

    # Veritabanına değişiklikleri kaydet
    try:
        db.session.commit()
        return jsonify({"message": "Product added successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@main.route('/api/products/<int:id>', methods=['PUT'])
def update_product_stock(id):
    data = request.get_json()
    new_stock = data.get('stock')

    try:
        product = Product.query.get(id)
        if not product:
            return jsonify({"error": "Ürün bulunamadı"}), 404

        # Stok miktarını güncelleme
        product.stock = new_stock
        product.price = product.unit_price * new_stock
        db.session.commit()
        return jsonify({"message": "Stok başarıyla güncellendi"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Ürün silme endpoint'i (DELETE)
@main.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    try:
        product = Product.query.get(id)
        if not product:
            return jsonify({"error": "Ürün bulunamadı"}), 404

        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Ürün başarıyla silindi"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@main.route('/api/teklif/stoktan', methods=['POST'])
def teklif_stoktan_ekle():
    data = request.get_json()
    urun_id = data.get('urun_id')
    miktar = int(data.get('miktar', 0))

    # Stoktaki ürünü kontrol et
    stok_urun = Product.query.get(urun_id)
    if not stok_urun:
        return jsonify({"error": "Stokta böyle bir ürün bulunamadı"}), 404

    # Yeterli stok kontrolü
    if stok_urun.stock < miktar:
        return jsonify({"error": "Yeterli stok yok"}), 400

    # Stok güncelleme ve toplam fiyat hesaplama
    stok_urun.stock -= miktar
    toplam_fiyat = stok_urun.unit_price * miktar

    # Teklif oluşturma
    teklif = Teklif(
        urun_id=urun_id,
        birim_fiyat=stok_urun.unit_price,
        miktar=miktar,
        toplam_fiyat=toplam_fiyat,
        aciklama=data.get('aciklama')
    )
    db.session.add(teklif)
    db.session.commit()
    return jsonify({"message": "Stoktan teklif başarıyla eklendi!"}), 201

@main.route('/api/teklif/manuel', methods=['POST'])
def teklif_manuel_ekle():
    data = request.get_json()
    urun_adi = data.get('urun_adi')
    birim_fiyat = float(data.get('birim_fiyat'))
    miktar = int(data.get('miktar', 0))
    toplam_fiyat = birim_fiyat * miktar

    # Teklif oluşturma
    teklif = Teklif(
        urun_adi=urun_adi,
        birim_fiyat=birim_fiyat,
        miktar=miktar,
        toplam_fiyat=toplam_fiyat,
        aciklama=data.get('aciklama')
    )
    db.session.add(teklif)
    db.session.commit()
    return jsonify({"message": "Manuel teklif başarıyla eklendi!"}), 201

@main.route('/api/teklifler', methods=['GET'])
def get_teklifler():
    teklifler = Teklif.query.all()
    output = [
        {
            "id": teklif.id,
            "musteri_id": teklif.musteri_id,
            "urun_id": teklif.urun_id,
            "urun_adi": teklif.urun_adi,
            "birim_fiyat": teklif.birim_fiyat,
            "miktar": teklif.miktar,
            "toplam_fiyat": teklif.toplam_fiyat,
            "tarih": teklif.tarih,
            "aciklama": teklif.aciklama,
            "durum": teklif.durum
        }
        for teklif in teklifler
    ]
    return jsonify({"teklifler": output})
