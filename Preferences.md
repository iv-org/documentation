Preferences for Invidious can be stored in a cookie named `PREFS`.  This cookie can be set on the Invidious Preferences page.

If setting the cookie value yourself, the value must be in JSON format and then URL-encoded.

These are the preferences you can set:
```
{
   "video_loop":true,             // Always loop
   "annotations":true,            // Show annotations
   "annotations_subscribed":true, // Show annotations for subscribed channels
   "autoplay":true,               // Autoplay current video
   "continue":true,               // Load next video when current video finishes
   "continue_autoplay":true,      // Load and autoplay next video
   "listen":true,                 // Audio-only mode by default
   "local": true,                 // Proxy requests via Invidious instance for privacy
   "speed":1.0,                   // Also accepts '0.5', '1.5', '2.0'
   "quality":"hd720",             // Also accepts 'dash' for 1080p, 'medium', 'small'
   "volume":100,                  // Audio Volume by default (0 = Min, 100 = Max)
   "comments":[                   // Choose which source to use for the comments; 'youtube' or 'reddit'
      "youtube",
      ""
   ],
   "captions":[                   // Language captions in order of preference
      "",
      "",
      ""
   ],
   "related_videos":true,         // Show related videos
   "redirect_feed":true,          // Redirect homepage to subscription feed
   "locale":"en-US",              // Choose interface language
   "dark_mode":true,              // Use dark mode
   "thin_mode":true,              // Don't include pictures in page load

   // For registered users (currently unused):
   "max_results":40,
   "sort":"published",
   "latest_only":false,
   "unseen_only":false,
   "notifications_only":false
}
```
