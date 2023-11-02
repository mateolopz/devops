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
from src.logic.blacklist import get_blacklist

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
            blocked_reason="Justification",
            client_ip="255.255.255.0"
        ) for i in range(num_emails)
    ]

    known_emails = [
        BlacklistEmail(email="test0@example.com", app_uuid="5b8f97ec-2888-46e9-b731-31820c4da230", blocked_reason="Justification", client_ip="255.255.255.0"),
        BlacklistEmail(email="test1@example.com", app_uuid="5b8f97ec-2888-46e9-b731-31820c4da230", blocked_reason="Spam", client_ip="255.255.255.0"),
        BlacklistEmail(email="test2@example.com", app_uuid="5b8f97ec-2888-46e9-b731-31820c4da230", blocked_reason="Justification", client_ip="255.255.255.0"),
        BlacklistEmail(email="test3@example.com", app_uuid="5b8f97ec-2888-46e9-b731-31820c4da230", blocked_reason="Justification", client_ip="255.255.255.0"),
        BlacklistEmail(email="test4@example.com", app_uuid="5b8f97ec-2888-46e9-b731-31820c4da230", blocked_reason="Justification", client_ip="255.255.255.0"),
        BlacklistEmail(email="test5@example.com", app_uuid="5b8f97ec-2888-46e9-b731-31820c4da230", blocked_reason="Justification", client_ip="255.255.255.0"),
    ]

    emails = random_emails + known_emails

    for email in emails:
        blacklist_email(fake_db, email)


def test_post_blacklist(mock_jwt_required, mocker, fake_db, populate_db):
    """
    Tests the successful addition of a correctly formatted email to the blacklist
    :param mock_jwt_required: Mocks the JWT
    :param mocker: mocker interface
    :param fake_db: the mocked db with its populated data
    """
    mocker.patch("src.logic.blacklist.blacklist_email", return_value=True)

    # Creates new tests and asserts success
    response = client.post("/blacklists",
                           json={
                               "email": "test@example.com",
                               "app_uuid": "5b8f97ec-2888-46e9-b731-31820c4da230",
                               "blocked_reason": "Justification"
                           })

    # Assertions of response
    assert response.json() == "Email agregado a la lista negra"
    assert response.status_code == 201




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
                               "blocked_reason": "Justification",

                           })

    # Assertions of json response
    assert response.status_code == 400
    assert response.json()['detail'] == "El email dado no es valido"



def test_get_blacklist_unknown_email(mock_jwt_required, mocker, populate_db):
    #mock_blacklist_email = BlacklistEmail(email="unknown@example.com", app_uuid="78ba3fa6-09ca-40a6-baa6-1810d6572b75", blocked_reason="Spam",client_ip="192.168.0.1")
    mocker.patch("src.logic.blacklist.get_blacklist", return_value=None)  # Mock get_blacklist to return None



    # Consult route with undefined email, however it has the correct format
    response = client.get("/blacklists/v.escobar1@uniandes.edu.co")
    assert response.status_code == 404
    assert response.json() == {"found": False}


def test_get_blacklist_unknown_email_bad_format(mock_jwt_required, mocker, populate_db):
    mocker.patch("src.logic.blacklist.get_blacklist", return_value=MagicMock(blocked_reason="Spam"))

    # Consult route with undefined email, however it has the correct format
    response = client.get("/blacklists/badformatemail")
    assert response.status_code == 400
    assert response.json()['detail'] == "El email dado no es valido"

def test_get_blacklist_by_email(mock_jwt_required, mocker, populate_db):
    mock_blacklist_email = BlacklistEmail(email="getit@example.com", app_uuid="28eac92c-5c0e-4bbc-87e6-a25fc4fb7330", blocked_reason="Spam", client_ip="192.168.0.1")
    mocker.patch("src.logic.blacklist.get_blacklist", return_value=mock_blacklist_email)

    # Consult an existing email in the db
    response = client.get("/blacklists/test1@example.com")
    assert response.status_code == 200
    assert response.json() == {"found": True, "blocked_reason": "Spam"}
