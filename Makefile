# AOC Timer Map - Deployment Commands
.PHONY: help local build prod-build prod-deploy prod-stop db-backup db-restore reset

# Default target
help:
	@echo "🎯 AOC Timer Map"
	@echo "==============="
	@echo ""
	@echo "📋 Available commands:"
	@echo "  local        - Start local development (port 9090)"
	@echo "  build        - Build Docker image"
	@echo "  prod-build   - Build production image"
	@echo "  prod-deploy  - Deploy to production"
	@echo "  prod-stop    - Stop production containers"
	@echo "  logs         - View container logs"
	@echo "  db-backup    - Backup SQLite database"
	@echo "  db-restore   - Restore database from backup"
	@echo "  reset        - Reset containers and images"
	@echo "  test         - Run full automated test suite"
	@echo "  test-quick   - Run quick endpoint tests"
	@echo "  test-selenium - Run Selenium browser tests"
	@echo "  test-perf    - Run performance tests"
	@echo ""
	@echo "🔐 Default login: invicta / invicta"

# Local Development
local:
	@echo "🚀 Starting local development with direct Docker..."
	@./scripts/start_local.sh

# Build frontend and Docker image
build: build-frontend
	@echo "🔨 Building Docker image..."
	docker-compose build
	@echo "✅ Build complete!"

# Build Angular frontend properly
build-frontend:
	@echo "🅰️  Building Angular frontend..."
	@./scripts/build_frontend.sh

# Production Build
prod-build:
	@echo "🏭 Building production image..."
	docker build -t aoc-timer-map:latest .
	@echo "✅ Production image built!"

# Production Deploy
prod-deploy: prod-build
	@echo "🚀 Deploying to production..."
	@mkdir -p data/database data/backups
	docker run -d \
		--name aoc-timer-map-prod \
		--restart unless-stopped \
		-p 80:80 \
		-v $(PWD)/data/database:/app/database \
		-v $(PWD)/data/backups:/app/backups \
		-v $(PWD)/.htpasswd:/app/.htpasswd:ro \
		aoc-timer-map:latest
	@echo "✅ Production deployed!"
	@echo "🌐 Access: http://your-domain.com"

# Stop production
prod-stop:
	@echo "🛑 Stopping production..."
	docker stop aoc-timer-map-prod || true
	docker rm aoc-timer-map-prod || true
	@echo "✅ Production stopped!"

# View logs
logs:
	@echo "📋 Container logs:"
	docker-compose logs -f

# Database backup
db-backup:
	@echo "💾 Creating database backup..."
	@mkdir -p data/backups
	@timestamp=$$(date +%Y%m%d_%H%M%S); \
	docker exec $$(docker-compose ps -q timer-map) \
		cp /app/database/mydb.sqlite /app/backups/backup_$$timestamp.sqlite && \
	echo "✅ Backup created: data/backups/backup_$$timestamp.sqlite"

# Database restore
db-restore:
	@echo "🔄 Restoring database..."
	@if [ -z "$(FILE)" ]; then \
		echo "❌ Please specify backup file: make db-restore FILE=backup_20240101_120000.sqlite"; \
		exit 1; \
	fi
	@if [ ! -f "data/backups/$(FILE)" ]; then \
		echo "❌ Backup file not found: data/backups/$(FILE)"; \
		exit 1; \
	fi
	docker exec $$(docker-compose ps -q timer-map) \
		cp /app/backups/$(FILE) /app/database/mydb.sqlite
	@echo "✅ Database restored from: $(FILE)"

# Reset containers
reset:
	@echo "🔄 Resetting containers..."
	docker-compose down -v
	docker system prune -f
	@echo "✅ Reset complete!"

# Update coordinates
update-coordinates:
	@echo "📊 Updating named mob coordinates..."
	python3 scripts/triangulate_coordinates.py
	@echo "✅ Coordinates updated!"

# Test suite (includes quick tests + attempt Selenium)
test: test-quick
	@echo "🧪 Running comprehensive test suite..."
	@python3 scripts/test_suite.py
	@echo "🌐 Attempting Selenium tests..."
	@make test-selenium 2>/dev/null || echo "⚠️  Selenium tests skipped (container issues)"

# Quick tests
test-quick:
	@echo "🚀 Running quick endpoint tests..."
	@bash scripts/test_endpoints.sh

# Test with Selenium
test-selenium:
	@echo "🌐 Running Selenium tests..."
	@docker run --rm --network host -v $(PWD)/scripts:/scripts --entrypoint="" selenium/standalone-chrome:latest /bin/bash -c \
		"pip install selenium && python3 /scripts/selenium_blank_page_debug.py" || \
		echo "⚠️  Selenium container not available, skipping browser tests"

# Performance tests
test-perf:
	@echo "⚡ Running performance tests..."
	@bash scripts/test_performance.sh

# Codex Import System
import-codex: ## Import/update named mob data from Codex (dry-run)
	@echo "📥 Testing Codex import (dry-run)..."
	python3 scripts/smart_codex_import.py --dry-run

import-codex-live: ## Import/update named mob data from Codex (LIVE)
	@echo "📥 Importing Codex data (LIVE)..."
	python3 scripts/smart_codex_import.py

import-report: ## Show current import status
	@echo "📊 Current import status..."
	python3 scripts/smart_codex_import.py --report-only
