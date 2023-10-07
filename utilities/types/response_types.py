from typing import Dict, Any, Union, List


# https://github.com/python/typing/issues/182
JSONType = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]

JSONDict = Dict[str, Any]
