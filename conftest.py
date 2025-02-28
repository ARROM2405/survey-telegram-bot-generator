from itertools import count

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import Session

from database import Base, get_db
from main import app
from models import TelegramBot, User


@pytest.fixture(scope="session")
def counter():
    return count(1)


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )

    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_db_override():
        return session

    app.dependency_overrides[get_db] = get_db_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def user(counter):
    return User(email=f"test_{counter}@test.com", password="<PASSWORD>")


@pytest.fixture
def bot(user, counter):
    return TelegramBot(
        active=True,
        telegram_token=f"some_telegram_token_{counter}",
        internal_token=f"some_internal_token_{counter}",
        user=user,
        greeting_message=f"some_greetings_message_{counter}",
        edited_message_response=f"some_edited_message_response_{counter}",
        confirmed_input_message=f"some_confirmed_message_{counter}",
        unconfirmed_input_message=f"some_unconfirmed_message_{counter}",
    )
