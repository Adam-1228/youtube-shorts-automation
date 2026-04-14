"""
youtube-shorts-automation - TTS 엔진 모듈 (video_maker/tts_engine.py)
-----------------------------------------------------------------------
Microsoft Edge TTS를 사용하여 한국어 나레이션 음성 파일을 생성하는 모듈.

주요 기능:
    - generate_scene_audio(): 씬별 텍스트를 MP3 음성 파일로 변환
    - 비동기(asyncio) 기반으로 여러 씬을 병렬 처리 가능

사용 엔진:
    Microsoft Edge TTS (edge-tts 라이브러리)
    - 무료 사용 가능 (Azure TTS 기반)
    - 한국어 음성: config.py의 TTS_VOICE 설정으로 변경 가능
    - 기본 음성: ko-KR-SunHiNeural (여성 음성)

출력:
    OUTPUTS_DIR에 MP3 파일 생성
    파일명 형식: scene_{씬번호}.mp3
"""
import asyncio
import edge_tts
import os
from config import TTS_VOICE, OUTPUTS_DIR


async def _generate_tts(text, output_path):
    """Generate TTS audio using edge-tts."""
    communicate = edge_tts.Communicate(text, TTS_VOICE)
    await communicate.save(output_path)


def generate_tts(text, filename="narration.mp3"):
    """Sync wrapper: Generate TTS audio file."""
    output_path = os.path.join(OUTPUTS_DIR, filename)
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    asyncio.run(_generate_tts(text, output_path))
    return output_path


def generate_scene_audio(scenes):
    """Generate narration audio for each scene."""
    audio_files = []
    for i, scene in enumerate(scenes):
        narration = scene.get('narration', scene.get('text', ''))
        filename = f"scene_{i:02d}.mp3"
        path = generate_tts(narration, filename)
        audio_files.append(path)
        print(f"  [TTS] Scene {i} audio saved: {path}")
    return audio_files


if __name__ == '__main__':
    test_path = generate_tts("Hello, this is a TTS test.", "test_tts.mp3")
    print(f"Test TTS saved: {test_path}")
