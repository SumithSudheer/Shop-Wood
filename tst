[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/Shop-Wood
ExecStart=/home/ubuntu/Shop-Wood/env/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          project1.wsgi:application

[Install]
WantedBy=multi-user.target




server {
    listen 80;
    server_name 54.168.104.151, shopwood.online, www.shopwood.online;

    location = /favicon.ico { access_log off; log_not_found off; }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}

CREATE USER admin WITH PASSWORD 'admin';

ALTER ROLE admin SET client_encoding TO 'utf8';
ALTER ROLE admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE admin SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE project TO admin;


user = User.objects.create_superuser(email='sumithsudheer66@gmail.com',password='sumith', phone='9567238587',name='sumith')


