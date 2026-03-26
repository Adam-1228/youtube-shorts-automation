import google.generativeai as genai
import json
import re
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')


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
