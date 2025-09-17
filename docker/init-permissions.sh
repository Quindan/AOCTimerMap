#!/bin/sh
# Initialize database permissions at container startup

echo "Initializing database permissions..."

# Ensure database directory exists and has correct permissions
mkdir -p /app/database/db /app/backups
chown -R www-data:www-data /app/database /app/backups
chmod -R 755 /app/database /app/backups

# If database file exists, ensure it's writable
if [ -f /app/database/db/mydb.sqlite ]; then
    chown www-data:www-data /app/database/db/mydb.sqlite
    chmod 644 /app/database/db/mydb.sqlite
    echo "Database file permissions updated"
else
    echo "Database file not found - will be created on first API call"
fi

echo "Permissions initialization complete"
