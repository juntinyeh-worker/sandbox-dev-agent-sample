from flask import Blueprint, request, jsonify
from app import db
from app.models.member import Member

members_bp = Blueprint("members", __name__)


@members_bp.get("/")
def list_members():
    members = Member.query.all()
    return jsonify([m.to_dict() for m in members])


@members_bp.post("/")
def create_member():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("name"):
        return jsonify({"error": "email and name required"}), 400
    if Member.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "email already exists"}), 409
    member = Member(email=data["email"], name=data["name"], tier=data.get("tier", "basic"))
    db.session.add(member)
    db.session.commit()
    return jsonify(member.to_dict()), 201


@members_bp.get("/<int:member_id>")
def get_member(member_id):
    member = db.get_or_404(Member, member_id)
    return jsonify(member.to_dict())


@members_bp.put("/<int:member_id>")
def update_member(member_id):
    member = db.get_or_404(Member, member_id)
    data = request.get_json()
    for field in ("name", "email", "tier", "active"):
        if field in data:
            setattr(member, field, data[field])
    db.session.commit()
    return jsonify(member.to_dict())


@members_bp.delete("/<int:member_id>")
def delete_member(member_id):
    member = db.get_or_404(Member, member_id)
    db.session.delete(member)
    db.session.commit()
    return "", 204
