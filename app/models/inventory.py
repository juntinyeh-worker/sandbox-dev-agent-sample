from datetime import datetime
from app import db


class InventoryItem(db.Model):
    __tablename__ = "inventory"

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id, "sku": self.sku, "name": self.name,
            "quantity": self.quantity, "price": str(self.price),
            "category": self.category,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
