# AOCTimerMap

### Features : 
- permet de marquer les boss et les ressources (et ce que vous voulez) sur la carte, vous pouvez mettre un timer et le respawn time, et le type
- Tout les pins sont mis en base de donnée, et tout le monde récupere tout les marqueurs et tout les timers ( mis à jour toutes minutes en direct)
sous forme de pin de loin, et de petit carré avec le timer quand c'est zoom; avec le pti icon
- on peut clic pour R (reset le timer), ou M (annoncé que c'est missing)
marqueur rouge pendant le temps où c'est en cooldown. Si tu récupere la resource ou voit le boss mourir, tu clic et reset le timer, il sera rouge pendant 30m ( ou le temps du cooldown réglé) puis reviendra à bleu. (passe jaune pendant le temps de cd si il est marqué missing)
- si l'icone du type existe dans le project, ça met un pti icon, (liste des icons pour l'instant: https://github.com/Quindan/AOCTimerMap/tree/main/src/icons)

### Utilisation : 
- Je coupe un wipping willow legendaire, je vais sur la map, je zoom bien et je clic dessus, je tape 'wipping legendaire' ou peu importe, tape le temps (je crois que c'est 4heure, alors tu tape '4h'), et le type (j'ai mis 'ww' pour wipping willow,mais il y a 'wood' qui existe si tu veux pas te prendre la tete).
- Le point apparait sur la carte pour tout le monde dans la minute, reste rouge pendant 4h.
4h après, le pin repasse bleu. Je reprend le willow. Je clic sur le pin, tape 'r' pour reset. Il redevient rouge pour tout le monde. si les gens zoom, ils voyent le timer précis.


# Requirements

## System Requirements

Before deploying AOCTimerMap, ensure your server has the following dependencies installed:

### Essential Tools
- **Git** - Version control (usually pre-installed)
- **Make** - Build automation tool
- **Build-essential** - Compilation tools (gcc, g++, etc.)

### Container Platform
- **Docker** - Container runtime and engine

### Web Server Tools  
- **Apache2-utils** - Provides `htpasswd` for basic authentication

## Installation Commands

### Ubuntu/Debian Server Setup

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install essential build tools and make
sudo apt install -y make build-essential

# Install Docker (official script)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install apache2-utils for basic auth
sudo apt install -y apache2-utils

# Verify installations
make --version
docker --version
htpasswd
```

### Alternative: One-Line Installation

```bash
# Complete server setup in one command
sudo apt update -y && sudo apt install -y make build-essential apache2-utils && curl -fsSL https://get.docker.com | sh
```

## Deployment

### Quick Deployment

```bash
# Clone the project
git clone https://github.com/Quindan/AOCTimerMap.git
cd AOCTimerMap

# Install dependencies and deploy
make install && make build && make create && make run
```

### Manual Step-by-Step

```bash
# 1. Install local dependencies (creates db/, sets permissions)
make install

# 2. Build Docker image
make build

# 3. Initialize database with proper permissions
make create

# 4. Run the application
make run
```

### Set Authentication Password

The application uses HTTP Basic Authentication with nginx. You need to create a `.htpasswd` file:

```bash
# Create/update user with username and password
make addUser USER=invicta ARGS="-c"

# Or manually create .htpasswd:
htpasswd -cb docker/nginx/.htpasswd invicta invicta

# After creating/updating auth, restart the container:
make restart
```

**Default credentials:** `invicta:invicta`

## Verification

After deployment, verify the application is running:

```bash
# Check container status
docker ps

# Test web access (should return 401 - authentication required)
curl -I http://your-server-ip/

# Check application logs
make logs

# Get detailed error logs (Docker + Nginx errors and access logs)
make error-logs
```

Your application will be accessible at `http://your-server-ip/` with basic authentication.

# Database Management

## Initialize Database

If you encounter database errors like "unable to open database file", run:

```bash
# Initialize database with proper permissions
make create

# Restart container to apply changes
make restart
```

This command:
- Creates the `db/` directory if missing
- Creates `mydb.sqlite` file
- Sets proper permissions for www-data user
- Ensures the container can access the database

## Known Issues

- **Database Path**: The SQLite database must be accessible at `/var/www/db/mydb.sqlite` inside the container
- **Permissions**: Database files need `www-data:www-data` ownership and `ug+rw` permissions
- **Pin Creation**: Cancel pin creation doesn't work properly
- **Pin Colors**: Delay for pin getting the right color, will move to icon instead of CSS rotation
- **Icons**: Missing icons - consider taking directly from codex instead of copying
