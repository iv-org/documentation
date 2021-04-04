---
title: Apache2-Reverse-Proxy
description: 
published: true
date: 2021-02-25T18:04:37.909Z
tags: 
editor: markdown
dateCreated: 2021-01-28T20:39:03.772Z
---

- A very basic config, secured with Let's Encrypt. Any log is disabled by default. Do not forget to replace `ServerName` with your domain.

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

- Another config example without HTTPS, but with Apache Basic Auth HTTP login. 
The user will connect to Apache on port 3333 and will be asked to log in. If authentification is successful, Apache will redirect the user to Invidious' page.
To make the VirtualHost config below actually work, you should as well:
	- Create a [.htpasswd](http://httpd.apache.org/docs/current/programs/htpasswd.html) file and add required [username/login combos](http://aspirine.org/htpasswd_en.html) to it, if not already existing. 
	- Open port 3333 (or any other free port) adding `Listen 3333` to Apache `ports.conf` (Debian `/etc/apache2/ports.conf`) 
	- If you run Invidious with default parameters, you may need to replace default host binding (0.0.0.0) with localhost (127.0.0.1) instead. That way, Invidious won't be publicly available on port 3000 anymore, but only accessible via the reverse proxy on port 3333. So if you run Invidious via a systemd service, you would edit the service file (e.g. `/etc/systemd/system/invidious.service`) and change modify the ExecStart line to include the -b switch as follows `ExecStart=/home/invidious/invidious/invidious -b 127.0.0.1 -o invidious.log` and then reload the daemon with `systemctl daemon-reload` so that changes are taken into account.
	- A convenient way to open such protected Invidious page without having to log in manually everytime is to access use a URL with the following format: http://username:password@domain:3333   

```
<VirtualHost *:3333>

    ServerName invidious.domain.tld #add your own domain name (or localhost if you have no) 
    ServerAdmin admin@localhost

    <Location />
        Deny from all # Forbid access to all by default...
        #Allow from 127.0.0.1 #...Except from specific IPs (which will not need to authentificate)...
	AuthUserFile /etc/apache2/.htpasswd #path to .htpasswd file
	AuthName "Restricted Area" # name displayed in the promptbox
 	AuthType Basic # http://httpd.apache.org/docs/current/howto/auth.html
	Satisfy Any
	Require valid-user # ...and except from authentified users included in the .htpasswd file
    </Location>

    ProxyPass 			/		http://127.0.0.1:3000/ nocanon
    ProxyPassReverse		/		http://127.0.0.1:3000/
    ProxyPreserveHost		On
    ProxyRequests		Off
    AllowEncodedSlashes		On

    #ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog /dev/null combined

</VirtualHost>
```
