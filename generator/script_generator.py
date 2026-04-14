"""
youtube-shorts-automation - 스크립트 생성 모듈 (generator/script_generator.py)
--------------------------------------------------------------------------------
Gemini API를 사용하여 유튜브 쇼츠용 한국어 스크립트를 자동으로 생성하는 모듈.

주요 기능:
    - generate_script(): 주어진 주제로 쇼츠 스크립트 생성
      * 제목, 나레이션 텍스트, 해시태그 포함
      * 30-60초 분량의 간결한 내용으로 최적화
    - 응답 형식: JSON (title, narration, hashtags)

사용 모델:
    Gemini 2.5 Flash (gemini-2.5-flash)
    - 빠른 생성 속도
    - 한국어 콘텐츠 최적화
"""
import google.generativeai as genai
import json
import re
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')


def generate_script():
    """Gemini API to generate YouTube Shorts script."""
    prompt = """
    You are a YouTube Shorts content creator for AI/Tech topics in Korean.
    Generate a script in the following JSON format ONLY (no other text):
    {
        "title": "Catchy Korean title under 50 chars",
        "description": "Video description under 100 chars with hashtags",
        "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
        "scenes": [
            {
                "text": "On-screen text (under 15 Korean chars)",
                "duration": 5,
                "narration": "TTS narration text in Korean"
            }
        ]
    }

    Rules:
    - 6-8 scenes, total duration under 50 seconds
    - First scene must be a strong hook
    - Topic: Latest AI tech, programming tips, or tech trends
    - Write in Korean
    - Do NOT include #Shorts in title
    """

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            script_data = json.loads(json_match.group())
        else:
            script_data = json.loads(text)

        required = ['title', 'description', 'tags', 'scenes']
        for field in required:
            if field not in script_data:
                raise ValueError(f"Missing field: {field}")

        return script_data

    except Exception as e:
        print(f"[ERROR] Script generation failed: {e}")
        return None


if __name__ == '__main__':
    script = generate_script()
    if script:
        print(json.dumps(script, ensure_ascii=False, indent=2))
