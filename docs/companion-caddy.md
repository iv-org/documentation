# Caddy reverse proxy setup with Invidious companion

This is a very basic config, assuming that you're using Caddy to manage SSL certificates for you.
Any log is disabled by default. Do not forget to replace `server_name` with your domain.

```
https://<server_name> {

  @companion {
		path /latest_version
		path /api/manifest/dash/id/*
		path /videoplayback*
		path /download*
	}

  reverse_proxy @companion localhost:8282
  reverse_proxy localhost:3000

  log {
      output discard
  }
}
```
