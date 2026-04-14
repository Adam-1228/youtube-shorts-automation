"""
YouTube Shorts Automation System
youtube-shorts-automation - 유튜브 쇼츠 자동 생성 및 업로드 시스템 (main.py)

주요 흐름:
    1. Gemini API로 쇼츠 스크립트(제목, 내용, 해시태그) 자동 생성
    2. edge-tts(Microsoft TTS)로 한국어 음성 파일 생성
    3. MoviePy로 자막 + 배경영상 + 음성을 합성하여 MP4 생성
    4. YouTube Data API v3로 생성된 쇼츠를 자동 업로드

의존성:
    - google-generativeai: Gemini API 클라이언트
    - moviepy==1.0.3: 영상 편집 (v2.x 비호환으로 버전 고정)
    - edge-tts: Microsoft Azure TTS (무료)
    - google-api-python-client: YouTube API 클라이언트
- Gemini API for script generation
- MoviePy + edge-tts for video creation
- YouTube Data API v3 for auto upload
"""
import os
import sys
import json
from datetime import datetime

from config import OUTPUTS_DIR
from generator.script_generator import generate_script
from video_maker.tts_engine import generate_scene_audio
from video_maker.video_creator import create_video
from uploader.youtube_uploader import get_authenticated_service, upload_video


def cleanup_temp_files():
    """Clean up temporary scene audio files."""
    if not os.path.exists(OUTPUTS_DIR):
        return
    for f in os.listdir(OUTPUTS_DIR):
        if f.startswith('scene_') and f.endswith('.mp3'):
            os.remove(os.path.join(OUTPUTS_DIR, f))


def run_pipeline():
    """Execute the full automation pipeline."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    print(f"\n{'='*50}")
    print(f"  YouTube Shorts Auto Creator")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")

    # Step 1: Generate script
    print("[1/4] Generating script with Gemini...")
    script = generate_script()
    if not script:
        print("[FAIL] Script generation failed. Aborting.")
        return False

    print(f"  Title: {script['title']}")
    print(f"  Scenes: {len(script['scenes'])}")

    # Save script
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    script_path = os.path.join(OUTPUTS_DIR, f'script_{timestamp}.json')
    with open(script_path, 'w', encoding='utf-8') as f:
        json.dump(script, f, ensure_ascii=False, indent=2)

    # Step 2: Generate TTS audio
    print("\n[2/4] Generating TTS audio...")
    audio_files = generate_scene_audio(script['scenes'])

    # Step 3: Create video
    print("\n[3/4] Creating video...")
    video_filename = f"shorts_{timestamp}.mp4"
    video_path = create_video(script, audio_files, video_filename)

    if not os.path.exists(video_path):
        print("[FAIL] Video creation failed. Aborting.")
        return False

    # Step 4: Upload to YouTube
    print("\n[4/4] Uploading to YouTube...")
    try:
        youtube = get_authenticated_service()
        video_id = upload_video(
            youtube,
            video_path,
            script['title'],
            script['description'],
            tags=script.get('tags', [])
        )
        print(f"\n[SUCCESS] Video uploaded: https://youtube.com/shorts/{video_id}")
    except Exception as e:
        print(f"[ERROR] Upload failed: {e}")
        print("  Video saved locally. You can upload manually.")

    # Cleanup
    cleanup_temp_files()

    print(f"\n{'='*50}")
    print("  Pipeline completed!")
    print(f"{'='*50}\n")
    return True


if __name__ == '__main__':
    run_pipeline()
