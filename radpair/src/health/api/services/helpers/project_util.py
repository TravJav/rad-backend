# #!/usr/bin/env python
# -
# 

import logging
from datetime import datetime, timezone
import requests
import boto3

from radpair.src.health.api.services.context_manager import ( ContextManager)


class ProjectUtilHelper(object):

    def get_upload_timestamp(self) -> datetime.now:
        """
        helper function for commmon requested functionality throughout the app
        Returns:
            datetime.datetime: returns a datetime object of the current
            datetime
        """
        return str(datetime.now(timezone.utc).replace(microsecond=0))

    def get_runtime_env_variable(self, env_key: str) -> str:
        """
        Acts as a helper class to obtain the environment variable key values
        to avoid having OS imports everywhere in the app TODO: conext manager
        for certain imports
        Args:
            env_key (str): expected env varibale key
        Raises:
            RuntimeError: runtime error if the enviroment variable can't be found
        Returns:
            str: env_key value
        """
        with ContextManager() as context_manager:
            return context_manager.fetch_environment_variable(("environ", env_key))
