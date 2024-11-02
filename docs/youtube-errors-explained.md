# All the YouTube error messages explained with solutions

**DISCLAIMER**: If you are just an user of a public instance. This documentation is not for you. Please instead redirect your Invidious instance maintainer to this page or switch to another public instance: [https://instances.invidious.io](https://instances.invidious.io)

## Error: non 200 status code. Youtube API returned status code 429

### Error explained

YouTube is limiting the traffic that you can sent to their servers. This error may appear for a duration of 24 hours.

### Cause(s)

Usually it is related to a lot of traffic being generated for refreshing your subscriptions.

- You have modified the parameter `channel_refresh_interval` and thus you are forcing the refresh of your subscriptions too quickly for YouTube.
- You are subscribed to a lot of channels. YouTube may classify this as abuse due to Invidious having to check for new videos on a lot of channels.
- You have sent a lot of traffic in another manner. Like by using the Invidious API.
- Someone on your network is sending a lot of traffic to YouTube.

### Solution(s)

- Try to keep the `channel_refresh_interval` parameter commented to let Invidious refreshing your subscriptions less frequently.
- Unsubscribe from some channels. While this may not be ideal, this will definitively send less data to YouTube.
- Configure pubsub: [/installation/#post-install-configuration](./installation.md/#post-install-configuration). This requires your Invidious to be available on the internet and through a public domain.  
   After this you can try to extend the refresh interval, like to `channel_refresh_interval: 240m`.  
   You will still get almost instantaneous notifications from new YouTube videos thanks to pubsub but you will induce less refreshing traffic to YouTube servers. As pubsub is method for YouTube to notify your Invidious instance for new videos.
- Change your public IP address. This may not solve the issue permanently but temporarily solve it.

## Sign in to confirm you are not a bot - This helps protect our community

### Error explained

YouTube is blocking the communication of Invidious to their servers.

### Cause(s)

- YouTube is running different mechanisms to detect the usage of non official YouTube clients. Your Invidious instance may have been detected by their system.
- Your IP address is blacklisted from YouTube servers. It is known that YouTube block datacenter IP addresses.

### Solution(s)

First make sure that you are running the latest version of Invidious and you are using Invidious companion. Please see [the updated installation guide](./installation.md).

After which you can try these solutions:

- Change your public IP address. Reboot your router or by configuring a proxy on Invidious companion: https://github.com/iv-org/invidious-companion/blob/be1f4bee39f4d01fe83c65855538dbaacbf6d0c0/config/default.toml#L14
- Configuring a YouTube account by enabling `oauth_enabled` in Invidious companion: https://github.com/iv-org/invidious-companion/blob/be1f4bee39f4d01fe83c65855538dbaacbf6d0c0/config/default.toml#L23.  
   **WARNING**: YouTube is known to ban accounts being used on non official YouTube clients, you have been warned. Do not use a personal account.
- If you have IPv6 on the computer hosting Invidious, you can try to rotate your IPv6 public address, tutorial available here: "[Rotate your IPv6 address for escaping YouTube blocking](/ipv6-rotator/)"

All of these options do not guarantee you to bring back Invidious to working conditions. These are just advices for trying to unblock your Invidious instance from YouTube. Make sure to always specify any modification being done to your Invidious when reporting issues.

## Videoplayback URLs that returns 403 HTTP errors

### Error explained

YouTube is forbidding you from viewing/downloading videos from their "googlevideo.com" server. Other functions such as viewing channels pages may still work.

### Cause(s)

This error has different root causes:

- You are loading a video stream that is restricted to the IP address that generated that URL. For example this can happen on music videos or copyright content.
- You or someone on your network have downloaded a lot of videos. Your IP address has been blocked from YouTube servers.

### Solution(s)

First make sure that you are running the latest version of Invidious and you are using inv_sig_helper. Please see [the updated installation guide](./installation.md).

After which you can try these solutions:

- Change your public IP address. Reboot your router or by configuring a proxy in Invidious: https://github.com/iv-org/invidious/blob/2150264d849771df8f15bab172ab6d87eeb80c55/config/config.example.yml#L176-L185
- If you have IPv6 on the computer hosting Invidious, you can try to rotate your IPv6 public address, tutorial available here: "[Rotate your IPv6 address for escaping YouTube blocking](./ipv6-rotator.md)"
- If it's a music video or a copyright content, then try to make sure that the video is loaded from the same IP that generated the video URL.

