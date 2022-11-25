# What is Redirector?

Redirector is a Browser extension for Firefox and Chromium that can manually be configured to redirect links, such as YouTube to Invidious or [Twitter to Nitter](https://github.com/zedeus/nitter/wiki/Extensions#redirector)

Get redirector: [Firefox](https://addons.mozilla.org/en-US/firefox/addon/redirector/) — [Chromium-based](https://chrome.google.com/webstore/detail/redirector/ocgpenflpmgnfapjedencafcfakcekcd) — [GitHub](https://github.com/einaregilsson/Redirector)

# How to use it for Invidious Redirects?

For basic redirects, you will need the following rules set up.

# Rule 1

Redirects Youtube Videos to Invidious
Redirect: https://*.youtube.com/watch?*v=*
to: https://[Invidious Domain Here]/watch?$2v=$3
Hint: Redirects individual videos to their Invidious equivelant
Example: https://www.youtube.com/watch?v=Lz13cxZNTCo → https://[Invidious Domain Here]/watch?v=Lz13cxZNTCo
Applies to: Main window (address bar)

# Rule 2 (Note, Rule 2 is for redirecting the youtu.be domain, typically accociated with embeds)

Redirect: https://youtu.be/*
to: https://[Invidious Domain Here]/watch?v=$1
Example: https://youtu.be/Ae5yV4p7uh8?t=35 → https://[Invidious Domain Here]/watch?v=Ae5yV4p7uh8?t=35

# Rule 3 (Note, Rule 3 is for those who use DDG bangs or search extensions to search YouTube and would like those properly redirected to Invidious)

Redirect YouTube Search to Invidious
Redirect: https://www.youtube.com/results?search_query=*&page
to: https://[Invidious Domain Here]/search?q=$1
Example: https://www.youtube.com/results?search_query=Smash+Bros+Trailer&page → https://[Invidious Domain Here]/search?q=Smash+Bros+Trailer
Applies to: Main window (address bar)


# Rule 4

Redirects Youtube to Invidous
Redirect: https://*.youtube.com/*
to: https://[Invidious Domain Here]/$2
Example: https://www.youtube.com/channel/UCOkL7q2SeGZeZuj22njMYEA → https://[Invidious Domain Here]/channel/UCOkL7q2SeGZeZuj22njMYEA
Applies to: Main window (address bar)


If you would like to use URL Parameters in your redirects (see https://github.com/cloudrac3r/invidious-documentation/blob/master/List-of-URL-parameters.md), you will need to manually add them to Rule 1, (https://[Invidious Domain Here]/watch?v=$1[URL Parameters here] in place of https://[Invidious Domain Here]/watch?v=$1.

For clarity, an example of a URL parameter would be &related_videos=false&comments=false to ensure that neither related videos nor comments are displayed on a video page, so https://[Invidious Domain Here]/watch?v=$1&related_videos=false&comments=false would be the destination of redirects.

Should you choose to use URL Parameters, I would reccomend adding the following rule to both ensure all invidious videos load with your preference, and to ensure that unnecesary parameters are not added when already applied. 

# Rule 5

Redirects Invidious Videos with URL Parameters
Redirect: https://[Invidious Domain Here]/watch?v=*
to: https://[Invidious Domain Here]/watch?v=$1[URL Parameters here]
excluding: https://[Invidious Domain Here]/watch?v=*[URL Parameters here]
Hint: Update this to correlate with the YouTube Video Redirect
Example: https://[Invidious Domain Here]/watch?v=Lz13cxZNTCo → https://[Invidious Domain Here]/watch?v=Lz13cxZNTCo[URL Parameters here]
Applies to: Main window (address bar)

It is important that you add the exception so as not to create infinite repeats of the same URL Parameters when opening multiple Invidious Videos in a single session. When creating or editing rules in Redirector you must access "Advanced Options" in order to set exceptions. 

For redirecting embeds, you'll need the following two rules.

# Rule 6

Redirects Embedded Youtube Videos to Invidious
Redirect: https://www.youtube.com/embed/*
to: https://[Invidious Domain Here]/embed/$1
Hint: Redirects individual videos to their Invidious equivelant
Example: https://www.youtube.com/embed/Lz13cxZNTCo → https://[Invidious Domain Here]/embed/Lz13cxZNTCo
Applies to: Main window (address bar), IFrames

# Rule 7

Redirects Embedded Youtube Videos to Invidious
Redirect: https://www.youtube-nocookie.com/embed/*
to: https://[Invidious Domain Here]/embed/$1
Hint: Redirects individual videos to their Invidious equivelant
Example: https://www.youtube-nocookie.com/embed/Lz13cxZNTCo → https://[Invidious Domain Here]/embed/Lz13cxZNTCo
Applies to: Main window (address bar), IFrames

(Note, it is imparative that you check it applies to both the Main Window and IFrames, otherwise the rule won't applied to Embeds).


Finally, if you like to subscribe to channels using RSS feeds, you made add the following two rules to redirect Invidious RSS feeds to their YouTube equivelants. This way you'll still have access to your feeds should you need to migrate to another instance. 

# Rule 8

Redirect Invidious Feeds to YouTube Feeds
Redirect: https://[Invidious Domain Here]/feed/channel/*
to: https://www.youtube.com/feeds/videos.xml?channel_id=$1
Hint: And now you can subscribe in peace.
Example: https://[Invidious Domain Here]/feed/channel/UCOkL7q2SeGZeZuj22njMYEA → https://www.youtube.com/feeds/videos.xml?channel_id=UCOkL7q2SeGZeZuj22njMYEA
Applies to: Main window (address bar)

#Rule 9

Redirect Playlist RSS from Invidious to YouTube
Redirect: https://[Invidious Domain Here]/feed/playlist/*
to: https://www.youtube.com/feeds/videos.xml?playlist_id=$1
Example: https://[Invidious Domain Here]/feed/playlist/PLY_6uAtgkYXl1sPyzNa2UFQYgPj2qA-qj → https://www.youtube.com/feeds/videos.xml?playlist_id=PLY_6uAtgkYXl1sPyzNa2UFQYgPj2qA-qj
Applies to: Main window (address bar)

All of these rules are made with Wildcard Processing. 

