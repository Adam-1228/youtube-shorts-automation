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
