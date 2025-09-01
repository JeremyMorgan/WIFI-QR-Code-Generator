#!/bin/bash

# WiFi QR Generator Deployment Script for Ubuntu EC2
# Run this script on your EC2 instance to set up the application

set -e

echo "Starting deployment of WiFi QR Generator..."

# Update system packages
sudo apt update
sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv nginx git

# Create application directory
sudo mkdir -p /opt/wifi-qr-generator
sudo chown $USER:$USER /opt/wifi-qr-generator

# Clone or update repository
if [ -d "/opt/wifi-qr-generator/.git" ]; then
    echo "Repository exists, pulling latest changes..."
    cd /opt/wifi-qr-generator
    git pull origin main
else
    echo "Cloning repository..."
    git clone https://github.com/YOUR_USERNAME/WIFI-QR-Code-Generator.git /opt/wifi-qr-generator
    cd /opt/wifi-qr-generator
fi

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Copy nginx configuration
sudo cp nginx.conf /etc/nginx/sites-available/wifi-qr-generator
sudo ln -sf /etc/nginx/sites-available/wifi-qr-generator /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
sudo nginx -t

# Create systemd service file
sudo tee /etc/systemd/system/wifi-qr-generator.service > /dev/null << EOF
[Unit]
Description=WiFi QR Code Generator Flask App
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/opt/wifi-qr-generator
Environment=PATH=/opt/wifi-qr-generator/venv/bin
ExecStart=/opt/wifi-qr-generator/venv/bin/python app.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and start services
sudo systemctl daemon-reload
sudo systemctl enable wifi-qr-generator
sudo systemctl start wifi-qr-generator
sudo systemctl enable nginx
sudo systemctl start nginx

# Check service status
echo "Checking service status..."
sudo systemctl status wifi-qr-generator --no-pager
sudo systemctl status nginx --no-pager

echo "Deployment completed successfully!"
echo "Your application should be accessible at http://YOUR_EC2_PUBLIC_IP"
echo ""
echo "To check logs, run:"
echo "sudo journalctl -u wifi-qr-generator -f"