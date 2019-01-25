Download Tampermonkey for your Browser:  
[Firefox](https://addons.mozilla.org/firefox/addon/tampermonkey/)  
[Chrome and Chromium](https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo)  
[Opera](https://addons.opera.com/extensions/details/tampermonkey-beta/)  

Than add the following script in Tampermonkey. It will always add `&quality=dash` to the end of the video url.

```
// ==UserScript==
// @name        Invidious Proxy automatically
// @match       *://*.invidio.us/watch?v=*
// @run-at      document-start
// @grant       none
// ==/UserScript==


if (!(/[?&]quality=dash/).test(location.search)) {
  location.search += (location.search ? "&" : "?") + "quality=dash";
}
```

##### NOTE: At the moment `googlevideo.com` will still be loaded as third party even with `dash` enabled. The current workaround is to either block this with [uBlock](https://addons.mozilla.org/firefox/addon/ublock-origin/), [uMatrix](https://addons.mozilla.org/firefox/addon/umatrix/) or [NoScript](https://addons.mozilla.org/firefox/addon/noscript/)