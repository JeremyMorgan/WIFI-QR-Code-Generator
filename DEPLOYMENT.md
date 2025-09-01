# Deployment Setup Guide

This guide explains how to set up CI/CD deployment to an Ubuntu EC2 instance using GitHub Actions.

## Prerequisites

1. **EC2 Instance**: Ubuntu 22.04 LTS or later
2. **GitHub Repository**: This repository with appropriate permissions
3. **SSH Access**: Key pair for EC2 instance access

## Initial EC2 Setup

### 1. Connect to your EC2 instance
```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

### 2. Run the deployment script
```bash
# Download and run the deployment script
wget https://raw.githubusercontent.com/YOUR_USERNAME/WIFI-QR-Code-Generator/main/deploy.sh
chmod +x deploy.sh
./deploy.sh
```

### 3. Update the deploy.sh script
Before running, edit the repository URL in `deploy.sh`:
```bash
# Replace YOUR_USERNAME with your actual GitHub username
git clone https://github.com/YOUR_USERNAME/WIFI-QR-Code-Generator.git /opt/wifi-qr-generator
```

### 4. Update nginx configuration
Edit the nginx configuration to use your domain:
```bash
sudo nano /etc/nginx/sites-available/wifi-qr-generator
# Replace 'your-domain.com' with your actual domain or EC2 public IP
```

## GitHub Secrets Setup

Add these secrets to your GitHub repository (Settings → Secrets and variables → Actions):

### Required Secrets:
- `EC2_HOST`: Your EC2 instance public IP address
- `EC2_USER`: SSH username (usually `ubuntu` for Ubuntu instances)
- `EC2_SSH_KEY`: Your private SSH key content

### Setting up SSH Key Secret:
1. Copy your private key content:
   ```bash
   cat ~/.ssh/your-key.pem
   ```
2. Add the entire content (including header/footer) to `EC2_SSH_KEY` secret

## How the CI/CD Pipeline Works

### Trigger Events:
- Push to `main` branch
- Merged pull requests to `main` branch

### Pipeline Steps:
1. **Test Phase**: Runs pytest on the application
2. **Deploy Phase**: 
   - Connects to EC2 via SSH
   - Pulls latest code from GitHub
   - Updates Python dependencies
   - Restarts the application service
   - Reloads nginx

### Deployment Location:
- Application directory: `/opt/wifi-qr-generator`
- Service name: `wifi-qr-generator`
- Port: 5001 (proxied through nginx on port 80)

## Monitoring and Troubleshooting

### Check application status:
```bash
sudo systemctl status wifi-qr-generator
```

### View application logs:
```bash
sudo journalctl -u wifi-qr-generator -f
```

### Check nginx status:
```bash
sudo systemctl status nginx
```

### Restart services if needed:
```bash
sudo systemctl restart wifi-qr-generator
sudo systemctl restart nginx
```

## Security Considerations

The nginx configuration includes:
- Security headers
- Hidden server tokens
- Proxy settings for the Flask application

## Accessing the Application

Once deployed, access your application at:
- `http://YOUR_EC2_PUBLIC_IP`
- `http://YOUR_DOMAIN` (if you've configured a domain)

## Manual Deployment

If you need to deploy manually without GitHub Actions:
```bash
cd /opt/wifi-qr-generator
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart wifi-qr-generator
```