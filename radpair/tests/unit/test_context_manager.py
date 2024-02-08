import unittest
from os import environ
from unittest import mock
from unittest.mock import MagicMock, patch
from uuid import UUID
from faker import Faker
import pytest

from radpair.src.health.api.services.context_manager import (ContextManager)

fake = Faker()
hash = "e8583f9f-c31f-4835-a517-d7df168f35e1"


def mockenv(**envvars):
    return mock.patch.dict(environ, envvars)


class TestContextManager(unittest.TestCase):
    def setUp(self):
        self.context_manager = ContextManager()
        self.caller_id = hash

        # caller id can only bge from util, should not be able to call the CM directly
    @mockenv(RUNTIME_ENVIRONMENT="AC")
    def test_fetch_env_variable_value(self):
        """
        fails because we cannot call context manager directly as expected
        """
        with pytest.raises(KeyError):
            with ContextManager() as context_manager:
                fetched_env_value: str = context_manager.fetch_environment_variable(
                    "RUNTIME_ENVIRONMENT"
                )
                self.assertTrue(fetched_env_value, "AC")

    def test_run_illegal_os_caller(self):
        # should not be able to call context manager directly only util helper can
        with pytest.raises(KeyError):
            with ContextManager() as context_manager:
                context_manager.run_os_command("system")("echo hello world")

    def test_register(self):
        # Define test data
        os_environ = {"RUNTIME_ENVIRONMENT": "UNITTEST"}

        # Create a mock object for the os module
        mock_os = MagicMock()
        mock_os.getenv.side_effect = os_environ.get
        mock_os.environ = os_environ
        with patch(
            "radpair.src.health.api.services.context_manager.os", mock_os
        ):
            # Call the register method with the test data
            self.context_manager.register()

            # Check that the environment variable was set correctly
            self.assertTrue(isinstance(mock_os.environ["ENV_HASH"], str))

    def test_run_os_command(self):
        # Define test data
        cmd = ("system", "echo hello world")
        expected_output = b"hello world\n"
        # Create a mock object for the subprocess module
        mock_subprocess = MagicMock()
        mock_subprocess.run.return_value.stdout = expected_output
        with patch(
            "radpair.src.health.api.services.context_manager.subprocess",
            mock_subprocess,
        ):
            # Call the run_os_command method with the test data
            output = self.context_manager.run_os_command(cmd)
            # Check that the output is correct
            self.assertEqual(output.stdout, expected_output)

    def test_generate_unique_uuid(self):
        # Call the generate_unique_uuid method
        output = self.context_manager.generate_unique_uuid()

        # Check that the output is a string
        self.assertIsInstance(output, str)

        # Check that the output is a valid UUID
        try:
            UUID(output)
        except ValueError:
            self.fail("Output is not a valid UUID")
