# Dockerfile
FROM php:8.2-fpm

# 1) Install needed packages: Nginx, Supervisor, plus SQLite libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    supervisor \
    libsqlite3-dev \
    sqlite3 \
 && rm -rf /var/lib/apt/lists/*

# 2) Enable pdo_sqlite in PHP (requires libsqlite3-dev)
RUN docker-php-ext-install pdo pdo_sqlite

# 3) Remove the default Nginx site and copy in your custom config
RUN rm /etc/nginx/sites-enabled/default
COPY docker/nginx/default.conf /etc/nginx/conf.d/default.conf

# 4) Copy Supervisor config
COPY docker/supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# 5) Expose port 80 for Nginx
EXPOSE 80

# 6) Use Supervisor to run both PHP-FPM & Nginx
CMD ["supervisord", "-n", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

