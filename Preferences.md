Preferences for Invidious can be stored in a cookie named `PREFS`.  This cookie can be set on the Invidious Preferences page.

If setting the cookie value yourself, the value must be in JSON format and then URL-encoded.

These are the preferences you can set:

```
{
   "video_loop":false, // Always loop?
   "autoplay":false,
   "continue":false,   // Autoplay next video
   "listen":false,     // Audio-only mode by default?
   "speed":1.0,        // Also accepts '0.5', '1.5', '2.0'
   "quality":"hd720",  // Also accepts 'dash' for 1080p, 'medium', 'small'
   "volume":100,
   "comments":[
      "youtube",
      ""               // Also accepts 'reddit'
   ],
   "captions":[        // Language captions in order of preference?
      "",
      "",
      ""
   ],
   "related_videos":true,
   "redirect_feed":false,
   "locale":"en-US",
   "dark_mode":false,
   "thin_mode":false,
   "max_results":40,
   "sort":"published",
   "latest_only":false,
   "unseen_only":false,
   "notifications_only":false
}
```
