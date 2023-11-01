from .base_controller import BaseController
from managers import DocusignWebhookManager
from fastapi_cloudauth.cognito import Cognito
from fastapi import status, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from utilities.types.fields import DocusignWebhookEventEnum
from datetime import datetime
from typing import Dict, Any
import logging
from config.env import DOCUSIGN_API_VERSION


class PostItem(BaseModel):
    event: DocusignWebhookEventEnum
    api_version: str = Field(alias="apiVersion", examples=['v2.1'])
    uri: str = Field(examples=["/restapi/v2.1/accounts/6f7fcdd0-bc7f-484b-8a15-ed3af04c16ff/envelopes/29e66716-238b-459e-a29d-5371be2bef80"])
    retry_count: int = Field(alias="retryCount", examples=[0])
    configuration_id: int = Field(alias="configurationId", examples=[10352224])
    generated_date_time: datetime = Field(alias="generatedDateTime", examples=["2023-11-01T03:20:28.1366172Z"])
    data: Dict[str, Any]


class DocusignWebhookController(BaseController):

    def __init__(self, auth: Cognito):  # type: ignore[no-any-unimported]
        super().__init__(auth)
        self.router.add_api_route("/docusign/webhook", self.post, methods=["POST"], response_model=None)

    def post(self, item: PostItem) -> Response:
        mgr = DocusignWebhookManager()

        # TODO Include Docusign HMAC Signature and OAUTH

        if item.api_version != DOCUSIGN_API_VERSION:
            logging.warn(f"Webhook API Version doesn't match. Current: {item.api_version}, Expected: {DOCUSIGN_API_VERSION}")

        try:
            mgr.handle_webhook_event(item.event, item.retry_count, item.generated_date_time, item.data)
        except NotImplementedError:
            return JSONResponse(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                content=None
                )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=None
        )
