# Make Invidious requests data from YouTube through a VPN using Gluetun (in case your IP is blocked)

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
