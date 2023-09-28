import logging
from fastapi import APIRouter
from time import strftime
from fastapi_cloudauth.cognito import Cognito
from fastapi import Request


class BaseController:

    def __init__(self, auth: Cognito):  # type: ignore[no-any-unimported]
        self.router = APIRouter()
        self.auth = auth

    @classmethod
    def log_debug(cls, msg: str, request: Request) -> None:
        timestamp = strftime('[%Y-%b-%d %H:%M]')
        assert request.client, "Missing header data in request. No client information."
        logging.debug('%s %s %s %s %s %s', timestamp, request.client.host, request.method, request.scope['type'], request.url, msg)
