# Makefile for AOCTimerMap
# Default goal is "help", so "make" alone shows usage.

.PHONY: help install build run stop down update logs create addUser compose-up compose-down compose-dev compose-feature deploy-branch

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
	@echo "Pulling latest code from git..."
	git pull
	@echo "Stopping + removing old container..."
	$(MAKE) stop
	$(MAKE) down
	@echo "Launching new container with updated code..."
	$(MAKE) run

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
	touch db/mydb.sqlite
	@echo "Setting proper permissions for database..."
	sudo chown -R $(WEB_USER):$(WEB_USER) db
	sudo chmod -R ug+rw db
	@echo "Database initialized at db/mydb.sqlite"
	@echo "If container is running, restart it: make restart"

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
