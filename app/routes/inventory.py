from flask import Blueprint, request, jsonify
from app import db
from app.models.inventory import InventoryItem

inventory_bp = Blueprint("inventory", __name__)


@inventory_bp.get("/")
def list_items():
    category = request.args.get("category")
    q = InventoryItem.query
    if category:
        q = q.filter_by(category=category)
    return jsonify([i.to_dict() for i in q.all()])


@inventory_bp.post("/")
def create_item():
    data = request.get_json()
    if not data or not data.get("sku") or not data.get("name") or data.get("price") is None:
        return jsonify({"error": "sku, name, and price required"}), 400
    if InventoryItem.query.filter_by(sku=data["sku"]).first():
        return jsonify({"error": "sku already exists"}), 409
    item = InventoryItem(
        sku=data["sku"], name=data["name"], price=data["price"],
        quantity=data.get("quantity", 0), category=data.get("category"),
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


@inventory_bp.get("/<int:item_id>")
def get_item(item_id):
    return jsonify(db.get_or_404(InventoryItem, item_id).to_dict())


@inventory_bp.put("/<int:item_id>")
def update_item(item_id):
    item = db.get_or_404(InventoryItem, item_id)
    data = request.get_json()
    for field in ("name", "sku", "quantity", "price", "category"):
        if field in data:
            setattr(item, field, data[field])
    db.session.commit()
    return jsonify(item.to_dict())


@inventory_bp.delete("/<int:item_id>")
def delete_item(item_id):
    item = db.get_or_404(InventoryItem, item_id)
    db.session.delete(item)
    db.session.commit()
    return "", 204
