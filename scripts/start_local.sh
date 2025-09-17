#!/bin/bash
# Direct Docker startup script to bypass Docker Compose issues

echo "🅰️  Building Angular frontend first..."
./scripts/build_frontend.sh

echo "🔨 Building Docker image..."
docker build -t aoctimermap_timer-map .

echo "🧹 Cleaning up old containers..."
docker stop aoc-timer-map 2>/dev/null || true
docker rm aoc-timer-map 2>/dev/null || true

echo "🚀 Starting container..."
docker run -d \
  --name aoc-timer-map \
  -p 9090:80 \
  -v $(pwd)/data/database:/app/database \
  -v $(pwd)/data/backups:/app/backups \
  -v $(pwd)/.htpasswd:/app/.htpasswd:ro \
  --restart unless-stopped \
  aoctimermap_timer-map

echo "✅ Container started!"
echo "🌐 Access: http://localhost:9090"
echo "🔐 Login: invicta / invicta"

# Wait a bit and check status
sleep 3
docker ps | grep aoc-timer-map
