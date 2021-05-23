---
title: Configuration
description: 
published: true
date: 2021-05-23T16:58:24.054Z
tags: 
editor: markdown
dateCreated: 2021-01-28T20:39:13.768Z
---

### What can be configured and what are these configuration options?

The configuration file is located at [invidious/config/config.yml](https://github.com/iv-org/invidious/blob/master/config/config.yml).

- `channel_threads` (default `1`) Number of threads to use for crawling videos from channels

- `feed_threads` (default `1`) Number of threads to use for refreshing subscription feeds

```
db:
  user: kemal # your database user
  password: kemal # your database password
  host: localhost # database host
  port: 5432 # postgres port
```

- `full_refresh` (default `false`) When crawling channel videos, threads should refresh *all* videos uploaded by a channel

- `https_only` (default `false`) Used to tell Invidious it is accessed via https, set to `true` if you have for example a reverse proxy with a ssl certificate

- `hmac_key` (default `nil`) Signing key for CSRF tokens (when `nil` is randomly generated on startup, can be any random string)

- `domain` (default `nil`) Domain to use for providing `self` links in RSS feeds, issuing cookies, etc.

- `use_pubsub_feeds` (default `false`) Use server-side notifications provided by [YouTube](https://developers.google.com/youtube/v3/guides/push_notifications). Requires `domain` and `hmac_key` to be set

- `default_home` (default `"Popular"`) Default home page **Moved into `default_user_preferences`**

- `feed_menu` (default `["Popular", "Trending", "Subscriptions"]`) Order of tabs on feed menu **Moved into `default_user_preferences`**

- `captcha_enabled` (default `true`) Determine if CAPTCHA should be required for registration

- `login_enabled` (default `true`) Whether users should be able to login

- `registration_enabled` (default `true`) Whether new users should be able to register

- `statistics_enabled` (default `false`) Whether statistics should be available from `/api/v1/stats`

- `admins` (default `[]`) List of user IDs that have access to administrator preferences

- `external_port` (default `nil`) Invidious should supply links to a different port (if running behind a proxy, for example). PubSub notifications (if enabled) will also be sent to this port

- `default_user_preferences` (default [`ConfigPreferences`](https://github.com/iv-org/invidious/blob/master/src/invidious/helpers/helpers.cr#L127)) Default preferences to use for new and unregistered users, see [#415](https://github.com/iv-org/invidious/issues/415)

- `dmca_content` (default `[]`) For compliance with DMCA requests, disables download widget for list of video IDs

- `check_tables` (default `false`) Check table integrity, automatically try to add any missing columns, create columns, etc.

- `cache_annotations` (default `false`) Cache annotations requested from IA, will not cache empty annotations or annotations that only contain cards

- `banner` (default `nil`) Optional banner to be displayed along top of page for announcements, etc.

- `hsts` (default `true`) For HTTP Strict Transport Security

- `disable_proxy` (default `false`) Disable proxy option serverwide (options: 'dash', 'livestreams', 'downloads', 'local')

- `force_resolve` (default `nil`) Force IPv4 or IPv6 connection to Google (options: 'ipv4', 'ipv6') see [#811](https://github.com/iv-org/invidious/issues/811)

- `pool_size` (default `100`) Pool size for HTTP connections for youtube.com and ytimg.com (each domain has a separate pool of `pool_size`)

- `admin_email` (default `omarroth@protonmail.com`) Email provided to users for bug reports

- `port` (default `3000`) Default port for HTTP server

- `host_binding` (default `0.0.0.0`) Default host for HTTP server

- `cookies` (default ``) Cookies to be used when connecting to YouTube

- `captcha_key` (default `nil`) [Anti-Captcha](https://anti-captcha.com/) API key for solving YouTube CAPTCHAs, see [#886](https://github.com/iv-org/invidious/issues/886).

- `popular_enabled` (default `false`) Whether to display popular videos of the instance.
