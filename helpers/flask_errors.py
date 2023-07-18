from typing import Dict, Tuple

FLASK_ERROR_TYPE = Tuple[Dict[str, str,], int]

class FlaskErrors:

    @classmethod
    def request_not_json_error(cls) -> FLASK_ERROR_TYPE:
        return {'error': "request does not return a json"}, 400

    @classmethod
    def missing_or_invalid_field(cls, field: str) -> FLASK_ERROR_TYPE:
        return {'error': f"missing or invalid '{field}' field"}, 400

    @classmethod
    def not_implemented_yet(cls) -> FLASK_ERROR_TYPE:
        return {'error': "not implemented yet"}, 501

    @classmethod
    def invalid_date(cls) -> FLASK_ERROR_TYPE:
        return {'error': "invalid date"}, 400
