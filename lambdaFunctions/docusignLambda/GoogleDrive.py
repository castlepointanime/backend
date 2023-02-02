from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import io, base64, os

class GoogleDrive():
    def __init__(self, credentials_filepath='credentials.json'):
        if not os.path.exists(credentials_filepath):
            raise Exception("credentials.json not found")
        self._SCOPES = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.file'
        ]
        self.credentials = Credentials.from_authorized_user_file(credentials_filepath, scopes=self._SCOPES) #TODO doesn't work
        self.service = build('drive', 'v3', credentials=self.credentials)
        
        
    def resumable_upload_to_drive(self, file_data: str, file_name: str, file_mimetype: str, is_base64 : bool = False):
        if is_base64:
            file_data = base64.b64decode(file_data).decode('utf-8')
        file_stream = io.BytesIO(file_data)
        media = MediaFileUpload(file_stream, mimetype=file_mimetype, resumable=True)
        file_metadata = {
            'name': file_name
        }
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return file.get("id")