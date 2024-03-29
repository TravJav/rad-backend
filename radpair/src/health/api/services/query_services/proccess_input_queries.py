from openai import OpenAI
from datetime import datetime
import logging

from radpair.src.health.api.services.query_services.session.session_manager import DatabaseConnection
from radpair.src.health.api.services.helpers.project_util import ProjectUtilHelper

class ProcessInputQueries:

    def __init__(self, request_session=DatabaseConnection()):
        self.request_session = request_session
        _util_helper = ProjectUtilHelper()
        OPEN_API_KEY = _util_helper.get_runtime_env_variable('OPENAI_API_KEY')
        self.client = OpenAI()

    def fetch_openapi_response(self, question: str) -> dict:
        """
        method that calls the openapi and structures are response object

        Args:
            question (str): 
        Returns:
            dict: response
        """
         # TODO implement a chat history so context is given to the model 
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        logging.error(response)
        response = self.get_completion_text(response)
        if response:
            
            return{"chatgpt_response": response,
                         "timestamp": datetime.utcnow(), 'query': question}

    def get_completion_text(self, response):
        if response and response.choices:
            # Get the first choice from the response
            choice = response.choices[0]
            if choice.message and choice.message.content:
                return choice.message.content
        return None
