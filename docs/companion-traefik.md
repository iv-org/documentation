# Traefik reverse proxy setup with Invidious companion

This is a very basic config, assuming that you're using Traefik to manage SSL certificates for you, and Traefik is on the same server as the Invidious and companion container.
Do not forget to replace `<server_name>` with your domain.

**Invidious Setup**
```
...
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.invidious.rule=Host(`<server_name>`) && !(Path(`/latest_version`) || PathPrefix(`/api/manifest/dash/id/`) || PathPrefix(`/videoplayback`))"
      - "traefik.http.routers.invidious.entrypoints=web-sec"
      - "traefik.http.routers.invidious.tls.certresolver=le"
      - "traefik.http.services.invidious.loadbalancer.server.port=3000"
...
```
**Companion Setup**
```
...
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.invidious-companion.rule=Host(`<server_name>`) && (Path(`/latest_version`) || PathPrefix(`/api/manifest/dash/id/`) || PathPrefix(`/videoplayback`))"
      - "traefik.http.routers.invidious-companion.entrypoints=web-sec"
      - "traefik.http.routers.invidious-companion.tls.certresolver=le"
      - "traefik.http.services.invidious-companion.loadbalancer.server.port=8282"
...
```
