---
title: NGINX-Reverse-Proxy
description: 
published: true
date: 2021-01-28T21:00:53.653Z
tags: 
editor: undefined
dateCreated: 2021-01-28T20:40:07.950Z
---

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

	ssl_certificate /etc/letsencrypt/live/invidious.domain.tld/fullchain.pem;
	ssl_certificate_key /etc/letsencrypt/live/invidious.domain.tld/privkey.pem;

	location / {
		proxy_pass http://127.0.0.1:3000/;
		proxy_set_header X-Forwarded-For $remote_addr;
		proxy_set_header Host $host;	# so Invidious knows domain
		proxy_http_version 1.1;		# to keep alive
		proxy_set_header Connection "";	# to keep alive
	}

	if ($https = '') { return 301 https://$host$request_uri; }	# if not connected to HTTPS, perma-redirect to HTTPS
}
```