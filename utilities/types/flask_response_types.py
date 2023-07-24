from typing import Dict, Any, Union, Tuple
from http import HTTPStatus

JSONData = Union[str, Dict[Any, Any]]
FlaskResponseType = Tuple[JSONData, HTTPStatus]
