import pickle
import google.auth
import google.auth.transport.requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
import os
    
def authenticate():
    """Authenticates and returns the Google Drive API service."""
    # Define the path to the credentials JSON file
    credentials_path = 'credentials.json'
    # Define the path to the token pickle file
    token_path = 'token.pickle'
    credentials = None

    # Load or create credentials
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            credentials = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, ['https://www.googleapis.com/auth/drive'])
            credentials = flow.run_local_server(port=0,open_browser=False)
        
        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(credentials, token)

    # Build and return the Google Drive API service
    return build('drive', 'v3', credentials=credentials)