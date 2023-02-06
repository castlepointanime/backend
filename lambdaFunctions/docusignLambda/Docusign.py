import mimetypes
import json

class Docusign:
    def __init__(self, events: dict):
        self._body = json.loads(events.get("body"))
        self._data = self._body["data"] if self._body else None
        self._envelope_summary = self._data["envelopeSummary"] if self._data else None
        self._envelope_documents = self._envelope_summary["envelopeDocuments"][0] if self._envelope_summary else None
        self._sender = self._envelope_summary["sender"]
        
        self.is_envelope_completed : bool = self._body["event"] == "envelope-completed" if self._body else False
        self.contract_name : str = self._envelope_summary["emailSubject"]
        self.contract_description : str = self._envelope_summary["emailBlurb"]
        self.document_id : int = int(self._envelope_documents["documentId"])
        self.sender_name : str = self._sender["userName"]
        self.sender_user_id : str = self._sender["userId"]
        self.sender_account_id : str = self._sender["accountId"]
        self.sender_email : str = self._sender["email"]
        self.document_name : str = self._envelope_documents["name"]
        self.file_name : str = f"{self.sender_email}_{self.document_name}"
        self.data : str = self._envelope_documents["PDFBytes"]
        self.is_base64 : bool = events["isBase64Encoded"] if events["isBase64Encoded"] else False
        self.file_mimetype = mimetypes.MimeTypes().guess_type(self.document_name)[0]