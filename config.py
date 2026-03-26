import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

# Video Settings
VIDEO_WIDTH = int(os.getenv('VIDEO_WIDTH', 1080))
VIDEO_HEIGHT = int(os.getenv('VIDEO_HEIGHT', 1920))
VIDEO_FPS = int(os.getenv('VIDEO_FPS', 24))
VIDEO_DURATION = int(os.getenv('VIDEO_DURATION', 30))

# Schedule
SCHEDULE_TIME_1 = os.getenv('SCHEDULE_TIME_1', '08:00')
SCHEDULE_TIME_2 = os.getenv('SCHEDULE_TIME_2', '20:00')

# TTS
TTS_LANGUAGE = os.getenv('TTS_LANGUAGE', 'ko')
TTS_VOICE = os.getenv('TTS_VOICE', 'ko-KR-SunHiNeural')

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
OUTPUTS_DIR = os.path.join(BASE_DIR, 'outputs')
FONT_PATH = os.path.join(ASSETS_DIR, 'fonts', 'NanumSquareB.ttf')

# YouTube
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, 'client_secrets.json')
TOKEN_FILE = os.path.join(BASE_DIR, 'token.pickle')
