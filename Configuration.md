### What can be configured and what are these configuration options?

The configuration file is located at [invidious/config/config.yml](https://github.com/omarroth/invidious/blob/master/config/config.yml).

`video_threads (default 0)` Number of threads to use for updating videos in cache (mostly non-functional)  
`crawl_threads (default 0)` Number of threads to use for finding new videos from YouTube (used to populate "top" page)  
`channel_threads (default 1)` Number of threads to use for crawling videos from channels (for updating subscriptions)  
`feed_threads (default 1)` Number of threads to use for updating feeds (RSS Feeds)  

```
db:
  user: kemal # your database user
  password: kemal # your database password
  host: localhost # database host
  port: 5432 # postgres port
```

`full_refresh (default false)` Used for crawling channels: threads should check all videos uploaded by a channel  
`https_only (default false)` Used to tell Invidious it is accessed via https, set to `true` if you have for example a reverse proxy with a ssl certificate  
`domain` You should specify the domain you publish your Invidious instance here