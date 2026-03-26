# YouTube Shorts Automation

AI-powered YouTube Shorts auto-creation and upload system.

## Features

- **Gemini AI Script Generation**: Auto-generates engaging Korean scripts
- **Edge-TTS Narration**: Natural Korean voice synthesis
- **MoviePy Video Creation**: Automated 9:16 vertical video production
- **YouTube Auto Upload**: Uploads directly via YouTube Data API v3
- **Scheduled Execution**: Runs twice daily (08:00, 20:00)

## Project Structure

```
youtube-shorts-automation/
├── config.py                  # Environment & path configuration
├── main.py                    # Main pipeline orchestrator
├── scheduler.py               # Twice-daily auto scheduler
├── setup.sh                   # EC2 one-click setup script
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variable template
├── .gitignore                 # Git ignore rules
├── generator/
│   ├── __init__.py
│   └── script_generator.py    # Gemini API script generation
├── video_maker/
│   ├── __init__.py
│   ├── tts_engine.py          # Edge-TTS audio generation
│   └── video_creator.py       # MoviePy video composition
├── uploader/
│   ├── __init__.py
│   └── youtube_uploader.py    # YouTube Data API v3 upload
├── deploy/
│   └── youtube-shorts.service # Systemd service file
└── assets/
    ├── fonts/                 # Korean fonts (NanumSquareB.ttf)
    └── backgrounds/           # Background images (optional)
```

## Prerequisites

- Python 3.10+
- FFmpeg
- Google Cloud Project with YouTube Data API v3 enabled
- Gemini API Key (from Google AI Studio)
- OAuth 2.0 client credentials (client_secrets.json)

## Quick Start (Local)

```bash
# 1. Clone repository
git clone https://github.com/Adam-1228/youtube-shorts-automation.git
cd youtube-shorts-automation

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
cp .env.example .env
nano .env  # Add your GEMINI_API_KEY

# 5. Add client_secrets.json to project root

# 6. Install Korean font
sudo apt-get install fonts-nanum
cp /usr/share/fonts/truetype/nanum/NanumGothicBold.ttf assets/fonts/NanumSquareB.ttf

# 7. First run (OAuth authentication)
python3 main.py
```

## EC2 Deployment

```bash
# 1. SSH into your EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# 2. Run setup script
git clone https://github.com/Adam-1228/youtube-shorts-automation.git
cd youtube-shorts-automation
chmod +x setup.sh
./setup.sh

# 3. Configure environment
cp .env.example .env
nano .env

# 4. Add credentials
# Upload client_secrets.json via SCP:
# scp -i your-key.pem client_secrets.json ubuntu@your-ec2-ip:~/youtube-shorts-automation/

# 5. First run (generate token.pickle)
# NOTE: EC2 has no browser, use console auth:
source venv/bin/activate
python3 main.py

# 6. Setup as systemd service (auto-restart)
sudo cp deploy/youtube-shorts.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable youtube-shorts
sudo systemctl start youtube-shorts

# Check status
sudo systemctl status youtube-shorts
sudo journalctl -u youtube-shorts -f
```

## Crontab Alternative

```bash
crontab -e

# Add these lines:
0 8 * * * cd /home/ubuntu/youtube-shorts-automation && /home/ubuntu/youtube-shorts-automation/venv/bin/python main.py >> /home/ubuntu/youtube-shorts-automation/logs/cron.log 2>&1
0 20 * * * cd /home/ubuntu/youtube-shorts-automation && /home/ubuntu/youtube-shorts-automation/venv/bin/python main.py >> /home/ubuntu/youtube-shorts-automation/logs/cron.log 2>&1
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| GEMINI_API_KEY | Google Gemini API key | (required) |
| VIDEO_WIDTH | Video width in pixels | 1080 |
| VIDEO_HEIGHT | Video height in pixels | 1920 |
| VIDEO_FPS | Frames per second | 24 |
| VIDEO_DURATION | Max duration in seconds | 30 |
| SCHEDULE_TIME_1 | First daily run time | 08:00 |
| SCHEDULE_TIME_2 | Second daily run time | 20:00 |
| TTS_VOICE | Edge-TTS voice model | ko-KR-SunHiNeural |

## Pipeline Flow

```
[Gemini AI] → Script JSON
     ↓
[Edge-TTS] → Scene Audio Files
     ↓
[MoviePy] → Composed MP4 Video
     ↓
[YouTube API] → Auto Upload to Channel
```

## Important Notes

- **Never commit** `client_secrets.json`, `token.pickle`, or `.env` to Git
- First OAuth run requires browser access (local PC recommended)
- After first auth, `token.pickle` handles auto-refresh
- YouTube API has a daily quota limit (10,000 units/day)
- Each upload costs ~1,600 units, so ~6 uploads/day max

## License

MIT
