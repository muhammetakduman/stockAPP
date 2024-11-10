from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS  # CORS kütüphanesini ekliyoruz
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # CORS ayarları
    CORS(app, resources={r"/api/*": {"origins": "*"}})  # Gerekirse origins kısmında izin verilen kaynakları belirtebilirsiniz

    from .routes import main
    app.register_blueprint(main)

    return app
