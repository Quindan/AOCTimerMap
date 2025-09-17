# AOC Timer Map - Production Dockerfile
FROM php:8.2-fpm-alpine

# Install system dependencies
RUN apk add --no-cache \
    nginx \
    supervisor \
    sqlite \
    python3 \
    curl

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

# Set up PHP-FPM
RUN echo "listen = 127.0.0.1:9000" >> /usr/local/etc/php-fpm.d/www.conf

# Set permissions
RUN chown -R www-data:www-data /app
# Scripts are kept outside container for temporary use

# Create database directory with proper permissions
RUN mkdir -p /app/database && chown www-data:www-data /app/database

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/health || exit 1

# Expose port
EXPOSE 80

# Start supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
