from app.models.member import Member
from app.models.inventory import InventoryItem


class TestMemberModel:
    def test_create_and_defaults(self, db, app):
        m = Member(email="a@b.com", name="Alice")
        db.session.add(m)
        db.session.commit()
        assert m.id is not None
        assert m.tier == "basic"
        assert m.active is True
        assert m.created_at is not None

    def test_to_dict(self, db, app):
        m = Member(email="a@b.com", name="Alice", tier="vip")
        db.session.add(m)
        db.session.commit()
        d = m.to_dict()
        assert d["email"] == "a@b.com"
        assert d["tier"] == "vip"
        assert "created_at" in d

    def test_unique_email(self, db, app):
        import pytest
        db.session.add(Member(email="dup@b.com", name="A"))
        db.session.commit()
        db.session.add(Member(email="dup@b.com", name="B"))
        with pytest.raises(Exception):
            db.session.commit()


class TestInventoryItemModel:
    def test_create_and_defaults(self, db, app):
        i = InventoryItem(sku="SKU-1", name="Widget", price=9.99)
        db.session.add(i)
        db.session.commit()
        assert i.id is not None
        assert i.quantity == 0
        assert i.created_at is not None

    def test_to_dict(self, db, app):
        i = InventoryItem(sku="SKU-1", name="Widget", price=9.99, category="tools")
        db.session.add(i)
        db.session.commit()
        d = i.to_dict()
        assert d["sku"] == "SKU-1"
        assert d["price"] == "9.99"
        assert d["category"] == "tools"

    def test_unique_sku(self, db, app):
        import pytest
        db.session.add(InventoryItem(sku="DUP", name="A", price=1))
        db.session.commit()
        db.session.add(InventoryItem(sku="DUP", name="B", price=2))
        with pytest.raises(Exception):
            db.session.commit()
