import mimetypes

class Docusign:
    def __init__(self, events: dict):
        self._body : dict = events.get("body")
        self._data : dict = self._body.get("data") if self._body else None
        self._envelope_summary : dict = self._data.get("envelopeSummary") if self._data else None
        self._envelope_documents : list = self._envelope_summary.get("envelopeDocuments")[0] if self._envelope_summary else None
        self._sender : dict = self._envelope_summary.get("sender")
        
        self.is_envelope_completed : bool = self._body.get("event") == "envelope-completed" if self._body else False
        self.contract_name : str = self._envelope_summary.get("emailSubject")
        self.contract_description : str = self._envelope_summary.get("emailBlurb")
        self.document_id : int = int(self._envelope_documents.get("documentId"))
        self.sender_name : str = self._sender.get("userName")
        self.sender_user_id : str = self._sender.get("userId")
        self.sender_account_id : str = self._sender.get("accountId")
        self.sender_email : str = self._sender.get("email")
        self.document_name : str = self._envelope_documents.get("name")
        self.file_name : str = f"{self.sender_email}_{self.document_name}"
        self.data : str = self._envelope_documents.get("PDFBytes")
        self.is_base64 : bool = events.get("isBase64Encoded") if events["isBase64Encoded"] else False
        self.file_mimetype = mimetypes.MimeTypes().guess_type(self.document_name)[0]