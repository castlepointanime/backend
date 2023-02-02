from Docusign import Docusign
from GoogleDrive import GoogleDrive

def lambda_handler(event, context):
    try:
        document : Docusign = Docusign(event)
        if not document.is_envelope_completed:
            return {
                "status": 400,
                "body": "Envelope is not completed."
            }
        api : GoogleDrive = GoogleDrive()
        api.resumable_upload_to_drive(document.data, document.file_name, document.file_mimetype, is_base64=document.is_base64)
    except Exception as e:
        print(str(e))
        return {
            "status": 500,
            "body": str(e)
        }