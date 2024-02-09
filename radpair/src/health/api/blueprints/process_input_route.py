import logging
from flask import Blueprint, jsonify, request
from radpair.src.health.api.services.handlers.process_input_handler import ProcessInputHandler


process_input_bp = Blueprint("process_input", __name__)

@process_input_bp.route('/process-command', methods=['POST'])
def process_query_command() -> jsonify:
    """
    called when chatGPT is queried when asking a question

    Returns:
        jsonify: contains the chatgpt response and orignal user query
    """
    try:
        data = request.get_json()
        query: str = data.get('query')
        logging.info(query)
        response = ProcessInputHandler().process_question(query)
        return response
    except (KeyError, ValueError) as e:
        logging.exception("Issue parsing response object: {} ".format(e))
        return jsonify(
            {
                "success": False,
                "message": "Unable to get loading information," " please try again later",
            }
        )
