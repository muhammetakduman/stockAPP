from flask import Blueprint, jsonify, request
from .models import Product
from . import db

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
