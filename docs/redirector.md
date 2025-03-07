# Redirector setup

# What is Redirector?

Redirector is a Browser extension for Firefox and Chromium that can manually be configured to redirect links, such as YouTube to Invidious or [Twitter to Nitter](https://github.com/zedeus/nitter/wiki/Extensions#redirector)

Get Redirector: [Firefox](https://addons.mozilla.org/en-US/firefox/addon/redirector/) — [Chromium-based](https://chrome.google.com/webstore/detail/redirector/ocgpenflpmgnfapjedencafcfakcekcd) — [GitHub](https://github.com/einaregilsson/Redirector)

All of these rules are made with Wildcard Processing. 

# How to use it for Invidious Redirects?

For basic redirects, you will need the following rules set up.

# Rule 1 (Redirect Video URLs)

Redirect ```https://*youtube.com/watch?*v=*```
 to: ```https://[Invidious Domain Here]/watch?$2v=$3```
 Example: ```https://www.youtube.com/watch?v=Lz13cxZNTCo``` → https://[Invidious Domain Here]/watch?v=Lz13cxZNTCo
 Applies to: Main window (address bar)

# Rule 2 (Redirects the youtu.be domain, typically accociated with URLs generated by the "Share" button)

Redirect: ```https://youtu.be/*```
to: ```https://[Invidious Domain Here]/watch?v=$1```
Example: ```https://youtu.be/Ae5yV4p7uh8?t=35``` → https://[Invidious Domain Here]/watch?v=Ae5yV4p7uh8?t=35
Applies to: Main window (address bar)

# Rule 3 (Redirects Search Results, useful for those who use DDG bangs or search extensions to search YouTube and would like those properly redirected to Invidious)

Redirect: ```https://www.youtube.com/results?search_query=*&page```
to: ```https://[Invidious Domain Here]/search?q=$1```
Example: ```https://www.youtube.com/results?search_query=Smash+Bros+Trailer&page``` → https://[Invidious Domain Here]/search?q=Smash+Bros+Trailer
Applies to: Main window (address bar)


# Rule 4 (Redirects the YouTube Domain itself, IE: channel pages and the homepage)

Redirect: ```https://*.youtube.com/*```
to: ```https://[Invidious Domain Here]/$2```
Example: ```https://www.youtube.com/channel/UCOkL7q2SeGZeZuj22njMYEA``` → https://[Invidious Domain Here]/channel/UCOkL7q2SeGZeZuj22njMYEA
Applies to: Main window (address bar)

# How to use it for Invidious URL Parameters?

If you would like to use URL Parameters in your redirects (see [here](https://github.com/cloudrac3r/invidious-documentation/blob/master/List-of-URL-parameters.md)), you will need to manually add them to the preceding rules (https://[Invidious Domain Here]/watch?v=$1[URL Parameters here] in place of https://[Invidious Domain Here]/watch?v=$1).

For clarity, an example of a URL parameter would be &related_videos=false&comments=false to ensure that neither related videos nor comments are displayed on a video page, so ```https://[Invidious Domain Here]/watch?v=$1&related_videos=false&comments=false``` would be the destination of redirects.

For redirects with ? in the URL, the Parameter string will start with &, while redirects without ? in the URL should have a Parameter string begining with ?, so https://[Invidious Domain Here]/$2 becomes ```https://[Invidious Domain Here]/$2?related_videos=false&comments=false```

Should you choose to use URL Parameters, I would reccomend adding the following rules to both ensure all Invidious videos load with your preference, and to ensure that unnecesary parameters are not added when already applied. 

# Rule 5 (Redirects Invidious Video URLs with parameters)

Redirect: ```https://[Invidious Domain Here]/watch?v=*```
to: ```https://[Invidious Domain Here]/watch?v=$1[URL Parameters here]```
excluding: ```https://[Invidious Domain Here]/watch?v=*[URL Parameters here]```
Example: ```https://[Invidious Domain Here]/watch?v=Lz13cxZNTCo``` → https://[Invidious Domain Here]/watch?v=Lz13cxZNTCo[URL Parameters here]
Applies to: Main window (address bar)

# Rule 6 (Redirects Invidious Domain URLs with parameters)

Redirect: ```https://[Invidious Domain Here]/*```
to: ```https://[Invidious Domain Here]/$1[URL Parameters here]```
excluding: ```https://[Invidious Domain Here]/*[URL Parameters here]```
Example: ```https://[Invidious Domain Here]/``` → https://[Invidious Domain Here]/[URL Parameters here]
Applies to: Main window (address bar)

It is important that you add the exceptions so as not to create infinite repeats of the same URL Parameters when opening multiple Invidious Videos in a single session. When creating or editing rules in Redirector you must access "Advanced Options" in order to set exceptions. 

# How to use it for Redirecting Embeds?

For redirecting embeds, you'll need the following two rules. (Note, it is imparative that you check these two roles apply to both the Main Window and IFrames, otherwise the rule won't apply to Embeds).

# Rule 7 (For redirecting standard embed links)

Redirect: ```https://www.youtube.com/embed/*```
to: ```https://[Invidious Domain Here]/embed/$1```
Example: ```https://www.youtube.com/embed/Lz13cxZNTCo``` → https://[Invidious Domain Here]/embed/Lz13cxZNTCo
Applies to: Main window (address bar), IFrames

# Rule 8 (For redirecting nocookie embeds)

Redirect: ```https://www.youtube-nocookie.com/embed/*```
to: ```https://[Invidious Domain Here]/embed/$1```
Example: ```https://www.youtube-nocookie.com/embed/Lz13cxZNTCo``` → https://[Invidious Domain Here]/embed/Lz13cxZNTCo
Applies to: Main window (address bar), IFrames



# How to use it to redirect Invidious Feeds to YouTube Feeds?

Finally, if you like to subscribe to channels using RSS feeds, the following two rules will redirect Invidious RSS feeds to their YouTube equivelants. This way you'll still have access to your feeds should you need to migrate to another instance. 

# Rule 9 (For redirecting channel feeds)

Redirect: ```https://[Invidious Domain Here]/feed/channel/*```
to: ```https://www.youtube.com/feeds/videos.xml?channel_id=$1```
Example: ```https://[Invidious Domain Here]/feed/channel/UCOkL7q2SeGZeZuj22njMYEA``` → https://www.youtube.com/feeds/videos.xml?channel_id=UCOkL7q2SeGZeZuj22njMYEA
Applies to: Main window (address bar)

# Rule 10 (For redirecting playlist feeds)

Redirect: ```https://[Invidious Domain Here]/feed/playlist/*```
to: ```https://www.youtube.com/feeds/videos.xml?playlist_id=$1```
Example: ```https://[Invidious Domain Here]/feed/playlist/PLY_6uAtgkYXl1sPyzNa2UFQYgPj2qA-qj``` → https://www.youtube.com/feeds/videos.xml?playlist_id=PLY_6uAtgkYXl1sPyzNa2UFQYgPj2qA-qj
Applies to: Main window (address bar)



