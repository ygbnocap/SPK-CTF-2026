FROM php:8.3-apache
COPY index.php /var/www/html/index.php
COPY flag.txt /flag.txt
RUN mkdir -p /var/www/html/uploads && chown -R www-data:www-data /var/www/html/uploads
