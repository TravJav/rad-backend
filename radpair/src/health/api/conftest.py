from dataclasses import asdict, dataclass
from types import SimpleNamespace
import flask_jwt_extended
from typing import List
import pytest

from pytest_mock import MockerFixture
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from health.api.domain.delcarative import Base

TEST_DATABASE = "postgresql://postgres:password@health-pg:5432/healthpg"


@pytest.fixture(scope="session")
def engine():
    return create_engine(TEST_DATABASE)


@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture()
def dbsession(*args):
    connection = create_engine(TEST_DATABASE).connect()
    transaction = connection.begin()
    session = scoped_session(sessionmaker(bind=connection, future=True))
    transaction = session()
    yield transaction
    transaction.commit()
    transaction.close()
    transaction.rollback()
    connection.close()


@dataclass
class MockIdentity:
    is_admin: bool
    permissions: List[str]
    user_id: int

    def has_permissions(self, *permissions: str, quantifier=all) -> bool:
        if self.is_admin:
            return True
        if not permissions:
            return False
        return quantifier([r in self.permissions for r in permissions])


class MockAuthIdentity:
    DEFAULT = MockIdentity(is_admin=False, permissions=[], user_id=1)

    @classmethod
    def identity(self):
        return SimpleNamespace(**asdict(self.DEFAULT))

    @classmethod
    def factory(self, **kwargs):
        def identity():
            return MockIdentity(**{**asdict(self.DEFAULT), **kwargs})

        return identity


def authz_identity() -> SimpleNamespace:
    return MockAuthIdentity.identity()


@pytest.fixture(scope="function")
def admin_identity(mocker: MockerFixture):
    mock = mocker.patch.object(
        MockAuthIdentity,
        "identity",
        MockAuthIdentity.factory(**asdict(MockIdentity(is_admin=True, permissions=[], user_id=1))),
    )
    return mock()


@pytest.fixture(scope="function")
def client_identity(mocker: MockerFixture):
    mock = mocker.patch.object(
        MockAuthIdentity,
        "identity",
        MockAuthIdentity.factory(
            **asdict(MockIdentity(is_admin=False, permissions=["sm/general"], user_id=1))
        ),
    )
    return mock()

@pytest.fixture(autouse=True)
def mock_no_jwt_required(mocker):
    def mock_jwt_required(*_):
        return True

    mock = mocker.patch(
        f"{flask_jwt_extended.__name__}.jwt_required",
        mock_jwt_required,
    )
    return mock
