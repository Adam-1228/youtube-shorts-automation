import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from config import SCOPES, CLIENT_SECRETS_FILE, TOKEN_FILE


def get_authenticated_service():
    """Get authenticated YouTube API service."""
    creds = None

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES
            )
            try:
                creds = flow.run_local_server(port=0)
            except Exception:
                creds = flow.run_console()

        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return build('youtube', 'v3', credentials=creds)


def upload_video(youtube, file_path, title, description, tags=None,
                 category_id='28', privacy='public'):
    """Upload video to YouTube."""
    if tags is None:
        tags = ['AI', 'Shorts', 'Tech']

    body = {
        'snippet': {
            'title': title,
            'description': description + '\n\n#Shorts',
            'tags': tags,
            'categoryId': category_id
        },
        'status': {
            'privacyStatus': privacy,
            'selfDeclaredMadeForKids': False
        }
    }

    media = MediaFileUpload(
        file_path,
        chunksize=256 * 1024,
        resumable=True,
        mimetype='video/mp4'
    )

    request = youtube.videos().insert(
        part='snippet,status',
        body=body,
        media_body=media
    )

    print(f"[UPLOAD] Uploading: {title}")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"  Progress: {int(status.progress() * 100)}%")

    video_id = response.get('id')
    print(f"[UPLOAD] Complete! Video ID: {video_id}")
    print(f"  URL: https://youtube.com/shorts/{video_id}")
    return video_id


if __name__ == '__main__':
    yt = get_authenticated_service()
    print("YouTube authentication successful!")
