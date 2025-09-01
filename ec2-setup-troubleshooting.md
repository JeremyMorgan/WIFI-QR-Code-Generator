# EC2 SSH Authentication Troubleshooting

## Step 1: Verify Manual SSH Access

First, ensure you can SSH to your EC2 instance manually:

```bash
ssh -i ~/.ssh/your-key.pem ubuntu@your-ec2-public-ip
```

If this fails, the issue is with your EC2 setup, not GitHub Actions.

## Step 2: Check EC2 Security Group

Ensure your security group allows SSH (port 22) access:
- Protocol: TCP
- Port Range: 22
- Source: 0.0.0.0/0 (or your IP range)

## Step 3: Generate Deployment Key Specifically for GitHub Actions

```bash
# Generate a new ed25519 key (more compatible)
ssh-keygen -t ed25519 -f ~/.ssh/github-actions-key -N ""

# Display the private key (copy this to GitHub secret EC2_SSH_KEY)
cat ~/.ssh/github-actions-key

# Display the public key (add this to EC2)
cat ~/.ssh/github-actions-key.pub
```

## Step 4: Add Public Key to EC2 Instance

Connect to your EC2 instance and add the public key:

```bash
# On your EC2 instance
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Add your public key to authorized_keys
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI..." >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# Restart SSH service (if needed)
sudo systemctl restart ssh
```

## Step 5: Test the New Key

Test the new key locally:
```bash
ssh -i ~/.ssh/github-actions-key ubuntu@your-ec2-public-ip
```

## Step 6: Update GitHub Secrets

Go to GitHub → Settings → Secrets and variables → Actions:

- `EC2_HOST`: Your EC2 public IP (e.g., `3.85.123.456`)
- `EC2_USER`: `ubuntu`
- `EC2_SSH_KEY`: Content of `~/.ssh/github-actions-key` (the private key, not .pub)

## Step 7: Run Initial Setup

You must run the initial setup script on your EC2 instance BEFORE GitHub Actions can deploy:

```bash
# On your EC2 instance, create the directory structure
sudo mkdir -p /opt/wifi-qr-generator
sudo chown ubuntu:ubuntu /opt/wifi-qr-generator

# Clone the repository
git clone https://github.com/YOUR_USERNAME/WIFI-QR-Code-Generator.git /opt/wifi-qr-generator
cd /opt/wifi-qr-generator

# Run the deployment script
chmod +x deploy.sh
./deploy.sh
```

## Common Issues:

1. **Wrong key format**: Use ed25519 instead of RSA
2. **Missing initial setup**: The /opt/wifi-qr-generator directory must exist
3. **Permissions**: Ensure ubuntu user owns the application directory
4. **Security groups**: SSH port 22 must be open
5. **Wrong IP**: Use public IP, not private IP for EC2_HOST

## Debug GitHub Actions

The workflow now includes `debug: true` to show more detailed SSH connection information in the GitHub Actions logs.