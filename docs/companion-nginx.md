# NGINX reverse proxy setup with Invidious companion direct traffic

This is a very basic config, secured with Let's Encrypt. Any log is disabled by default. Do not forget to replace `server_name` with your domain.

```
server {
    listen 80;
    listen [::]:80;
    listen 443 ssl http2;
    listen [::]:443 ssl http2;

    server_name invidious.domain.tld;

    access_log off;
    error_log /var/log/nginx/error.log crit;

    ssl_certificate     /etc/letsencrypt/live/invidious.domain.tld/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/invidious.domain.tld/privkey.pem;

    # Redirect all HTTP requests to HTTPS
    if ($scheme = http) {
        return 301 https://$host$request_uri;
    }

    proxy_set_header X-Forwarded-For $remote_addr;
    proxy_set_header Host $host;
    proxy_http_version 1.1;
    proxy_set_header Connection "";

    # Invidious main service
    location / {
        proxy_pass http://127.0.0.1:3000;
    }

    # Invidious companion service
    location /companion {
        proxy_pass http://127.0.0.1:8282;
    }
}
```
