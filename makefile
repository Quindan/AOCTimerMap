# Makefile for AOCTimerMap
# Default goal is "help", so "make" alone shows usage.

.PHONY: help install build run stop down update logs create addUser compose-up compose-down compose-dev compose-feature deploy-branch hub-build hub-start hub-logs hub-stop prod-start prod-stop start portal-build fetch-named-mobs import-named-mobs error-logs local dev prod prod-stop prod-logs prod-status prod-backup bookstack-up bookstack-down bookstack-backup bookstack-restore bookstack-prod-up bookstack-prod-down bookstack-prod-backup bookstack-prod-restore

.DEFAULT_GOAL := help

IMAGE_NAME = aoctimermap
CONTAINER_NAME = aoctimermap_container
WEB_USER = www-data

help:
	@echo "Usage: make <target>"
	@echo
	@echo "Targets:"
	@echo "  help     Show this help message"
	@echo "  install  Install apache2-utils on host, prepare db/ folder, set perms"
	@echo "  build    Build the Docker image (env only, no code inside)"
	@echo "  run      Run container, mounting src/, db/, and .htpasswd"
	@echo "  stop     Stop (but not remove) container"
	@echo "  down     Remove container"
	@echo "  update   Pull code, stop/down old container, run new"
	@echo "  logs     Follow container logs (ctrl+c to quit)"
	@echo "  create   Initialize database with proper permissions"
	@echo "  addUser  Add or update a user in docker/nginx/.htpasswd (on host)"
	@echo ""
	@echo "Docker Compose Commands:"
	@echo "  compose-up       Start main production service"
	@echo "  compose-down     Stop all services"
	@echo "  compose-dev      Start development service (port 8080)"
	@echo "  compose-feature  Start feature testing service (port 8081)"
	@echo "  deploy-branch    Deploy specific branch (usage: make deploy-branch BRANCH=feature/named-timers ENV=feature)"
	@echo ""
	@echo "Development Commands:"
	@echo "  local            Build complete local environment (port 9090)"
	@echo "  dev              Quick Angular rebuild and container restart"
	@echo ""
	@echo "Production Commands:"
	@echo "  prod             Deploy to production with backup and complete build (port 80)"
	@echo "  prod-stop        Stop production container"
	@echo "  prod-logs        Show production container logs"
	@echo "  prod-status      Show production container status"
	@echo "  prod-backup      Create production database backup"
	@echo ""
	@echo "BookStack Wiki Commands:"
	@echo "  bookstack-up     Start BookStack wiki service (port 8082)"
	@echo "  bookstack-down   Stop BookStack wiki service"
	@echo "  bookstack-backup Create BookStack database backup"
	@echo "  bookstack-restore FILE=backup.sql Restore BookStack database"
	@echo "  bookstack-prod-up Start BookStack in production (port 8083)"
	@echo "  bookstack-prod-down Stop BookStack production"
	@echo "  bookstack-prod-backup Create production BookStack backup"
	@echo "  bookstack-prod-restore FILE=backup.sql Restore production BookStack"

install:
	@echo "Installing apache2-utils (provides 'htpasswd') on the host..."
	sudo apt-get update -y
	sudo apt-get install -y apache2-utils
	@echo "Creating db folder + mydb.sqlite if missing..."
	mkdir -p db
	touch db/mydb.sqlite
	@echo "Fixing ownership and permissions for src/ & db/ so container can access..."
	sudo chown -R $(WEB_USER):$(WEB_USER) src db
	sudo chmod -R ug+rw src db
	@echo "If you plan to use .htpasswd for basic auth, consider creating it in docker/nginx/.htpasswd."
	@echo "Install done."

build:
	docker build -t $(IMAGE_NAME) .

run:
	@echo "Starting container '$(CONTAINER_NAME)'..."
	docker run -d \
		-p 80:80 \
		--name $(CONTAINER_NAME) \
		-v $(PWD)/src:/var/www/html \
		-v $(PWD)/db:/var/www/db \
		-v $(PWD)/docker/nginx/.htpasswd:/etc/nginx/.htpasswd \
		$(IMAGE_NAME)
	@echo ""
	@echo "==========================================================="
	@echo "Container is running in detached mode."
	@echo "Access the site at http://<server-ip>/"
	@echo "If you enabled basic auth, use the username/password from .htpasswd"
	@echo "==========================================================="
	@echo ""

stop:
	@echo "Stopping container '$(CONTAINER_NAME)'..."
	docker stop $(CONTAINER_NAME) || true

down:
	@echo "Removing container '$(CONTAINER_NAME)'..."
	docker rm $(CONTAINER_NAME) || true

update:
	@echo "🚀 Starting comprehensive production update..."
	@echo "📅 Creating timestamp for backup..."
	@TIMESTAMP=$$(date +"%Y%m%d_%H%M%S"); \
	echo "Update timestamp: $$TIMESTAMP"

	@echo "💾 Creating database backup before update..."
	@TIMESTAMP=$$(date +"%Y%m%d_%H%M%S"); \
	mkdir -p backups; \
	if [ -f db/mydb.sqlite ]; then \
		cp db/mydb.sqlite backups/mydb_backup_$$TIMESTAMP.sqlite; \
		echo "✅ Database backed up to: backups/mydb_backup_$$TIMESTAMP.sqlite"; \
	else \
		echo "⚠️  No existing database found to backup"; \
	fi

	@echo "📥 Pulling latest code from git..."
	git pull origin main

	@echo "🛑 Stopping all services..."
	$(MAKE) compose-down

	@echo "🧹 Cleaning Docker cache and rebuilding image..."
	docker system prune -f
	docker build --no-cache -t $(IMAGE_NAME) .

	@echo "🚀 Starting updated services..."
	$(MAKE) compose-up

	@echo "📊 Verifying deployment status..."
	$(MAKE) prod-status

	@echo "✅ Production update completed successfully!"
	@echo "🌐 Services available at:"
	@echo "   - Main application: http://84.247.141.193/"
	@echo "   - BookStack wiki: http://84.247.141.193:8083"

restart:
		$(MAKE) stop
		$(MAKE) down
		$(MAKE) run

logs:
	@echo "Showing logs for container '$(CONTAINER_NAME)' (ctrl+c to quit)..."
	docker logs -f $(CONTAINER_NAME)

error-logs:
	@echo "Getting error logs from container..."
	@echo "=== Docker container logs ==="
	docker logs $(CONTAINER_NAME) --tail 20
	@echo ""
	@echo "=== Nginx error logs ==="
	docker exec $(CONTAINER_NAME) cat /var/log/nginx/error.log 2>/dev/null || echo "No nginx error log found"
	@echo ""
	@echo "=== Nginx access logs ==="
	docker exec $(CONTAINER_NAME) cat /var/log/nginx/access.log 2>/dev/null || echo "No nginx access log found"

bash:
	docker exec -it aoctimermap_container bash

create:
	@echo "Initializing database and permissions..."
	mkdir -p db data
	@if [ ! -f db/mydb.sqlite ]; then \
		touch db/mydb.sqlite || sudo touch db/mydb.sqlite; \
	fi
	@echo "Setting proper permissions for database..."
	sudo chown -R $$USER:$$USER db data || true
	chmod -R 755 db data || true
	@echo "Database initialized at db/mydb.sqlite"

fetch-named-mobs:
	@echo "Fetching named mobs data from Ashes Codex API..."
	php scripts/fetch_named_mobs.php
	@echo "Named mobs data saved to data/named_mobs.json and data/named_mobs.sql"

import-named-mobs: fetch-named-mobs
	@echo "Importing named mobs into database..."
	@if [ -f "data/named_mobs.sql" ]; then \
		echo "Importing SQL data..."; \
		sqlite3 db/mydb.sqlite < data/named_mobs.sql; \
		echo "Named mobs imported successfully!"; \
	else \
		echo "Error: data/named_mobs.sql not found. Run 'make fetch-named-mobs' first."; \
	fi

# InvictaWeb Hub commands
hub-build:
	@echo "🏗️ Building InvictaWeb..."
	docker build -f Dockerfile.monolith -t invictaweb:latest .
	@echo "InvictaWeb built successfully!"

# Simplified working local setup
local:
	@echo "🚀 Building complete local environment from scratch..."
	
	@echo "📦 Building Docker image..."
	docker build -t $(IMAGE_NAME) .
	
	@echo "🧹 Cleaning Angular cache and rebuilding..."
	cd services/aoc-timer-map/dev && npm run ng cache clean 2>/dev/null || true
	cd services/aoc-timer-map/dev && npm run build
	
	@echo "📁 Copying Angular build files (preserving custom files)..."
	# Copy only the JS/CSS files from Angular build, preserve our custom index.html
	cp services/aoc-timer-map/dev/dist/aoc-map/browser/*.js services/aoc-timer-map/ 2>/dev/null || true
	cp services/aoc-timer-map/dev/dist/aoc-map/browser/*.css services/aoc-timer-map/ 2>/dev/null || true
	cp services/aoc-timer-map/dev/dist/aoc-map/browser/*.map services/aoc-timer-map/ 2>/dev/null || true
	cp services/aoc-timer-map/dev/dist/aoc-map/browser/favicon.ico services/aoc-timer-map/ 2>/dev/null || true
	
	@echo "📄 Setting up map routing..."
	mkdir -p services/aoc-timer-map/map
	# Copy the Angular index.html only to the map subdirectory
	cp services/aoc-timer-map/dev/dist/aoc-map/browser/index.html services/aoc-timer-map/map/
	
	# Add timestamp to prevent caching
	sed -i "s/<!-- Dev build: \$(date) -->/<!-- Dev build: $$(date) -->/" services/aoc-timer-map/map/index.html
	mkdir -p services/aoc-timer-map/assets/icons
	
	@echo "🛑 Stopping existing container..."
	docker stop invictaweb-local 2>/dev/null || true
	docker rm invictaweb-local 2>/dev/null || true
	
	@echo "🚀 Starting fresh container..."
	docker run -d --name invictaweb-local \
		-p 9090:80 \
		-v $(PWD)/db:/var/www/db \
		-v $(PWD)/services/aoc-timer-map:/var/www/html \
		-v $(PWD)/infrastructure/nginx/simple.conf:/etc/nginx/http.d/default.conf \
		-v $(PWD)/.htpasswd:/etc/nginx/.htpasswd \
		$(IMAGE_NAME):latest
	
	@echo ""
	@echo "🎉 InvictaWeb fully rebuilt and running!"
	@echo "🏠 Landing Page: http://localhost:9090/"
	@echo "🗺️  Timer Map: http://localhost:9090/map/"
	@echo "📖 Guild Wiki: http://localhost:9090/guides/"
	@echo "🏆 Named Mobs: http://localhost:9090/named-mobs"
	@echo "🔐 Login: invicta / password"
	@echo "🚫 All caching disabled for development"
	@echo ""
	@echo "🧪 Testing connection..."
	@sleep 3
	@curl -s -u invicta:password -o /dev/null -w "Main App: %{http_code}\n" http://localhost:9090/
	@curl -s -u invicta:password -o /dev/null -w "Named Mobs: %{http_code}\n" http://localhost:9090/named-mobs

# Development: Only rebuild Angular and restart container
dev:
	@echo "🔄 Rebuilding Angular and restarting container..."
	@echo "🧹 Cleaning Angular cache and rebuilding..."
	cd services/aoc-timer-map/dev && npm run ng cache clean 2>/dev/null || true
	cd services/aoc-timer-map/dev && npm run build
	
	@echo "📁 Copying Angular build files (preserving custom files)..."
	# Copy only the JS/CSS files from Angular build, preserve our custom index.html
	cp services/aoc-timer-map/dev/dist/aoc-map/browser/*.js services/aoc-timer-map/ 2>/dev/null || true
	cp services/aoc-timer-map/dev/dist/aoc-map/browser/*.css services/aoc-timer-map/ 2>/dev/null || true
	cp services/aoc-timer-map/dev/dist/aoc-map/browser/*.map services/aoc-timer-map/ 2>/dev/null || true
	cp services/aoc-timer-map/dev/dist/aoc-map/browser/favicon.ico services/aoc-timer-map/ 2>/dev/null || true
	
	@echo "📄 Setting up map routing..."
	mkdir -p services/aoc-timer-map/map
	# Copy the Angular index.html only to the map subdirectory
	cp services/aoc-timer-map/dev/dist/aoc-map/browser/index.html services/aoc-timer-map/map/
	
	# Add timestamp to prevent caching
	sed -i "s/<!-- Dev build: \$(date) -->/<!-- Dev build: $$(date) -->/" services/aoc-timer-map/map/index.html
	
	@echo "🔄 Restarting container..."
	docker restart invictaweb-local
	
	@echo "✅ Development rebuild complete!"
	@echo "🏠 Landing Page: http://localhost:9090/"
	@echo "🗺️  Timer Map: http://localhost:9090/map/"

hub-start: create
	@echo "🚀 Starting InvictaWeb..."
	@echo "📁 Ensuring directories exist..."
	mkdir -p logs/nginx logs/php
	@echo "🐳 Starting services..."
	docker compose -f docker-compose.hub.yml up -d
	@echo ""
	@echo "🎉 InvictaWeb is running!"
	@echo "🌐 Portal: http://localhost:9090/"
	@echo "🗺️  Map: http://localhost:9090/map/"
	@echo "📚 API Docs: http://localhost:9090/api-docs/"
	@echo "🔍 Health: http://localhost:9090/health"
	@echo ""
	@echo "🔐 Login: invicta / password"

hub-logs:
	@echo "📊 InvictaWeb logs..."
	docker compose -f docker-compose.hub.yml logs -f

hub-stop:
	@echo "🛑 Stopping InvictaWeb..."
	docker compose -f docker-compose.hub.yml down
	@echo "InvictaWeb stopped."

# Production deployment
prod-start: create
	@echo "🚀 Starting InvictaWeb (Production)..."
	@echo "📁 Ensuring directories exist..."
	mkdir -p logs/nginx logs/php
	@echo "🐳 Starting services on port 80..."
	docker compose -f docker-compose.hub.yml -f docker-compose.prod.yml up -d
	@echo ""
	@echo "🎉 InvictaWeb is running in production mode!"
	@echo "🌐 Portal: http://localhost/"
	@echo "🗺️  Map: http://localhost/map/"
	@echo "📚 API Docs: http://localhost/api-docs/"
	@echo "🔍 Health: http://localhost/health"
	@echo ""
	@echo "🔐 Login: invicta / password"


# Aliases for convenience
start: hub-start
stop: hub-stop
logs: hub-logs

portal-build:
	@echo "🏗️ Building main portal..."
	@if [ -d "services/main-portal" ]; then \
		cd services/main-portal && npm install && npm run build; \
		echo "Portal built successfully!"; \
	else \
		echo "Portal source not found, using static version"; \
	fi

# Docker Compose commands
compose-up:
	@echo "Starting main production service with docker-compose..."
	docker-compose up -d aoctimermap-main
	@echo "Service available at http://localhost"

compose-down:
	@echo "Stopping all docker-compose services..."
	docker-compose down

compose-dev:
	@echo "Starting development service with docker-compose..."
	mkdir -p db-dev
	touch db-dev/mydb.sqlite
	sudo chown -R $(WEB_USER):$(WEB_USER) db-dev
	sudo chmod -R ug+rw db-dev
	docker-compose --profile dev up -d aoctimermap-dev
	@echo "Development service available at http://localhost:8080"

compose-feature:
	@echo "Starting feature testing service with docker-compose..."
	mkdir -p db-feature
	touch db-feature/mydb.sqlite
	sudo chown -R $(WEB_USER):$(WEB_USER) db-feature
	sudo chmod -R ug+rw db-feature
	docker-compose --profile feature up -d aoctimermap-feature
	@echo "Feature service available at http://localhost:8081"

deploy-branch:
	@echo "Deploying branch with deployment script..."
	@BRANCH=${BRANCH:-main}; \
	ENV=${ENV:-development}; \
	echo "Branch: $$BRANCH, Environment: $$ENV"; \
	./scripts/branch-deploy.sh "$$BRANCH" "$$ENV"

addUser:
	@echo "Add/Update user in docker/nginx/.htpasswd on the host..."
	@echo "Usage: make addUser USER=alice ARGS='-c'"
	@echo " '-c' overwrites if you want a clean file. Otherwise it appends or updates."
	@echo "Example: make addUser USER=alice ARGS='-B' => create hashed password with bcrypt."
	@echo ""
	@[ -n "$(USER)" ] || (echo "ERROR: Missing USER=..." && exit 1)
	htpasswd $(ARGS) docker/nginx/.htpasswd $(USER)
	@echo "User '$(USER)' added/updated. If container is running, you may need to 'make stop' and 'make run' again."

# Production deployment with database backup and complete build
prod:
	@echo "🚀 Preparing production deployment..."
	@echo "📅 Creating timestamp for backup..."
	@TIMESTAMP=$$(date +"%Y%m%d_%H%M%S"); \
	echo "Backup timestamp: $$TIMESTAMP"

	@echo "💾 Creating database backup..."
	@TIMESTAMP=$$(date +"%Y%m%d_%H%M%S"); \
	mkdir -p backups; \
	if [ -f db/mydb.sqlite ]; then \
		cp db/mydb.sqlite backups/mydb_backup_$$TIMESTAMP.sqlite; \
		echo "✅ Database backed up to: backups/mydb_backup_$$TIMESTAMP.sqlite"; \
	else \
		echo "⚠️  No existing database found to backup"; \
	fi

	@echo "🛑 Stopping existing containers..."
	@docker stop invictaweb-prod 2>/dev/null || true
	@docker rm invictaweb-prod 2>/dev/null || true

	@echo "🧹 Cleaning Angular cache and rebuilding for production..."
	@cd services/aoc-timer-map/dev && npm run ng cache clean 2>/dev/null || true
	@cd services/aoc-timer-map/dev && npm run build --configuration=production

	@echo "📁 Setting up production files..."
	@mkdir -p services/aoc-timer-map/map
	@mkdir -p services/aoc-timer-map/assets/icons
	@mkdir -p services/aoc-timer-map/assets/images
	
	@echo "📦 Copying Angular build assets to map directory..."
	@cp services/aoc-timer-map/dev/dist/aoc-map/browser/*.js services/aoc-timer-map/map/
	@cp services/aoc-timer-map/dev/dist/aoc-map/browser/*.css services/aoc-timer-map/map/
	@cp services/aoc-timer-map/dev/dist/aoc-map/browser/*.ico services/aoc-timer-map/map/
	@cp services/aoc-timer-map/dev/dist/aoc-map/browser/*.map services/aoc-timer-map/map/
	@cp services/aoc-timer-map/dev/dist/aoc-map/browser/index.html services/aoc-timer-map/map/
	
	@echo "⚠️  Preserving custom landing page (not overwriting index.html)..."

	@echo "📄 Copying Angular production build (preserving custom landing page)..."
	@cp services/aoc-timer-map/dev/dist/aoc-map/browser/*.js services/aoc-timer-map/ 2>/dev/null || true
	@cp services/aoc-timer-map/dev/dist/aoc-map/browser/*.css services/aoc-timer-map/ 2>/dev/null || true
	@cp services/aoc-timer-map/dev/dist/aoc-map/browser/*.map services/aoc-timer-map/ 2>/dev/null || true
	@cp services/aoc-timer-map/dev/dist/aoc-map/browser/favicon.ico services/aoc-timer-map/ 2>/dev/null || true
	@cp services/aoc-timer-map/dev/dist/aoc-map/browser/index.html services/aoc-timer-map/map/
	@echo "✅ Landing page preserved - Angular index.html only copied to /map/"

	@echo "🐳 Building production Docker image..."
	@docker build -t $(IMAGE_NAME):prod .

	@echo "🚀 Starting production container on port 80..."
	@docker run -d --name invictaweb-prod \
		-p 80:80 \
		-v $(PWD)/db:/var/www/db \
		-v $(PWD)/services/aoc-timer-map:/var/www/html \
		-v $(PWD)/infrastructure/nginx/simple.conf:/etc/nginx/http.d/default.conf \
		-v $(PWD)/.htpasswd:/etc/nginx/.htpasswd \
		$(IMAGE_NAME):prod

	@echo ""
	@echo "🎉 InvictaWeb deployed to production!"
	@echo "🌐 Production URL: http://localhost/"
	@echo "🗺️  Timer Map: http://localhost/map/"
	@echo "📖 Guild Wiki: http://localhost/guides/"
	@echo "🏆 Named Mobs: http://localhost/named-mobs"
	@echo "🔐 Login: invicta / password"
	@echo ""
	@echo "🧪 Testing production deployment..."
	@sleep 3
	@curl -s -u invicta:password -o /dev/null -w "Main App: %{http_code}\n" http://localhost/
	@curl -s -u invicta:password -o /dev/null -w "Named Mobs: %{http_code}\n" http://localhost/named-mobs

# Production management commands
prod-stop:
	@echo "🛑 Stopping production container..."
	@docker stop invictaweb-prod 2>/dev/null || true
	@docker rm invictaweb-prod 2>/dev/null || true
	@echo "✅ Production container stopped and removed"

prod-logs:
	@echo "📋 Showing production container logs..."
	@docker logs invictaweb-prod

prod-status:
	@echo "📊 Production container status..."
	@docker ps -a --filter name=invictaweb-prod

prod-backup:
	@echo "💾 Creating production database backup..."
	@TIMESTAMP=$$(date +"%Y%m%d_%H%M%S"); \
	mkdir -p backups; \
	if [ -f db/mydb.sqlite ]; then \
		cp db/mydb.sqlite backups/mydb_backup_$$TIMESTAMP.sqlite; \
		echo "✅ Database backed up to: backups/mydb_backup_$$TIMESTAMP.sqlite"; \
		ls -la backups/mydb_backup_$$TIMESTAMP.sqlite; \
	else \
		echo "⚠️  No database found to backup"; \
	fi

# BookStack Wiki Management
bookstack-up:
	@echo "📚 Starting BookStack wiki service..."
	@mkdir -p bookstack-data bookstack-db bookstack-backups
	@docker-compose --profile bookstack up -d
	@echo "✅ BookStack started on http://localhost:8082"
	@echo "📖 Default login: admin@admin.com / password"

bookstack-down:
	@echo "📚 Stopping BookStack wiki service..."
	@docker-compose --profile bookstack down
	@echo "✅ BookStack stopped"

bookstack-backup:
	@echo "💾 Creating BookStack database backup..."
	@TIMESTAMP=$$(date +"%Y%m%d_%H%M%S"); \
	mkdir -p bookstack-backups; \
	docker exec bookstack-db mysqldump -u bookstack -pbookstack_password bookstack > bookstack-backups/bookstack_backup_$$TIMESTAMP.sql; \
	echo "✅ BookStack backup created: bookstack-backups/bookstack_backup_$$TIMESTAMP.sql"; \
	ls -la bookstack-backups/bookstack_backup_$$TIMESTAMP.sql

bookstack-restore:
	@echo "📥 Restoring BookStack database from backup..."
	@if [ -z "$(FILE)" ]; then \
		echo "❌ Please specify backup file: make bookstack-restore FILE=backup_file.sql"; \
		echo "Available backups:"; \
		ls -la bookstack-backups/; \
		exit 1; \
	fi
	@if [ ! -f "bookstack-backups/$(FILE)" ]; then \
		echo "❌ Backup file not found: bookstack-backups/$(FILE)"; \
		exit 1; \
	fi
	@echo "🔄 Restoring from: bookstack-backups/$(FILE)"
	@docker exec -i bookstack-db mysql -u bookstack -pbookstack_password bookstack < bookstack-backups/$(FILE)
	@echo "✅ BookStack database restored successfully"

# Production BookStack commands
bookstack-prod-up:
	@echo "🚀 Starting BookStack in production mode..."
	docker-compose -f docker-compose.prod.yml up -d
	@echo "✅ BookStack production started on port 8083"
	@echo "🌐 Access: http://84.247.141.193:8083"

bookstack-prod-down:
	@echo "🛑 Stopping BookStack production..."
	docker-compose -f docker-compose.prod.yml down
	@echo "✅ BookStack production stopped"

bookstack-prod-backup:
	@echo "💾 Creating BookStack production backup..."
	@mkdir -p bookstack-backups
	@TIMESTAMP=$$(date +%Y%m%d_%H%M%S); \
	docker-compose -f docker-compose.prod.yml exec bookstack-db-prod mysqldump -u bookstack -pbookstack_password bookstack > bookstack-backups/bookstack_prod_backup_$$TIMESTAMP.sql; \
	echo "✅ Production backup created: bookstack-backups/bookstack_prod_backup_$$TIMESTAMP.sql"

bookstack-prod-restore:
	@echo "📥 Restoring BookStack production database from backup..."
	@if [ -z "$(FILE)" ]; then \
		echo "❌ Please specify backup file: make bookstack-prod-restore FILE=backup_file.sql"; \
		echo "Available backups:"; \
		ls -la bookstack-backups/; \
		exit 1; \
	fi
	@if [ ! -f "bookstack-backups/$(FILE)" ]; then \
		echo "❌ Backup file not found: bookstack-backups/$(FILE)"; \
		exit 1; \
	fi
	@echo "🔄 Restoring from: bookstack-backups/$(FILE)"
	@docker exec -i bookstack-db-prod mysql -u bookstack -pbookstack_password bookstack < bookstack-backups/$(FILE)
	@echo "✅ BookStack production database restored successfully"
