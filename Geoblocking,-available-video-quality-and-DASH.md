## Geoblocking
Sometimes you may notice that you cannot watch a video on Invidious. This is because YouTubes geoblocking.

If "Proxy videos?" is enabled, then Invidious will proxy videos through itself, so:  
client/browser --> invidious/server --> youtube

If a video is blocked where the instance is hosted, then it will be:  
client/browser --> invidious/server --> proxy server --> youtube  
The current system works is cycling through proxies in different regions, and finding one where the video is unblocked.  
The reason geo-blocked videos can take a long time to load is if Invidious cannott find a proxy or if none of the regions Invidious tries, return a valid response.

If that option is disabled, then it will look like this:  
client/browser --> youtube


## Video quality and DASH
On Invidious you do often not have the same quality options as on YouTube. This is because the audio and video streams are separated and Invidious cannot sync them together.

DASH is a streaming technique used by YouTube to provide resolutions higher than 1080p. Very simply: it provides multiple files for a client to use depending on network and user preferences.

In the settings you can enable "DASH" as video quality. With this option enabled first of all the stream gets proxied through Invidious and second you can watch in higher quality or use automatic quality.

You can also add `&quality=dash` to the url of your video.