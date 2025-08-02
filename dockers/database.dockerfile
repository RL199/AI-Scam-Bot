FROM mysql:9.0

# Set non-sensitive default values
ENV MYSQL_DATABASE=scambot_db
ENV MYSQL_USER=scambot_user

# Copy initialization scripts
COPY database/init.sql /docker-entrypoint-initdb.d/

# Expose MySQL port
EXPOSE 3306

# Set MySQL configuration
RUN echo '[mysqld]' > /etc/mysql/conf.d/custom.cnf && \
    echo 'max_connections=500' >> /etc/mysql/conf.d/custom.cnf && \
    echo 'innodb_buffer_pool_size=256M' >> /etc/mysql/conf.d/custom.cnf
