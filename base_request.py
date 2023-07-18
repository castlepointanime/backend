from helpers import Validation, FlaskErrors
from typing import Optional, Dict

class BaseRequest:

    validation = Validation()
    content : Optional[Dict] = None 
    errors = FlaskErrors()
    
    def generate_request_content(self, request) -> bool:
        content = request.get_json()

        # verify that input is a json
        if type(content) != dict:
            return False

        self.content = content
        return True


    