import os
import shutil

import allure
import pytest
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import get_db
from app.main import app
from app.models import Base

fake = Faker("en_US")

LOG_FILE = "logs/test_run.log"
DB_FILE = "test.db"


@pytest.fixture(scope="session")
def engine():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope="function")
def db_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    connection = engine.connect()
    transaction = connection.begin()
    session.bind = connection

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    def override_db():
        yield db_session

    app.dependency_overrides[get_db] = override_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def get_user_data():
    """Генерирует случайные данные для пользователя"""

    def _generate_user():
        username = f"{fake.user_name()}{fake.random_int(1000, 9999)}"
        email = fake.unique.email()
        age = fake.random_int(11, 60)
        return {"username": username, "email": email, "age": age}

    return _generate_user


@pytest.fixture(scope="function")
def get_order_data():
    """Генерирует случайные данные для заказа."""

    def _generate_order():
        product_name = fake.word().capitalize()
        quantity = fake.random_int(1, 5)
        return {"product_name": product_name, "quantity": quantity}

    return _generate_order


@pytest.fixture(autouse=True)
def reset_db(engine):
    """Полностью пересоздаёт БД перед каждым тестом (гарантия чистоты)."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук, который прикладывает логи и дамп базы в Allure при падении теста."""
    outcome = yield
    result = outcome.get_result()

    # Только если тест упал
    if result.when == "call" and result.failed:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                allure.attach(f.read(), name="Logs", attachment_type=allure.attachment_type.TEXT)

        # Прикладываем файл базы (если он используется)
        if os.path.exists(DB_FILE):
            snapshot = f"artifacts/{item.name}_db_snapshot.db"
            os.makedirs("artifacts", exist_ok=True)
            shutil.copy(DB_FILE, snapshot)
            allure.attach.file(snapshot, name="DB Snapshot", attachment_type=allure.attachment_type.BINARY)
