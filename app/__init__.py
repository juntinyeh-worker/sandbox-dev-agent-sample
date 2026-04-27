from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.members import members_bp
    from app.routes.inventory import inventory_bp

    app.register_blueprint(members_bp, url_prefix="/api/members")
    app.register_blueprint(inventory_bp, url_prefix="/api/inventory")

    @app.get("/health")
    def health():
        return {"status": "healthy"}

    return app
