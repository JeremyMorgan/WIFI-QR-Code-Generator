#!/bin/bash

# WiFi QR Generator Deployment Script
# Run this script on your EC2 instance to set up the application

set -e

APP_DIR="/opt/wifi-qr-generator"
APP_USER="ubuntu"
REPO_URL="https://github.com/JeremyMorgan/WIFI-QR-Code-Generator.git"

echo "Starting deployment..."

# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv nginx git

# Create application directory
sudo mkdir -p $APP_DIR
sudo chown $APP_USER:$APP_USER $APP_DIR

# Clone or update repository
if [ -d "$APP_DIR/.git" ]; then
    echo "Repository exists, pulling latest changes..."
    cd $APP_DIR
    git pull origin main
else
    echo "Cloning repository..."
    git clone $REPO_URL $APP_DIR
    cd $APP_DIR
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$APP_DIR/venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# Create production WSGI file
cat > wsgi.py << EOF
from app import app

if __name__ == "__main__":
    app.run()
EOF

echo "Deployment completed successfully!"
echo "Next steps:"
echo "1. Update REPO_URL in this script with your actual GitHub repository URL"
echo "2. Set up the systemd service: sudo cp wifi-qr-generator.service /etc/systemd/system/"
echo "3. Set up nginx: sudo cp nginx.conf /etc/nginx/sites-available/wifi-qr-generator"
echo "4. Enable and start services"