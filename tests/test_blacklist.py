# tests/test_blacklists.py

from fastapi.testclient import TestClient
from fastapi_jwt_auth import AuthJWT

from src.db.schemas.blacklist import BlacklistEmail
from src.logic.blacklist import blacklist_email
from src.main import app  # Assuming your FastAPI app is created in src/main.py
import pytest
from unittest.mock import MagicMock
from src.db.db import Base, engine, SessionLocal
from faker import Faker

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


@pytest.fixture
def populate_db(fake_db):
    fake = Faker()

    # Generating random BlacklistEmail objects
    num_emails = 25

    random_emails = [
        BlacklistEmail(
            email=fake.email(),
            app_uuid=str(i + 5),
            blocked_reason="Justification"
        ) for i in range(num_emails)
    ]

    known_emails = [
        BlacklistEmail(email="test0@example.com", app_uuid="00000", blocked_reason="Justification"),
        BlacklistEmail(email="test1@example.com", app_uuid="00001", blocked_reason="Justification"),
        BlacklistEmail(email="test2@example.com", app_uuid="00002", blocked_reason="Justification"),
        BlacklistEmail(email="test3@example.com", app_uuid="00003", blocked_reason="Justification"),
        BlacklistEmail(email="test4@example.com", app_uuid="00004", blocked_reason="Justification"),
        BlacklistEmail(email="test5@example.com", app_uuid="00005", blocked_reason="Justification"),
    ]

    emails = random_emails + known_emails

    for email in emails:
        blacklist_email(fake_db, email)


def test_post_blacklist(mock_jwt_required, mocker, fake_db, populate_db):
    """
    Tests the successful addition of a correctly formatted email to the blacklist
    :param mock_jwt_required: Mocks the JWT
    :param mocker:
    :param fake_db:
    :return:
    """
    mocker.patch("src.logic.blacklist.blacklist_email", return_value=True)

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


def test_post_blacklist_bad_email_format(mock_jwt_required, mocker, populate_db):
    """
    Tests that blacklist post request is rejected if the email format is not met
    :param mock_jwt_required:
    :param mocker:
    :param populate_db:
    :return:
    """
    mocker.patch("src.logic.blacklist.blacklist_email", return_value=True)

    # Creates new tests and asserts results
    response = client.post("/blacklists",
                           json={
                               "email": "badtestexamplecom",
                               "app_uuid": "00009",
                               "blocked_reason": "Justification"
                           })
    # Assertions
    assert response.status_code == 400
    assert response.json() == "El email dado no es valido"

def test_post_blacklist_existing_uuid(mock_jwt_required, mocker, populate_db):
    """

    :param mock_jwt_required:
    :param mocker:
    :param populate_db:
    :return:
    """
    mocker.patch("src.logic.blacklist.blacklist_email", return_value=True)

    # Creates new tests and asserts success
    pre_existing_uuid = "00001"
    response = client.post("/blacklists",
                           json={
                               "email": "goodmail@hotmail.com",
                               "app_uuid": pre_existing_uuid,
                               "blocked_reason": "Justification"
                           })
    # Assertions
    assert response.status_code == 400
    assert response.json() == "El email dado no es valido"

def test_get_blacklist_by_email(mock_jwt_required, mocker, populate_db):
    mocker.patch("src.logic.blacklist.get_blacklist", return_value=MagicMock(blocked_reason="Spam"))

    # Consult an existing email in the db
    response = client.get("/blacklists/test1@example.com")
    assert response.status_code == 200
    assert response.json() == {"found": True, "blocked_reason": "Spam"}
