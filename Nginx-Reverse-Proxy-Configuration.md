# This first block redirects non-HTTPS traffic to secure port 443. Optional, but recommended.
server {
    listen 80;
    listen [::]:80;
    server_name invidious.domain.tld;

    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name invidious.domain.tld;

    ssl_certificate /etc/letsencrypt/live/invidious.domain.tld/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/invidious.domain.tld/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:3000/;
        proxy_set_header   Host                $host;
        proxy_set_header   X-Real-IP           $remote_addr;
        proxy_set_header   X-Forwarded-For     $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto   $scheme;
    }
}