# Make Invidious requests data from YouTube through a VPN using Gluetun (in case your IP is blocked)

This tutorial has been written by [TheFrenchGhosty](https://github.com/TheFrenchGhosty). He is better suited when looking for help about this tutorial.

## Create the docker network (must be done outside of the compose file):

```
docker network create --subnet=172.80.0.0/16 gluetun_network
```

Note: We're not using the Gluetun default of 172.18.0.0/16, because it might already be used which causes Gluetun to not start with the error `Error response from daemon: invalid pool request: Pool overlaps with other one on this address space`, if you have this issue with 172.80.0.0/16 just use a number higher than "80" (at the second byte) and apply the rest of the documentation accordingly


## Create the compose file for Gluetun

- Global setup: https://github.com/qdm12/gluetun-wiki/tree/main/setup

- Provider setup: https://github.com/qdm12/gluetun-wiki/tree/main/setup/providers

```
services:
  gluetun:
    image: ghcr.io/qdm12/gluetun
    container_name: gluetun
    cap_add:
      - NET_ADMIN
    devices:
      - /dev/net/tun:/dev/net/tun
    ports:
#      - 8888:8888/tcp # HTTP proxy # Useless
#      - 8388:8388/tcp # Shadowsocks # Useless
#      - 8388:8388/udp # Shadowsocks # Useless
      - "127.0.0.1:3000:3000" # Invidious (use the Invidious ports configuration)
    volumes:
      - /docker/gluetun/data:/gluetun
    environment:
      - VPN_SERVICE_PROVIDER=<REDACTED>
      - VPN_TYPE=openvpn # Use openvpn or wireguard
      - OPENVPN_USER=<REDACTED>
      - OPENVPN_PASSWORD=<REDACTED>
      - SERVER_COUNTRIES=Germany # Use your server location
      - UPDATER_PERIOD=24h
      - TZ=Europe/Paris # Use your timezone
    networks:
      gluetun_network:

networks:
  gluetun_network:
    external: true
```

## Make Invidious use gluetun


Add this to your DB:

```
    networks:
      gluetun_network:
        ipv4_address: 172.80.0.22
```

Add this to the end of your compose (to make the Invidious-Postgres stack connect to gluetun):

```
networks:
  gluetun_network:
    external: true
```


Add this to the Invidious container:

```
    network_mode: "container:gluetun"
```

Comment out the "- ports:" of the Invidious container (gluetun replaces it, reason why we configured it with the same value)


Update the Invidious config to use the new database address (since the network is "different", using the hostname wont work):

```
      INVIDIOUS_CONFIG: |
        db:
          dbname: invidious
          user: kemal
          password: <REDACTED>
          host: 172.80.0.22
          port: 5432
```

## Tell Gluetun to change IP daily (optional but recommended)

**Don't forget to replace `/path/to/` with a proper path**

- Control server documentation https://github.com/qdm12/gluetun-wiki/blob/main/setup/advanced/control-server.md

Start by exposing the Gluetun control server internally (DO NOT EXPOSE IT EXTERNALLY, KEEP `127.0.0.1`), add this port mapping to Gluetun:

```
    ports:
      - 127.0.0.1:8000:8000/tcp # Control server
```


Write a script named `restartvpn.sh` and add this content to it:

! Remember to replace /path/to/ with the path you want the log to go (either the script location, or `/var/log/`) !

Note: `2>&1` sent STDERR to STDOUT, `tee /path/to/restartvpn.log` will write the output of the script to /path/to/restartvpn.log (in the current directory) (while still printing it to the shell)

```bash
#!/usr/bin/env bash

echo "BEGIN $(date --rfc-3339=seconds)" 2>&1 | tee /path/to/restartvpn.log

curl -X GET "http://127.0.0.1:8000/v1/publicip/ip" 2>&1 | tee /path/to/restartvpn.log # Print the original IP

curl -X PUT -H "Content-Type: application/json" -d '{"status":"stopped"}' "http://127.0.0.1:8000/v1/openvpn/status" 2>&1 | tee /path/to/restartvpn.log # Stop OpenVPN

sleep 5

curl -X PUT -H "Content-Type: application/json" -d '{"status":"running"}' "http://127.0.0.1:8000/v1/openvpn/status" 2>&1 | tee /path/to/restartvpn.log # Start OpenVPN (changing the server it's connecting to)

sleep 5

curl -X GET "http://127.0.0.1:8000/v1/openvpn/status" 2>&1 | tee /path/to/restartvpn.log # Print the Gluetun status

curl -X GET "http://127.0.0.1:8000/v1/publicip/ip" 2>&1 | tee /path/to/restartvpn.log # Print the new IP

echo "END $(date --rfc-3339=seconds)" 2>&1 | tee /path/to/restartvpn.log
```


Run this daily using cron

Run `crontab -e` and add a new cronjob:

```
@daily /path/to/restartvpn.sh
```
