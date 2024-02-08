import json
import unittest
from faker import Faker
from mock import patch

from radpair.src.health.api import app

from radpair.tests.unit.fixtures import (
    mock_jwt_required,
)


class TestAuthRoute(unittest.TestCase):

    @classmethod
    def setUp(cls) -> None:
        cls.faker = Faker()
        cls.app = app.config["TESTING"] = True
        cls.client = app.test_client()
        cls.route = "/status"

    @classmethod
    def tearDownClass(cls):
        cls.faker = None
        cls.client = None
        cls.body_request_sample = None

    def test_get_public_status_check(self, *args):
        response = self.client.get('/status')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] == True
        assert data["message"] == "public api-radpair status check endpoint is operational"
