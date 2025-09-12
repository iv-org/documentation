# Caddy reverse proxy setup with Invidious companion direct traffic

This is a very basic config, assuming that you're using Caddy to manage SSL certificates for you.
Any log is disabled by default. Do not forget to replace `server_name` with your domain.

```
https://<server_name> {

  reverse_proxy /companion localhost:8282
  reverse_proxy localhost:3000

  log {
      output discard
  }
}
```
