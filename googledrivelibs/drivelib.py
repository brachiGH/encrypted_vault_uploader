import os
import google.auth
import google.auth.transport.requests
from googleapiclient.http import MediaFileUpload
# Define the MIME type of the file
import mimetypes


def upload_file(service, file_path, mime_type, folder_id):
    """Uploads a file to Google Drive in the specified folder."""

    try:
        file_size = get_file_size(file_path)
        print(f"uploading \"{file_path}\" size is: {file_size:.2f} MB")
    except FileNotFoundError as e:
        print(str(e))

    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, mimetype=mime_type)
    service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()


def get_file_size(file_path):
    """Gets the size of a file in megabytes (MB)."""
    if os.path.isfile(file_path):
        size_bytes = os.path.getsize(file_path)
        size_mb = size_bytes / (1024 * 1024)
        return size_mb
    else:
        raise FileNotFoundError("File not found.")


def get_mime_type(file_path):
    """Gets the MIME type of a file."""
    return mimetypes.guess_type(file_path)[0]

def upload_file_to_drive(file_path, folder_id, drive_service):
    mime_type = get_mime_type(file_path)

    try:
        # Upload the file to the specified folder
        upload_file(drive_service, file_path, mime_type, folder_id)

        print(f'"{file_path}" uploaded successfully!')
    except Exception as e:
        print('An error occurred:', str(e))



def list_files_in_directory(drive_service, directory_id):
    """Lists all non-trashed files in the specified directory in Google Drive."""
    try:
        results = drive_service.files().list(q=f"'{directory_id}' in parents", fields="files(id, name)").execute()
        files = results.get('files', [])
        return files
    except Exception as e:
        print('An error occurred:', str(e))
        return []


def download_file(drive_service, file_id, destination_path):
    try:
        request = drive_service.files().get_media(fileId=file_id)
        with open(destination_path, 'wb') as file:
            downloader = request.execute()
            file.write(downloader)
        print(f"File downloaded successfully to: {destination_path}")
    except Exception as e:
        print(f"Error downloading file: {e}")