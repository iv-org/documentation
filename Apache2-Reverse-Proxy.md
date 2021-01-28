---
title: Apache2-Reverse-Proxy
description: 
published: true
date: 2021-01-28T21:00:11.405Z
tags: 
editor: undefined
dateCreated: 2021-01-28T20:39:03.772Z
---

This is a very basic config, secured with Let's Encrypt. Any log is disabled by default. Do not forget to replace `ServerName` with your domain.

```
<IfModule mod_ssl.c>
<VirtualHost *:443>
        ServerName invidious.domain.tld
        ServerAdmin admin@localhost

        ProxyPreserveHost On
        ProxyRequests off
        ProxyPass / http://127.0.0.1:3000/
        ProxyPassReverse / http://127.0.0.1:3000/

#        ErrorLog /var/log/apache2/invidious.domain.tld/error.log
        CustomLog /dev/null combined

RewriteEngine on
SSLCertificateFile /etc/letsencrypt/live/invidious.domain.tld/fullchain.pem
SSLCertificateKeyFile /etc/letsencrypt/live/invidious.domain.tld/privkey.pem
SSLCertificateChainFile /etc/letsencrypt/live/invidious.domain.tld/chain.pem

</VirtualHost>
</IfModule>
```