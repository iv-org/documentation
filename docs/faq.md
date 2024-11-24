# Frequently Asked Questions

## Table of Contents

- Using Invidious
  * [Can I use Invidious on my device?](#q-can-i-use-invidious-on-my-device)
  * [Do you plan to make an Android/iOS app?](#q-do-you-plan-to-make-an-androidios-app)
  * [Can I synchronize my account between instances?](
    #q-can-i-synchronize-my-account-between-instances)
  * [What data is collected by Invidious?](#q-what-data-is-collected-by-invidious)
  * [What data is shared with YouTube?](#q-what-data-is-shared-with-youtube)

- Commonly encountered errors/problems
  * [The media could not be loaded…](#q-the-media-could-not-be-loaded)
  * [Could not check out a connection in 2.0 seconds (DB::PoolTimeout)](
    #q-could-not-check-out-a-connection-in-20-seconds-dbpooltimeout)
  * [`DB::PoolRetryAttemptsExceeded`](#q-dbpoolretryattemptsexceeded)
  * [Subtitles are not working!](#q-subtitles-are-not-working)
  * [Where are the 360p/480p/1080p quality options?](
    #q-where-are-the-360p480p1080p-quality-options)

- Running your own instance
  * [Do you provide pre-built binaries (`.deb`, `.rpm`, etc..)?](
    #q-do-you-provide-pre-built-binaries-deb-rpm-etc)
  * [How can I configure _[thing]_?](#q-how-can-i-configure-thing)
  * [RSS feeds/links/etc... URLs redirect to `<IP>:3000` but I have a reverse proxy!](
    #q-rss-feedslinksetc-urls-redirect-to-ip3000-but-i-have-a-reverse-proxy)
  * [The "popular" feed/page on my instance is empty!](
    #q-the-popular-feedpage-on-my-instance-is-empty)
  * [I can't log in nor save preferences](#q-i-cant-log-in-nor-save-preferences)


# Using Invidious

## **Q:** Can I use Invidious on my device?

**A:** As long as your device is equipped with a modern web browser,
sure, of course! A responsive interface is available for mobile/tablets.

<br/>

## **Q:** Do you plan to make an Android/iOS app?

**A:** No. Invidious is and will always be a browser application.

If you have an Android phone/tablet, you can check the
[NewPipe](https://github.com/TeamNewPipe/NewPipe) application.

<br/>

## **Q:** Can I synchronize my account between instances?

**A:** Short answer: manually => Yes, automatically => No.

**How to do it manually:**

1. Go to the import/export page while connected to your account (preferences
page, then click the "Import/export data" link at the bottom of the page)
2. Click on "Export Invidious data as JSON"
3. Go to the same import/export page on the other instance
4. Use "Import Invidious JSON data"
5. Press import

Yes, we're aware that it's cumbersome. Please continue to read to understand
why we don't implement automatic synchronization.

**Why we don't implement automatic sync:**

TL;DR: we don't have the time to implement/maintain it.

To get automatic synchronization, we have 3 options:
  1. Centralized database (like Youtube)
  2. Federation (like Matrix, Mastodon and PeerTube)
  3. An external tool that uses the API

1. A centralized database goes against our idea of a decentralized web so
let's ignore that right away (plus, we don't want to risk hosting large
amounts of user data anyway).

2. Federation is a good option (it works well for the others), however we
currently don't have the time nor the resources required to implement it.

3. An external tool (that runs locally on your PC, or a self-hosted server
like _Firefox Sync_) is also a valid option. As for federation, we don't
have the resources to develop such a solution. PRs and external tool
propositions are welcome!

Please see the following issues for more details on the subject:
https://github.com/iv-org/invidious/issues/2515

<br/>

## **Q:** What data is collected by Invidious?

**A:** Invidious by itself does not collect any data about its users, but
keep in mind that instance owners can log your IP address (like any other
server on the internet).

By default, the server logs which URLs were accessed, the associated error
code (e.g 404 if the URL was not found) and the time it took for the server
to respond.

Here is what the server logs look like:

```
2021-08-30 18:15:44 UTC [info] 200 GET /watch?v=GIAKHj9uJtM 781.21ms
2021-08-30 18:15:49 UTC [info] 200 GET /api/v1/search?q=Fly%20away 500.0ms
2021-08-30 18:15:49 UTC [info] 200 GET /vi/lJcqAzWFWLs/mqdefault.jpg 15.82ms
2021-08-30 18:15:49 UTC [info] 200 GET /vi/JoP_Tte7z7o/mqdefault.jpg 70.64ms
```

When you create an account, your watch history and the list of channels you
subscribed will be stored in the server's database. You can export, migrate
or delete these data at any time from your user account page.

<br/>

## **Q:** What data is shared with YouTube?

**A:** By default, the video stream is fetched directly from Google's servers
(`googlevideo.com`) in order to reduce the bandwidth required by Invidious,
meaning that Google will be able to see your IP address and some other data
commonly sent by web browsers, like your user-agent string.

If you don't want that to happen, you can go to the `preferences` page and
check the `Proxy videos` option. When this option is enabled, the Invidious
instance will be used as a relay (also known as a "proxy") between you and
Google's servers, which will hide your IP address and the other information
sent by your browser.

<br/>


# Commonly encountered errors/problems

## **Q:** The media could not be loaded…

**A:** This problem can occur in different scenarios:

* If you are the one that have installed Invidious, please read the page
  ["All the YouTube error messages explained with solutions"](/youtube-errors-explained/)

* If you're trying to watch a music clip, Youtube is likely blocking the
  video stream. Try enabling `Proxy videos` in the preferences (or add
  `&local=1` in the URL). Switching to another instance is also a good
  alternative, as this type of content is often geo-restricted.

* Youtube often sends corrupted video data for the `hd720`, `medium` and
  `small` quality settings. Refreshing the page multiple times (5-7) can
  fix the problem. You may also set your `preferred video quality` to
  `dash` (or add `&quality=dash` to the URL).

* Rarely, it can be due to an internal failure of the instance and the
  video stream can't be fetched. A simple page refresh can solve the issue.

If none of the solutions listed above fix the problem, try switching
instances. And if that still doesn't work, you'll have to watch the video
on YouTube itself (sorry for the inconvenience).

<br/>

## **Q:** Could not check out a connection in 2.0 seconds (DB::PoolTimeout)

**A: Please, do not open a bug report on github, we can't do anything!**

The instance you are using is having _database issues_. Please use another
instance from the [list of public instances](https://instances.invidious.io)

<br/>

## **Q:** `DB::PoolRetryAttemptsExceeded`

**A:** The instance you are using is having _database issues_. Please use
another instance from the [list of public instances](
https://instances.invidious.io)

If you're an instance admin, first try restarting Invidious. Then try
restarting PostgreSQL. If neither fixed the problem, try [increasing the
maximum number of connections allowed](https://stackoverflow.com/a/32584211).
Some distributions change the default to a low number.

## **Q:** Subtitles are not working!

**A:** Subtitles (also know as "Closed Captions") are generally not working
on popular Invidious instances. This is due to URL rate limiting coming
from Google servers.

To solve that, try using a less popular public instance or host Invidious
yourself.

Please take a look at the following issue for more details:
https://github.com/iv-org/invidious/issues/2567

<br/>

## **Q:** Where are the 360p/480p/1080p quality options?

**A:** These quality options are only available when DASH is enabled.
In order to enable DASH, go to the preferences and set the preferred
video quality to "DASH".

Note that DASH requires Javascript and _can_ be disabled by the instance
administrator. So if the option is not available to you, try to switch to
another instance.

By default, DASH is not enabled to allow videos to be played without
Javascript and also to save on bandwidth (DASH **must** be proxied in order
to work properly, which uses a lot of the instance bandwidth).

<br/>


# Running your own instance

## **Q:** Do you provide pre-built binaries (`.deb`, `.rpm`, etc.)?

**A:** We currently don't provide those, due to the rolling release nature
of Invidious. Get a fresh `clone` or `pull` the latest commits from `master`
instead.

<br/>

## **Q:** How can I configure _[thing]_?

**A:** Read the example config file (`config/config.example.yml`).
All the supported configuration options are documented there.

<br/>

## **Q:** RSS feeds/links/etc... URLs redirect to `<IP>:3000` but I have a reverse proxy!

**A:** Make sure that the following parameters are set according to your environment:
- `https_only`: if your instance is served over HTTPS
- `domain`: if you have a domain name that redirects to your instance
- `external_port`: if your instance is accessed from a different port than
  the listening one (e.g your instance listens on :3000, but is available on
  :443 through a reverse proxy, set `external_port` to `443`)

<br/>

## **Q:** The "popular" feed/page on my instance is empty!

**A:** The "popular" feed is generated from the videos that are popular amongst
the users registered on your instance. If nobody has created an account on your
instance (e.g if registration is disabled) the popular feed will be empty.

<br/>

## **Q:** I can't log in nor save preferences!

**A:** Double check your config! The value of the `domain` config option is
used for the session (`SID`) and preferences (`PREFS`) cookies. If set
incorrectly, the cookies will be invalid, and your browser will silently
ignore them.

**If you access your Invidious instance by IP address (like `192.168.1.205`)
then leave the `domain` config option EMPTY!**

Common invalid values include:
 - IP addresses (like `192.168.1.205`)
 - Scheme before the domain (`https://example.com`)
 - Port after the domain (`example.com:3000`)
 - Typo in the FQDN (`<domain>.cm` instead of `<domain>.com`)
