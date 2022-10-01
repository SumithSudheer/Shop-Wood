[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/project/Shop-Wood
ExecStart=/home/ubuntu/project/env/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          project1.wsgi:application

[Install]
WantedBy=multi-user.target




server {
    listen 80;
    server_name 35.78.76.79;

    location = /favicon.ico { access_log off; log_not_found off; }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}


user = User.objects.create_superuser(email='sumithsudheer66@gmail.com',password='sumith', phone='9567238587',name='sumith')