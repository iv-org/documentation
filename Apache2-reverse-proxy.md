---
title: Apache2-reverse-proxy
description: 
published: true
date: 2021-11-17T16:59:09.054Z
tags: 
editor: markdown
dateCreated: 2021-11-17T20:40:07.950Z
---

This is the barebones SSL and non-SSL configs for Apache 2.2 and up. You will need to use Let's Encrypt to generate a certificate. Replace `your-domain` with your website. Logs are not recorded by default.

```
<VirtualHost *:80>
        ServerAdmin webmaster@localhost
        ServerAlias your-domain

        ProxyPass / http://0.0.0.0:3000/
        ProxyPassReverse / http://0.0.0.0:3000/
RemoteIPHeader CF-Connecting-IP
        ErrorLog /dev/null
        CustomLog /dev/null
RewriteEngine on
RewriteCond %{SERVER_NAME} =your-domain
RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]
</VirtualHost>

<VirtualHost *:443>
        ServerAdmin webmaster@localhost
        ServerAlias your-domain

        ErrorDocument 503 "Invidious is unavailable at this time."
        ProxyPass / http://0.0.0.0:3000/
        ProxyPassReverse / http://0.0.0.0:3000/

        ErrorLog /dev/null
        CustomLog /dev/null

#RemoteIPHeader CF-Connecting-IP

Include /etc/letsencrypt/options-ssl-apache.conf
ServerName your-domain
SSLCertificateFile /etc/letsencrypt/live/your-domain/fullchain.pem
SSLCertificateKeyFile /etc/letsencrypt/live/your-domain/privkey.pem
</VirtualHost>
</IfModule>
```
