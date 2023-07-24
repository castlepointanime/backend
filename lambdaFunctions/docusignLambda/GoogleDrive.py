from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2.service_account import Credentials
import io
import os
import base64


class GoogleDrive():
    def __init__(self):
        self._SCOPES = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.file'
        ]
        self.credentials = None
        self.check_credentials()  # TODO doesn't work
        self.service = build('drive', 'v3', credentials=self.credentials)

    def check_credentials(self, credentials_filepath='service_account.json'):
        if not os.path.exists(credentials_filepath):
            raise Exception("service_account.json not found")
        self.credentials = Credentials.from_service_account_file(credentials_filepath)

    def resumable_upload_to_drive(self, file_data: str, file_name: str, file_mimetype: str, is_base64: bool = False):
        file_data = base64.b64decode(file_data)
        file_stream = io.BytesIO(file_data)
        media = MediaIoBaseUpload(file_stream, mimetype=file_mimetype, resumable=True)
        file_metadata = {
            'name': file_name,
            'parents': ['17TvqjY62dW_hc0_K-b6C8-mbk930pbzC']  # TODO: replace this with an actual official CPAC shared folder
        }
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return file.get("id")
