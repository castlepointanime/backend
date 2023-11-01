from pydantic import Field
from config import Config
from enum import Enum

config = Config()
phone_number_max = config.get_contract_limit("phone_number_max")
phone_number_min = config.get_contract_limit("phone_number_min")


def phone_number(alias: str) -> int:
    # This is technically a pydantic.fields.FieldInfo, but we will trick mypy so it's callers can be defined correctly
    result: int = Field(alias=alias, ge=phone_number_max, le=phone_number_min, examples=['11234567890'])
    return result


class VendorTypeEnum(Enum):
    artist = 'artist'
    dealer = 'dealer'


class DocusignWebhookEventEnum(Enum):
    envelope_created = 'envelope-created'
    envelope_sent = 'envelope-sent'
    envelope_delivered = 'envelope-delivered'
    envelope_completed = 'envelope-completed'
    envelope_purge = 'envelope-purge'
    envelope_resent = 'envelope-resent'
    envelope_corrected = 'envelope-corrected'
    envelope_discard = 'envelope-discard'
    envelope_voided = 'envelope-voided'
    envelope_deleted = 'envelope-deleted'
    envelope_declined = 'envelope-declined'

    recipient_sent = 'recipient-sent'
    recipient_auto_responded = 'recipient-auto-responded'
    recipient_delivered = 'recipient-delivered'
    recipient_completed = 'recipient-completed'
    recipient_declined = 'recipient-declined'
    recipient_authentication_failure = 'recipient-authentication-failure'
    recipient_resent = 'recipient-resent'
    recipient_reassign = 'recipient-reassign'
    recipient_finish_later = 'recipient-finish-later'
    recipient_delegate = 'recipient-delegate'
