import logging
from fastapi import APIRouter
from time import strftime
from fastapi_cloudauth.cognito import Cognito
from fastapi import Request

class BaseController:  # type: ignore[no-any-unimported]

    def __init__(self, auth: Cognito):
        self.router = APIRouter()
        self.auth = auth

    @classmethod
    def log_debug(cls, msg: str, request: Request) -> None:
        timestamp = strftime('[%Y-%b-%d %H:%M]')
        logging.debug('%s %s %s %s %s %s', timestamp, request.client.host, request.method, request.scope['type'], request.url, msg)
