# Hide Invidious instance behind proxy server (for escaping DMCA requests)

This tutorial has been writen by [unixfox](https://github.com/unixfox), owner of [yewtu.be](https://yewtu.be/)

## Synopsis

This tutorial will explain how to hide your Invidious (public) instance behind another server, useful for escaping the DMCA requests.

This proxy server will only redirect the [TCP](https://en.wikipedia.org/wiki/Transmission_Control_Protocol) connections, allowing you to keep everything from your existing infrastructure.

??? note "It's possible to do it by forwarding the HTTP connections directly but..."

    By forwarding the actual HTTP protocol this is more compute intensive and won't be covered in this tutorial.

    You need to proxy the HTTP protocol normally like you would already do with your current web server for invidious. But in this case from the proxy server to your existing infrastructure. Then also setup the certificates for HTTPS.

    Then you optionally preserve the IP address of your clients using for example on NGINX set_real_ip_from and real_ip_header.

## Warning

Adding an extra layer like a proxy server **will** add more latency, thus increase the response time from your final server to your browser. That's why for the part where you are going to rent a proxy server, you should choose a server close to your existing server(s).

It should be noted, in the 4th step of the instructions, you will be able to remove this latency for a major part of the users of your instance (around 90% - people using modern browsers). The rest will experience this *added* latency which won't result in a decrease of the user experience if you choose your server wisely.

## Requirements

- Your main web server should support the proxy protocol, it's possible to do it without it (later on in the tutorial). Non-exhaustive list of web servers that support it:  
 
    * NGINX (recommended web server for this tutorial)
    * Traefik
    * Apache ([doesn't come in the official version](https://www.scaleway.com/en/docs/tutorials/proxy-protocol-v2-load-balancer/#configuring-proxy-protocol-in-apache-web-server))
    * Caddy ([need to build with a custom module](https://github.com/mastercactapus/caddy2-proxyprotocol))

- You will have to spend a bit more money per month for renting this new proxy server.

## Instructions

### 1) Renting your proxy server

There are a lot of providers that don't care about DMCA requests, you can find them by doing a search on your favorite search engine.  
Here are some lists compiled from lowendtalk users:

- https://lowendtalk.com/discussion/182615/are-there-any-active-dmca-free-vps-offers-from-top-providers ([webarchive link](https://web.archive.org/web/20221206182503/https://lowendtalk.com/discussion/182615/are-there-any-active-dmca-free-vps-offers-from-top-providers))
- https://lowendtalk.com/discussion/181443/options-for-dmca-free-vps ([webarchive link](https://web.archive.org/web/20221007000624/https://lowendtalk.com/discussion/181443/options-for-dmca-free-vps))
- https://lowendtalk.com/discussion/179472/what-are-my-options-for-a-dmca-free-vps ([webarchive link](https://web.archive.org/web/20230217184607/https://lowendtalk.com/discussion/179472/what-are-my-options-for-a-dmca-free-vps))

I personally chose [BuyVM](https://buyvm.net) as it's close to my existing infrastructure and it's cheap, but please try to at least find another one, it's much better to avoid the centralisation.

Here are the recommended requirements for this proxy server:

- At least 256MB of RAM in total if you are running Debian or 512MB with Ubuntu.
- The **outgoing** bandwidth limit/quota should be the same as the **outgoing** bandwidth consumption of your existing server that run Invidious.  
  Later in the tutorial I'll explain you how to reduce the bandwidth consumption on the proxy server but this won't drastically reduce it by a lot.  
  TL;DR: If you have "unlimited" bandwidth limit it's much better.
- 1 CPU core.
- The proxy server should be close to your existing server(s), for minimal latency overhead.

??? note "You can monitor the bandwidth usage of your servers using vnStat."

    Documentation: https://wiki.archlinux.org/title/vnStat  
    Column `rx`: receive or incoming bandwidth  
    Column `tx`: Transfer or outgoing bandwidth  

    1. Install vnStat from your package manager, example on debian/ubuntu: `apt install vnstat`
    2. Start vnStat: `systemctl enable --now vnstat`
    3. In a few hours execute the command `vnstat`

If you run into performance issue on the proxy server, feel free to switch to a new provider.

And if you need help in choosing the ideal server, please seek for help on our [Matrix room](https://matrix.to/#/#invidious:matrix.org) or [IRC channel](https://web.libera.chat/?channel=#invidious).

### 2) Listen to new ports on your web server of your existing infrastructure

**On the web server of your existing infrastructure/server** that currently host your Invidious, listen on another port with the proxy protocol enabled for the HTTPS/TLS port.

In this tutorial I'll use the port 8443, but you can choose any port you would want.  
You don't need to setup a new port for the HTTP (cleartext) port as the proxy protocol is only for preserving the IP address of the clients that will connect your web server and nowadays all the requests are permanently redirected to HTTPS.

??? note "If you don't want to preserve the IP address of the users of your instance."

    Meaning keeping your instance truly 100% anonymous, then you don't need to enable the proxy protocol on another port, you can keep your current configuration without touching anything and jump to the 3rd step.  
    
    But preserving the IP address is in my opinion essential for blocking bots, bad actors.

#### NGINX

In the NGINX configuration file for Invidious, just after the line `listen 443 ssl http2` add this line:
```
listen 8443 ssl http2 proxy_protocol;
set_real_ip_from PUBLIC_IPV4_ADDRESS_OF_ORIGINAL_SERVER/32;
real_ip_header proxy_protocol;
```

Very simple example of a final result:
```
http {
    server {
        listen 443 ssl http2;
        listen 8443 ssl http2 proxy_protocol;
        set_real_ip_from PUBLIC_IPV4_ADDRESS_OF_ORIGINAL_SERVER/32;
        real_ip_header proxy_protocol;
    }
}
```

Note: You may not have `http2` parameter for the `listen 443 ssl` line, if you don't have it enabled, it's hugely recommended to enable it for better performance and user experience.

**If you are going to follow the [4th step](#4-optionally-reduce-the-traffic-going-through-the-proxy-server), please remove `http2` parameter from the line `listen 8443 ssl http2 proxy_protocol`, it may clash with the technique.**

#### Traefik

CLI parameters, adapt to your platform (docker compose, kubernetes or local traefik):
```
--entryPoints.websecure.address=:8443
--entryPoints.websecure.proxyProtocol.trustedIPs=PUBLIC_IPV4_ADDRESS_OF_ORIGINAL_SERVER/32
```

Please see the documentation: https://doc.traefik.io/traefik/routing/entrypoints/#proxyprotocol

For people on Kubernetes, this may help you: https://github.com/traefik/traefik-helm-chart/issues/404

#### Caddy

(Not tested) On caddy it is not possible to listen on a port that support proxy protocol and another port without the proxy protocol, thus you won't be able to follow the step 4.  
Or you can follow the step 4 but you need to not use the proxy protocol (not touching your configuration), thus losing the ability to preserve the IP address of the clients.

1. Compile caddy with this module: https://github.com/mastercactapus/caddy2-proxyprotocol
2. Enable the proxy protocol like so: https://github.com/mastercactapus/caddy2-proxyprotocol#caddyfile

#### Apache

Apache is not the ideal web server for using proxy protocol because it's still in alpha stage and you need to compile apache using an external module like explained here: https://www.scaleway.com/en/docs/tutorials/proxy-protocol-v2-load-balancer/#configuring-proxy-protocol-in-apache-web-server

Either you do that or you don't preserve the IP address of the clients by not touching your configuration but I can't help you more.

#### Other web servers

I won't cover all the possible web servers, look at the documentation of your web server and make it listen on port 8443 (or another port) with the proxy protocol enabled on it. Also try to find a way to preserve the IP address if needed.

You can also not touch anything about your web server configuration and follow the note in the 3rd step.

### 3) Install HAProxy on the proxy server

**On the proxy server that you just rented.**

1. Install haproxy from your package manager, on debian/ubuntu: `apt install haproxy`.
2. Edit the file `/etc/haproxy/haproxy.cfg` and replace it with this configuration:
 
    ```
    global
        log /dev/null    local0 info alert
        log /dev/null    local1 notice alert
        chroot /var/lib/haproxy
        stats socket /run/haproxy/admin.sock mode 660 level admin
        stats timeout 30s
        user haproxy
        group haproxy
        daemon

    defaults
        log	global
        mode	http

    frontend https
        bind :::443 v4v6
        mode tcp
        use_backend https

    backend https
        balance roundrobin
        mode tcp
        server server1 PUBLIC_IPV4_ADDRESS_OF_ORIGINAL_SERVER:8443 check send-proxy

    frontend http
        bind :::80 v4v6
        mode tcp
        use_backend http

    backend http
        balance roundrobin
        mode tcp
        server server1 PUBLIC_IPV4_ADDRESS_OF_ORIGINAL_SERVER:80 check
    ```

    **If you didn't enable the proxy protocol on your server** then remove `send-proxy` for the backend `https` and replace the port `8443` with `443`.

    In case you have more servers, add the other servers after the two lines `server server1` with their corresponding IP addresses.

    For caddy if you have enabled the proxy protocol you need to also add `send-proxy` for the backend `http`.

4. Restart HAProxy using `systemctl restart haproxy`.

5. Test if your setup is working by either temporarily update your local Hosts file to the IP address of your proxy server.
    Or you can use curl for that:
    ```
    curl https://yourdomain.com/ --resolve yourdomain.com:443:PUBLIC_IPV4_ADDRESS_OF_PROXY_SERVER
    ```

6. If everything works well, you can now update the DNS entries of the domain for your Invidious instance to the IPv4 (and IPv6) address of your proxy server.

### 4) Optionally reduce the traffic going through the proxy server

There is a technique in the HTTP protocol that allow to redirect a client (e.g. a browser) to another server, it's the Alt-Svc header: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Alt-Svc.

Unfortunately it only works for Firefox browsers as Chrome doesn't support the ability to use a different domain on HTTP2 with Alt-Svc but it does support it for HTTP3 which you can later on enable too with Alt-Svc.

*I'll use the terminology `original server(s)` for the server(s) of your existing infrastructure, not the proxy server.*

#### Requirement
You need to have HTTP2 enabled on your web server, on NGINX it's as simple as adding `http2` in the `listen ssl` line.  
You can check that in your config or here: https://tools.keycdn.com/http2-test

#### Instructions

1. Go to your instance and press F12 for the dev tools, then go to the "Network" tab and click on the latest request.  
    Then check in `Remote Address` (Chrome) or `Address` (Firefox you need to click on `>`) if you see the IP address of your proxy server.
2. Add a new DNS record for the IPv4 (and IPv6) of your original server(s) to a subdomain, like `original.yourdomain.com`.
3. In your existing web server add this new HTTP header:
    ```
    alt-svc: h2="original.yourdomain.com:443"; ma=86400
    ```
    Here is how to do it for:
    - NGINX: `add_header alt-svc 'h2="original.yourdomain.com:443"; ma=86400';`
    - Traefik (or [read the doc](https://doc.traefik.io/traefik/middlewares/http/headers/)): `traefik.http.middlewares.altsvc.headers.customresponseheaders.alt-svc=h2="original.yourdomain.com:443"; ma=86400`
    - Caddy: `header alt-svc h2="original.yourdomain.com:443"; ma=86400`
    - Apache: `Header set alt-svc 'h2="original.yourdomain.com:443"; ma=86400'`
4. Restart your web server
5. Go to your instance and press F12 for the dev tools, then go to the "Network" tab and click on the latest request.  
    Then check in `Remote Address` (Chrome) or `Address` (Firefox you need to click on `>`) if you see the IP address of your original server(s).   
    You may need to refresh the page.


#### Bonus point if you have HTTP3 on your web server

Different web servers that support HTTP3:

- Traefik, you can enable HTTP3: https://doc.traefik.io/traefik/routing/entrypoints/#http3
- NGINX, there is a tutorial here: https://www.nginx.com/blog/binary-packages-for-preview-nginx-quic-http3-implementation/
- Caddy, it's already enabled by default

1. Edit the previously added HTTP header by adapting it like this:
    ```
    alt-svc: h3="original.yourdomain.com:443"; ma=86400, h2="original.yourdomain.com:443"; ma=86400
    ```
2. Restart your web server. Check in the dev tools if you still see the IP address of your original server(s) and the HTTP3 protocol should be also displayed.
