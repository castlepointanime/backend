from Docusign import Docusign
from GoogleDrive import GoogleDrive
import logging
import json

def lambda_handler(event, context):
    try:
        document : Docusign = Docusign(event)
        if not document.is_envelope_completed:
            result = {
                "status": 400,
                "body": "Envelope is not completed."
            }
            logging.error("Failed to execute docusign function: docusign is not complete.")
            return result
        api : GoogleDrive = GoogleDrive()
        file_id = api.resumable_upload_to_drive(document.data, document.file_name, document.file_mimetype, is_base64=document.is_base64)
        
        result = {
            "status": 200,
            "google_drive_file_id": file_id,
            "contract_name": document.contract_name,
            "contract_description": document.contract_description,
            "docusign_document_id": document.document_id,
            "sender_name": document.sender_name,
            "sender_user_id": document.sender_user_id,
            "sender_account_id": document.sender_account_id,
            "sender_email": document.sender_email,
            "document_name": document.document_name,
            "file_name": document.file_name
        }
        logging.debug(f"Successfully uploaded to google drive: {json.dumps(result)}")
        return result
    except Exception as e:
        logging.error(f"Internal Server Error: '{str(e)}'")
        return {
            "status": 500,
            "body": str(e)
        }