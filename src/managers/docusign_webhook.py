from config.env import DOCUSIGN_QUERY_PARAM_KEY
from utilities.types.fields import DocusignWebhookEventEnum
from datetime import datetime
from typing import Dict, Any


class DocusignWebhookManager():

    def is_webhook_key(self, key: str) -> bool:
        return key == DOCUSIGN_QUERY_PARAM_KEY

    def handle_webhook_event(self, event: DocusignWebhookEventEnum, retry_count: int, generated_date_time: datetime, data: Dict[str, Any]) -> None:
        match event:
            case DocusignWebhookEventEnum.envelope_created:
                self._handle_envelope_created(retry_count, generated_date_time, data)
            case DocusignWebhookEventEnum.envelope_sent:
                self._handle_envelope_sent(retry_count, generated_date_time, data)
            case DocusignWebhookEventEnum.envelope_delivered:
                self._handle_envelope_delivered(retry_count, generated_date_time, data)
            case DocusignWebhookEventEnum.envelope_completed:
                self._handle_envelope_completed(retry_count, generated_date_time, data)
            case DocusignWebhookEventEnum.envelope_purge:
                self._handle_envelope_purge(retry_count, generated_date_time, data)
            case DocusignWebhookEventEnum.envelope_resent:
                self._handle_envelope_resent(retry_count, generated_date_time, data)
            case DocusignWebhookEventEnum.envelope_corrected:
                self._handle_envelope_corrected(retry_count, generated_date_time, data)
            case DocusignWebhookEventEnum.envelope_discard:
                self._handle_envelope_discard(retry_count, generated_date_time, data)
            case DocusignWebhookEventEnum.envelope_voided:
                self._handle_envelope_voided(retry_count, generated_date_time, data)
            case DocusignWebhookEventEnum.envelope_deleted:
                self._handle_envelope_deleted(retry_count, generated_date_time, data)
            case DocusignWebhookEventEnum.envelope_declined:
                self._handle_envelope_declined(retry_count, generated_date_time, data)
            case DocusignWebhookEventEnum.recipient_sent:
                self._handle_recipient_sent(retry_count, generated_date_time, data)
            case DocusignWebhookEventEnum.recipient_auto_responded:
                self._handle_recipient_auto_responded(retry_count, generated_date_time, data)
            case DocusignWebhookEventEnum.recipient_delivered:
                self._handle_recipient_delivered(retry_count, generated_date_time, data)
            case DocusignWebhookEventEnum.recipient_completed:
                self._handle_recipient_completed(retry_count, generated_date_time, data)
            case DocusignWebhookEventEnum.recipient_declined:
                self._handle_recipient_declined(retry_count, generated_date_time, data)
            case DocusignWebhookEventEnum.recipient_authentication_failure:
                self._handle_recipient_authentication_failure(retry_count, generated_date_time, data)
            case DocusignWebhookEventEnum.recipient_resent:
                self._handle_recipient_resent(retry_count, generated_date_time, data)
            case DocusignWebhookEventEnum.recipient_reassign:
                self._handle_recipient_reassign(retry_count, generated_date_time, data)
            case DocusignWebhookEventEnum.recipient_finish_later:
                self._handle_recipient_finish_later(retry_count, generated_date_time, data)
            case DocusignWebhookEventEnum.recipient_delegate:
                self._handle_recipient_delegate(retry_count, generated_date_time, data)
            case _ as unknown:
                raise Exception(f"Unknown docusign event '{unknown}'")

    def _handle_envelope_created(self, retry_count: int, generated_date_time: datetime, data: Dict[str, Any]) -> None:
        # TODO Here we have more info about the contract compared to our initial post route, so update contract and users DB
        raise NotImplementedError

    def _handle_envelope_sent(self, retry_count: int, generated_date_time: datetime, data: Dict[str, Any]) -> None:
        # TODO Email is sent to signer/approver. Update contract state (and maybe users db if needed).
        raise NotImplementedError

    def _handle_envelope_delivered(self, retry_count: int, generated_date_time: datetime, data: Dict[str, Any]) -> None:
        # An envelope has been signed from both parties but it's not done yet. We can do nothing here
        return

    def _handle_envelope_completed(self, retry_count: int, generated_date_time: datetime, data: Dict[str, Any]) -> None:
        # TODO update contract state (and maybe users db if needed)
        # TODO send contract PDF to google drive
        raise NotImplementedError

    def _handle_envelope_purge(self, retry_count: int, generated_date_time: datetime, data: Dict[str, Any]) -> None:
        # TODO at this point we need to delete the contracts and any kind of it's history from our DB.
        raise NotImplementedError

    def _handle_envelope_resent(self, retry_count: int, generated_date_time: datetime, data: Dict[str, Any]) -> None:
        # An envelope email is being sent to the signer/approver. We can do nothing here
        return

    def _handle_envelope_corrected(self, retry_count: int, generated_date_time: datetime, data: Dict[str, Any]) -> None:
        # TODO update contract data (and maybe users db if needed)
        raise NotImplementedError

    def _handle_envelope_discard(self, retry_count: int, generated_date_time: datetime, data: Dict[str, Any]) -> None:
        # TODO it is unknown when this event will occur
        raise NotImplementedError

    def _handle_envelope_voided(self, retry_count: int, generated_date_time: datetime, data: Dict[str, Any]) -> None:
        # TODO update contract state (and maybe users db if needed)
        raise NotImplementedError

    def _handle_envelope_deleted(self, retry_count: int, generated_date_time: datetime, data: Dict[str, Any]) -> None:
        # TODO update contract state (and maybe users db if needed). DO NOT DELETE IT. Purge deletes.
        raise NotImplementedError

    def _handle_envelope_declined(self, retry_count: int, generated_date_time: datetime, data: Dict[str, Any]) -> None:
        # TODO update contract state (and maybe users db if needed)
        raise NotImplementedError

    def _handle_recipient_sent(self, retry_count: int, generated_date_time: datetime, data: Dict[str, Any]) -> None:
        # An envelope email is being sent to the signer/approver. We can do nothing here
        return

    def _handle_recipient_auto_responded(self, retry_count: int, generated_date_time: datetime, data: Dict[str, Any]) -> None:
        # TODO it is unknown when this event will occur
        raise NotImplementedError

    def _handle_recipient_delivered(self, retry_count: int, generated_date_time: datetime, data: Dict[str, Any]) -> None:
        # Signer/approver has filled out all fields, but has not confirmed the contract yet. We can do nothing here
        return

    def _handle_recipient_completed(self, retry_count: int, generated_date_time: datetime, data: Dict[str, Any]) -> None:
        # TODO Signer/approver has finished the contract. Update contract DB (and maybe users db if needed)
        raise NotImplementedError

    def _handle_recipient_declined(self, retry_count: int, generated_date_time: datetime, data: Dict[str, Any]) -> None:
        # TODO update contract state (and maybe users db if needed)
        raise NotImplementedError

    def _handle_recipient_authentication_failure(self, retry_count: int, generated_date_time: datetime, data: Dict[str, Any]) -> None:
        # TODO it is unknown when this event will occur
        raise NotImplementedError

    def _handle_recipient_resent(self, retry_count: int, generated_date_time: datetime, data: Dict[str, Any]) -> None:
        # An envelope email is being sent to the signer/approver. We can do nothing here
        return

    def _handle_recipient_reassign(self, retry_count: int, generated_date_time: datetime, data: Dict[str, Any]) -> None:
        # TODO update contract state and users db
        raise NotImplementedError

    def _handle_recipient_finish_later(self, retry_count: int, generated_date_time: datetime, data: Dict[str, Any]) -> None:
        # TODO update contract state (and maybe users db if needed)
        raise NotImplementedError

    def _handle_recipient_delegate(self, retry_count: int, generated_date_time: datetime, data: Dict[str, Any]) -> None:
        # TODO it is unknown when this event will occur
        raise NotImplementedError
