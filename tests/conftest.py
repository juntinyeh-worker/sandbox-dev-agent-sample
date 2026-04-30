import os
import pytest

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app import create_app, db as _db


@pytest.fixture()
def app():
    app = create_app()
    app.config["TESTING"] = True
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def db(app):
    return _db
