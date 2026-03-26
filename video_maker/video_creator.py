import os
from moviepy.editor import (
    TextClip, CompositeVideoClip, AudioFileClip,
    ColorClip, concatenate_videoclips, ImageClip
)
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from config import VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS, OUTPUTS_DIR, ASSETS_DIR, FONT_PATH


def create_text_image(text, width=900, font_size=60, text_color='white',
                      bg_color=None, padding=20):
    """Create text image using PIL (Korean font support)."""
    try:
        font = ImageFont.truetype(FONT_PATH, font_size)
    except (OSError, IOError):
        font = ImageFont.load_default()
        print("[WARN] Custom font not found, using default font")

    dummy_img = Image.new('RGBA', (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    img_w = width
    img_h = text_h + padding * 2

    if bg_color:
        img = Image.new('RGBA', (img_w, img_h), bg_color)
    else:
        img = Image.new('RGBA', (img_w, img_h), (0, 0, 0, 0))

    draw = ImageDraw.Draw(img)
    x = (img_w - text_w) // 2
    y = padding
    draw.text((x, y), text, font=font, fill=text_color)

    return np.array(img)


def create_scene_clip(text, duration, bg_color=(25, 25, 35)):
    """Create a single scene video clip."""
    background = ColorClip(
        size=(VIDEO_WIDTH, VIDEO_HEIGHT),
        color=bg_color,
        duration=duration
    )

    text_img = create_text_image(
        text,
        width=VIDEO_WIDTH - 100,
        font_size=65,
        text_color='white',
        bg_color=(0, 0, 0, 180),
        padding=30
    )

    text_clip = (
        ImageClip(text_img)
        .set_duration(duration)
        .set_position('center')
    )

    return CompositeVideoClip([background, text_clip])


def create_video(script_data, audio_files, output_filename="shorts_video.mp4"):
    """Create the full Shorts video."""
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    scenes = script_data['scenes']
    clips = []

    bg_colors = [
        (25, 25, 35), (35, 20, 45), (20, 35, 50),
        (40, 25, 25), (25, 40, 30), (30, 30, 45),
        (45, 30, 20), (20, 40, 40)
    ]

    for i, scene in enumerate(scenes):
        text = scene['text']
        duration = scene.get('duration', 5)
        bg_color = bg_colors[i % len(bg_colors)]

        print(f"  [VIDEO] Creating scene {i}: {text[:20]}...")

        scene_clip = create_scene_clip(text, duration, bg_color)

        if i < len(audio_files) and os.path.exists(audio_files[i]):
            audio = AudioFileClip(audio_files[i])
            actual_duration = max(duration, audio.duration + 0.5)
            scene_clip = scene_clip.set_duration(actual_duration)
            scene_clip = scene_clip.set_audio(audio)

        clips.append(scene_clip)

    final_video = concatenate_videoclips(clips, method="compose")

    output_path = os.path.join(OUTPUTS_DIR, output_filename)
    final_video.write_videofile(
        output_path,
        fps=VIDEO_FPS,
        codec='libx264',
        audio_codec='aac',
        preset='medium',
        threads=4
    )

    final_video.close()
    for clip in clips:
        clip.close()

    print(f"  [VIDEO] Final video saved: {output_path}")
    return output_path


if __name__ == '__main__':
    test_script = {
        "scenes": [
            {"text": "AI Automation Test", "duration": 3},
            {"text": "Video created successfully!", "duration": 3}
        ]
    }
    output = create_video(test_script, [], "test_video.mp4")
    print(f"Test video: {output}")
