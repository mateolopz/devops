# tests/test_blacklists.py

from fastapi.testclient import TestClient
from fastapi_jwt_auth import AuthJWT

from src.db.schemas.blacklist import BlacklistEmail
from src.logic.blacklist import blacklist_email
from src.main import app  # Assuming your FastAPI app is created in src/main.py
import pytest
from unittest.mock import MagicMock
from src.db.db import Base, engine, SessionLocal

client = TestClient(app)


@pytest.fixture
def mock_jwt_required(mocker):
    mocker.patch.object(AuthJWT, "jwt_required", return_value=None)


@pytest.fixture
def fake_db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


def populate_db(session):
    emails = [
        BlacklistEmail(email="test1@example.com", app_uuid="00000", blocked_reason="Justification"),
        BlacklistEmail(email="test2@example.com", app_uuid="00001", blocked_reason="Justification"),
    ]
    for email in emails:
        blacklist_email(session,email)

def test_post_blacklist(mock_jwt_required, mocker, fake_db):
    '''
    Tests the successful addition of an email to the blacklist
    :param mock_jwt_required: Mocks the JWT
    :param mocker:
    :param fake_db:
    :return:
    '''
    mocker.patch("src.logic.blacklist.blacklist_email", return_value=True)

    # Populates the db with data points
    populate_db(fake_db)

    # Creates new tests and asserts success
    response = client.post("/blacklists",
                           json={
                               "email": "test@example.com",
                               "app_uuid": "00001",
                               "blocked_reason": "Justification"
                           })

    # Assertions
    assert response.status_code == 201
    assert response.json() == "Email agregado a la lista negra"


def test_get_blacklist_by_email(mock_jwt_required, mocker):
    mocker.patch("src.logic.blacklist.get_blacklist", return_value=MagicMock(blocked_reason="Spam"))
    response = client.get("/blacklists/test@example.com")
    assert response.status_code == 200
    assert response.json() == {"found": True, "blocked_reason": "Spam"}
