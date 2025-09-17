# AOC Timer Map - Production Dockerfile
FROM php:8.2-fpm-alpine

# Install system dependencies
RUN apk add --no-cache \
    nginx \
    supervisor \
    sqlite \
    python3 \
    curl \
    shadow

# Fix www-data UID/GID to match host (33:33 instead of 82:82)
RUN deluser www-data && \
    addgroup -g 33 www-data && \
    adduser -D -u 33 -G www-data www-data

# Create application directories
WORKDIR /app
RUN mkdir -p /app/{frontend,api,database,backups} \
    /var/log/supervisor \
    /run/nginx

# Copy application files
COPY app/frontend-built/ /app/frontend/
COPY app/api/ /app/api/
COPY docker/nginx.conf /etc/nginx/nginx.conf
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY docker/init-permissions.sh /usr/local/bin/init-permissions.sh

# Set up PHP-FPM
RUN echo "listen = 127.0.0.1:9000" >> /usr/local/etc/php-fpm.d/www.conf

# Set permissions for app directories
RUN chown -R www-data:www-data /app/frontend /app/api

# Create database directory structure (will be mounted as volume)
RUN mkdir -p /app/database/db /app/backups && \
    chown -R www-data:www-data /app/database /app/backups && \
    chmod -R 755 /app/database /app/backups

# Make init script executable
RUN chmod +x /usr/local/bin/init-permissions.sh

# Scripts are kept outside container for temporary use

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/health || exit 1

# Expose port
EXPOSE 80

# Start supervisord directly (permissions handled by init script in supervisord)
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
