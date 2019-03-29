Download Tampermonkey for your Browser:  
[Firefox](https://addons.mozilla.org/firefox/addon/tampermonkey/)  
[Chrome and Chromium](https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo)  
[Opera](https://addons.opera.com/extensions/details/tampermonkey-beta/)  

Than add the following script in Tampermonkey. It will always add `&local=true` to the end of the video url.

```
// ==UserScript==
// @name        Invidious Proxy automatically
// @match       *://*.invidio.us/watch?v=*
// @run-at      document-start
// @grant       none
// ==/UserScript==


if (!(/[?&]quality=dash/).test(location.search)) {
  location.search += (location.search ? "&" : "?") + "local=true";
}
```

You can also enable this by checking `Proxy videos? ` in your preferences.