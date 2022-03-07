---
title: Geoblocking,-available-video-quality-and-DASH
description: 
published: true
date: 2021-05-23T16:58:38.141Z
tags: 
editor: markdown
dateCreated: 2021-01-28T20:39:32.300Z
---

## Geoblocking
Sometimes you may notice that you cannot watch a video on Invidious. This is because YouTube is geoblocking, i.e. preventing access to videos based on your geographical location.

If the `Proxy videos?` setting is enabled, Invidious will proxy videos through itself, so the stream will be routed like this:
> YouTube → Invidious/server → Client/browser

If a video is blocked where the instance is hosted, then the route would be this:
> YouTube → Proxy server → Invidious/server → Client/browser

The current system works by cycling through proxies in different regions, and finding one where the video is not blocked.
The reason geoblocked videos may take a long time to load is because Invidious would have to cycle through all known proxy servers until it finds one that is able to play back the video.

If the `Proxy videos?` setting is disabled, then the stream would be routed like this:
> YouTube → Client/browser

## Video quality and DASH
On Invidious you often don't have the same quality options as on YouTube. This is because the audio and video streams are separated and Invidious currently can't sync them together.

DASH is a streaming technique used by YouTube to provide resolutions higher than 720p by providing multiple files for a client to use depending on network and user preferences.

You can enable DASH by selecting the appropriately named video quality in the settings or by appending `&quality=dash` to the end of a video's URL. With this option enabled, the stream is proxied through Invidious for you to then watch at a higher or automatic quality.
