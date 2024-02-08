import os
import csv
from radpair.src.health.api.services.query_services.proccess_input_queries import ProcessInputQueries

class ProcessInputHandler:

    def process_question(self, question: str) -> dict:
        _process_input_queries = ProcessInputQueries()
        detected_macros = self.detect_potential_macros_in_query(question)
        if detected_macros:
            for macro_phrase, macro_text in detected_macros:
                question = question.replace(macro_phrase, macro_text)
        
        chatgpt_response = _process_input_queries.fetch_openapi(question)
        return chatgpt_response
    
    def detect_potential_macros_in_query(self, question: str) -> list:
        macro_dict = self.load_project_macro_resources()
        detected_macros = []
        for macro_phrase, macro_text in macro_dict.items():
            if macro_phrase in question:
                detected_macros.append((macro_phrase, macro_text))
        return detected_macros

    def load_project_macro_resources(self) -> dict:
        macro_dict = {}
        MACRO_FILE_NAME = 'macro_dict.csv'
        current_dir = os.path.dirname(__file__)
        csv_path = os.path.join(current_dir, MACRO_FILE_NAME)
        with open(csv_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                macro_dict[row['Macro Phrase']] = row['Macro Text']
        return macro_dict
