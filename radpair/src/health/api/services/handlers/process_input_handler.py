import os
import logging
import csv
from radpair.src.health.api.services.query_services.proccess_input_queries import ProcessInputQueries

class ProcessInputHandler:

    def process_question(self, question: str) -> dict:
        """
        entry point into handlder where the user query should be processed
        we use su

        Args:
            question (str): string query from user

        Returns:
            dict: chatGPT response
        """
        original_question: str = question
        try:
            _process_input_queries: object = ProcessInputQueries()
            detected_macros: list = self._detect_potential_macros_in_query(question)
            
            if detected_macros:
                for macro_phrase, macro_text in detected_macros:
                    question: str = question.replace(macro_phrase, macro_text)
            
            chatgpt_response: dict = _process_input_queries.fetch_openapi_response(question)  
            chatgpt_response['query'] = original_question 
            return chatgpt_response
        except Exception as e:
            logging.exception(f"An error occurred while processing the question: {e}")
            return {"error": "An error occurred while processing the question. Please try again."}

    
    def _detect_potential_macros_in_query(self, question: str) -> list:
        """
        submethod to help with loading the macros from the resource file
        the method searches for the phrase in the macros and adds it to the list 
        if found and returns

        Args:
            question (str): original query from user

        Returns:
            list: detected macro list
        """
        try:
            macro_dict = self._load_project_macro_resources()
            detected_macros: list = []
            for macro_phrase, macro_text in macro_dict.items():
                if macro_phrase in question:
                    detected_macros.append((macro_phrase, macro_text))
            return detected_macros
        except Exception as e:
            logging.exception(f"An error occurred while detecting macros: {e}")
            return []
            
    def _load_project_macro_resources(self) -> dict:
        """
            submethod to assist wiht loading the macro resources

        Returns:
            dict: macro dictionary
        """
        try:
            macro_dict = {}
            MACRO_FILE_NAME: str = 'macro_dict.csv'
            current_dir: str = os.path.dirname(__file__)
            csv_path: str = os.path.join(current_dir, MACRO_FILE_NAME)
            with open(csv_path, 'r', encoding='utf-8-sig') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if len(row) >= 2:
                        macro_dict[row[0]] = row[1]
            return macro_dict
        except FileNotFoundError:
            logging.exception("Macro file not found.")
            return {}
        except Exception as e:
            logging.exception(f"An error occurred while loading macro resources: {e}")
            return {}
