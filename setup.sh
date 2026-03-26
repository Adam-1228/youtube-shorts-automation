#!/bin/bash
# ===========================================
# YouTube Shorts Automation - EC2 Setup Script
# ===========================================

set -e

echo "=========================================="
echo " YouTube Shorts Automation - EC2 Setup"
echo "=========================================="

# Update system
echo "[1/6] Updating system packages..."
sudo apt-get update -y
sudo apt-get upgrade -y

# Install Python 3.10+ and pip
echo "[2/6] Installing Python and dependencies..."
sudo apt-get install -y python3 python3-pip python3-venv
sudo apt-get install -y ffmpeg
sudo apt-get install -y fonts-nanum

# Clone repository (if not already cloned)
echo "[3/6] Setting up project..."
PROJECT_DIR="$HOME/youtube-shorts-automation"
if [ ! -d "$PROJECT_DIR" ]; then
    git clone https://github.com/Adam-1228/youtube-shorts-automation.git "$PROJECT_DIR"
fi
cd "$PROJECT_DIR"

# Create virtual environment
echo "[4/6] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python packages
echo "[5/6] Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "[6/6] Creating directories..."
mkdir -p outputs
mkdir -p assets/fonts
mkdir -p assets/backgrounds

# Copy system Nanum font to assets
NANUM_FONT="/usr/share/fonts/truetype/nanum/NanumSquareB.ttf"
if [ -f "$NANUM_FONT" ]; then
    cp "$NANUM_FONT" assets/fonts/
    echo "  Font copied: NanumSquareB.ttf"
else
    NANUM_GOTHIC="/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf"
    if [ -f "$NANUM_GOTHIC" ]; then
        cp "$NANUM_GOTHIC" assets/fonts/NanumSquareB.ttf
        echo "  Font copied: NanumGothicBold.ttf -> NanumSquareB.ttf"
    else
        echo "  [WARN] Nanum font not found. Please install manually."
        echo "  Run: sudo apt-get install fonts-nanum-extra"
    fi
fi

echo ""
echo "=========================================="
echo " Setup Complete!"
echo "=========================================="
echo ""
echo " Next steps:"
echo "  1. Create .env file:  cp .env.example .env"
echo "  2. Edit .env:         nano .env"
echo "  3. Add client_secrets.json to project root"
echo "  4. First run (for OAuth):  python3 main.py"
echo "  5. Setup crontab:     crontab -e"
echo ""
echo " Crontab entries (add these lines):"
echo "  0 8 * * * cd $PROJECT_DIR && $PROJECT_DIR/venv/bin/python main.py >> logs/cron.log 2>&1"
echo "  0 20 * * * cd $PROJECT_DIR && $PROJECT_DIR/venv/bin/python main.py >> logs/cron.log 2>&1"
echo ""
echo " Or run scheduler: python3 scheduler.py"
echo "=========================================="
