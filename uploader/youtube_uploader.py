"""
youtube-shorts-automation - 유튜브 업로더 모듈 (uploader/youtube_uploader.py)
------------------------------------------------------------------------------
YouTube Data API v3를 사용하여 생성된 쇼츠 영상을 유튜브 채널에 자동 업로드하는 모듈.

주요 기능:
    - get_authenticated_service(): OAuth 2.0 인증으로 YouTube API 클라이언트 생성
      * 인증 토큰은 token.pickle 파일에 캐시하여 재사용
      * EC2 헤드리스 서버 환경에서도 동작하도록 설계
    - upload_video(): 생성된 MP4 파일을 유튜브 채널에 업로드
      * 제목, 설명, 태그, 카테고리, 개인정보 보호 설정 포함
      * Shorts는 #Shorts 해시태그 포함 및 세로 영상으로 자동 인식

인증:
    OAuth 2.0 (client_secrets.json 파일 필요)
    최초 실행 시 브라우저 인증 후 token.pickle로 저장.
"""
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
                        creds = flow.run_local_server(
                                            port=8080,
                                            open_browser=False,
                                            authorization_prompt_message='Please visit this URL to authorize: {url}',
                                            success_message='Authorization complete. You may close this window.'
                        )

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
