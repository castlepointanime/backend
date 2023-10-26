from controllers import ContractController, MeController, HealthController
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from time import strftime
import logging
from config.env import COGNITO_REGION, COGNITO_USERPOOL_ID, COGNITO_APP_CLIENT_ID
import traceback
import uvicorn
from fastapi_cloudauth.cognito import Cognito
from starlette.middleware.base import _StreamingResponse
from typing import Awaitable, Callable

app = FastAPI()
auth = Cognito(
    region=COGNITO_REGION,
    userPoolId=COGNITO_USERPOOL_ID,
    client_id=COGNITO_APP_CLIENT_ID
)

logging.getLogger().setLevel(logging.INFO)

app.include_router(ContractController(auth).router)
app.include_router(MeController(auth).router)
app.include_router(HealthController(auth).router)


@app.middleware("http")
async def after_request(request: Request, call_next: Callable[..., Awaitable[_StreamingResponse]]) -> Response:
    response: Response = await call_next(request)
    timestamp = strftime('[%Y-%b-%d %H:%M]')  # TODO this is defined in multiple spots. Make robust
    assert request.client, "Missing header data in request. No client information."
    logging.info('%s %s %s %s %s %s', timestamp, request.client.host, request.method, request.scope['type'], request.url, response.status_code)
    return response


@app.exception_handler(Exception)
def exceptions(request: Request, e: Exception) -> JSONResponse:
    tb = traceback.format_exc()
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    assert request.client, "Missing header data in request. No client information."
    logging.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s', timestamp, request.client.host, request.method, request.scope['type'], request.url, tb)
    logging.error(e)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=None
    )


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    uvicorn.run(app, host="0.0.0.0", port=3001)
