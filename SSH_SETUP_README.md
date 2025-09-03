# SSH Key Setup for AOCTimerMap Server

This guide will help you set up SSH key authentication to connect to your VPS server without entering a password each time.

## Server Information

- **Server IP**: `84.247.141.193`
- **User**: `root`
- **Current Password**: `1r0N1gKK5Yx9P`
- **VNC Access**: `5.189.133.152:63330`

## Prerequisites

- SSH client installed (comes with Linux/macOS, or use OpenSSH on Windows)
- Access to your local terminal

## Step 1: Generate SSH Key Pair (if not already done)

Check if you already have SSH keys:
```bash
ls -la ~/.ssh/
```

If you see `id_rsa` and `id_rsa.pub`, you already have keys. Skip to Step 2.

If not, generate new SSH keys:
```bash
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"
```

When prompted:
- Press Enter to save in default location (`~/.ssh/id_rsa`)
- Enter a passphrase (optional but recommended)
- Confirm the passphrase

## Step 2: Copy Your Public Key to the Server

### Method 1: Using ssh-copy-id (recommended)
```bash
ssh-copy-id root@84.247.141.193
```

When prompted, enter the server password: `1r0N1gKK5Yx9P`

### Method 2: Manual Copy
If `ssh-copy-id` is not available:

1. Display your public key:
```bash
cat ~/.ssh/id_rsa.pub
```

2. Copy the entire output (starts with `ssh-rsa`)

3. Connect to the server:
```bash
ssh root@84.247.141.193
```

4. On the server, create the SSH directory and authorized_keys file:
```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "your-public-key-content-here" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

5. Exit the server:
```bash
exit
```

## Step 3: Test SSH Key Authentication

Test the connection without password:
```bash
ssh root@84.247.141.193
```

You should now connect without entering a password (only your SSH key passphrase if you set one).

## Step 4: Secure the Server (Optional but Recommended)

Once key authentication works, you can disable password authentication for better security:

1. Connect to the server:
```bash
ssh root@84.247.141.193
```

2. Edit the SSH configuration:
```bash
nano /etc/ssh/sshd_config
```

3. Find and modify these lines:
```
PasswordAuthentication no
PubkeyAuthentication yes
PermitRootLogin yes
```

4. Restart SSH service:
```bash
systemctl restart ssh
```

5. Test the connection from another terminal before closing the current one to ensure you can still connect.

## Common Commands for Server Management

### Connect to Server
```bash
ssh root@84.247.141.193
```

### Copy Files to Server
```bash
scp /local/file/path root@84.247.141.193:/remote/path/
```

### Copy Entire Directory
```bash
scp -r /local/directory/ root@84.247.141.193:/remote/path/
```

### Run Command on Server Without Logging In
```bash
ssh root@84.247.141.193 "command-to-run"
```

### Transfer Project Files
```bash
# From project directory
scp -r . root@84.247.141.193:/var/www/aoctimermap/
```

## Server Setup (Required Before Deployment)

The server needs Docker and basic web environment setup. Run these commands:

```bash
# Connect to server
ssh root@84.247.141.193

# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install make and other tools
apt install -y make git

# Create web directory
mkdir -p /var/www/aoctimermap

# Set proper permissions
chown -R root:root /var/www/aoctimermap
chmod -R 755 /var/www/aoctimermap
```

## Deployment Commands

### Initial Deployment
```bash
# From local machine - copy project files
scp -r . root@84.247.141.193:/var/www/aoctimermap/

# Connect to server
ssh root@84.247.141.193

# Navigate to project directory
cd /var/www/aoctimermap

# Install dependencies and setup
make install

# Build and run Docker container
make build
make run
```

### Check Application Status
```bash
ssh root@84.247.141.193 "docker ps"
ssh root@84.247.141.193 "docker logs aoctimermap_container"
```

## Troubleshooting

### Connection Refused
```bash
# Check if SSH service is running on server
ssh root@84.247.141.193 "systemctl status ssh"
```

### Permission Denied
```bash
# Check SSH key permissions
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
chmod 700 ~/.ssh
```

### Verbose Connection for Debugging
```bash
ssh -v root@84.247.141.193
```

### Reset to Password Authentication (if locked out)
Use VNC access at `5.189.133.152:63330` to access the server console and fix SSH configuration.

## Environment Variables

Your `.env` file should contain:
```bash
SERVER_HOST=84.247.141.193
SERVER_PORT=22
SERVER_USER=root
SSH_KEY_PATH=~/.ssh/id_rsa
DEPLOY_PATH=/var/www/aoctimermap
```

## Security Notes

1. **Never share your private key** (`~/.ssh/id_rsa`)
2. **Keep your private key secure** with proper file permissions (600)
3. **Use a passphrase** for your SSH key for additional security
4. **Disable password authentication** once key auth is working
5. **Regular backups** of your server and SSH keys

## VNC Access (Emergency)

If SSH access fails, you can use VNC to access the server console:
- **VNC Address**: `5.189.133.152:63330`
- **VNC Password**: `5.189.133.152:63330`

Use a VNC client like TigerVNC, RealVNC, or TightVNC to connect.
